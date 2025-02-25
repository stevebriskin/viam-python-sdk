from inspect import iscoroutinefunction
from threading import Lock
from typing import List, Mapping, Optional, Sequence, Tuple

from grpclib.utils import _service_name

from viam import logging
from viam.components.component_base import ComponentBase
from viam.errors import ResourceNotFoundError, ValidationError
from viam.proto.app.robot import ComponentConfig
from viam.proto.module import (
    AddResourceRequest,
    HandlerDefinition,
    HandlerMap,
    ReadyRequest,
    ReadyResponse,
    ReconfigureResourceRequest,
    RemoveResourceRequest,
    ValidateConfigRequest,
    ValidateConfigResponse,
)
from viam.proto.robot import ResourceRPCSubtype
from viam.resource.base import ResourceBase
from viam.resource.registry import Registry
from viam.resource.types import Model, ResourceName, Subtype, resource_name_from_string
from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions
from viam.rpc.server import Server

from .service import ModuleService
from .types import Reconfigurable, Stoppable

LOGGER = logging.getLogger(__name__)


class Module:
    _address: str
    _parent_address: Optional[str] = None
    _ready: bool
    _log_level: int
    _lock: Lock
    parent: Optional[RobotClient] = None
    server: Server

    def __init__(self, address: str, *, log_level: int = logging.DEBUG) -> None:
        self._address = address
        self.server = Server(components=[], module_service=ModuleService(self))
        self._log_level = log_level
        self._ready = True
        self._lock = Lock()

    async def _connect_to_parent(self):
        if self.parent is None:
            if self._parent_address is None:
                raise ValueError("Parent address not found")
            self.parent = await RobotClient.at_address(
                self._parent_address,
                RobotClient.Options(
                    dial_options=DialOptions(disable_webrtc=True, insecure=True),
                    log_level=self._log_level,
                ),
            )

    async def _get_component(self, name: ResourceName) -> ComponentBase:
        await self._connect_to_parent()
        assert self.parent is not None
        await self.parent.refresh()
        return self.parent.get_component(name)

    async def _get_dependencies(self, dependencies: Sequence[str]) -> Mapping[ResourceName, ComponentBase]:
        deps: Mapping[ResourceName, ComponentBase] = {}
        for dep in dependencies:
            rn = resource_name_from_string(dep)
            component = await self._get_component(rn)
            deps[rn] = component
        return deps

    async def start(self):
        """Start the module service and gRPC server"""
        try:
            await self.server.serve(log_level=self._log_level, path=self._address)
        finally:
            await self.stop()

    async def stop(self):
        """Stop the module service and gRPC server"""
        LOGGER.debug("Shutting down module")
        try:
            if self.parent is not None:
                await self.parent.close()
        except Exception as e:
            LOGGER.error("Encountered error while shutting down module", exc_info=e)

    def set_ready(self, ready: bool):
        """Set the module's ready state. The module automatically sets to READY on load. Setting to False can be useful
        in instances where the module is not instantly ready (e.g. waiting on hardware)

        Args:
            ready (bool): Whether the module is ready
        """
        with self._lock:
            self._ready = ready

    async def add_resource(self, request: AddResourceRequest):
        dependencies = await self._get_dependencies(request.dependencies)
        config: ComponentConfig = request.config
        subtype = Subtype.from_string(config.api)
        model = Model.from_string(config.model, ignore_errors=True)
        creator = Registry.lookup_resource_creator(subtype, model)
        resource = creator(config, dependencies)
        self.server.register(resource)

    async def reconfigure_resource(self, request: ReconfigureResourceRequest):
        dependencies = await self._get_dependencies(request.dependencies)
        config: ComponentConfig = request.config
        subtype = Subtype.from_string(config.api)
        name = config.name
        rn = ResourceName(namespace=subtype.namespace, type=subtype.resource_type, subtype=subtype.resource_subtype, name=name)
        resource = self.server.get_resource(ResourceBase, rn)
        if isinstance(resource, Reconfigurable):
            resource.reconfigure(config, dependencies)
        else:
            if isinstance(resource, Stoppable):
                if iscoroutinefunction(resource.stop):
                    await resource.stop()
                else:
                    resource.stop()
            add_request = AddResourceRequest(config=request.config, dependencies=request.dependencies)
            self.server.remove_resource(rn)
            await self.add_resource(add_request)

    async def remove_resource(self, request: RemoveResourceRequest):
        rn = resource_name_from_string(request.name)
        resource = self.server.get_resource(ResourceBase, rn)
        if isinstance(resource, Stoppable):
            if iscoroutinefunction(resource.stop):
                await resource.stop()
            else:
                resource.stop()
        self.server.remove_resource(rn)

    async def ready(self, request: ReadyRequest) -> ReadyResponse:
        self._parent_address = request.parent_address

        svcname_to_models: Mapping[Tuple[str, Subtype], List[Model]] = {}
        for subtype_model_str in Registry.REGISTERED_RESOURCE_CREATORS().keys():
            subtype_str, model_str = subtype_model_str.split("/")
            subtype = Subtype.from_string(subtype_str)
            model = Model.from_string(model_str)

            registration = Registry.lookup_subtype(subtype)
            service = registration.rpc_service(self.server)
            service_name = _service_name(service)

            models = svcname_to_models.get((service_name, subtype), [])
            models.append(model)
            svcname_to_models[(service_name, subtype)] = models

        handlers: List[HandlerDefinition] = []
        for key, value in svcname_to_models.items():
            svc_name, subtype = key
            rpc_subtype = ResourceRPCSubtype(
                subtype=ResourceName(
                    namespace=subtype.namespace,
                    type=subtype.resource_type,
                    subtype=subtype.resource_subtype,
                    name="",
                ),
                proto_service=svc_name,
            )
            handler_def = HandlerDefinition(subtype=rpc_subtype, models=[str(model) for model in value])
            handlers.append(handler_def)

        return ReadyResponse(ready=self._ready, handlermap=HandlerMap(handlers=handlers))

    def add_model_from_registry(self, subtype: Subtype, model: Model):
        """Add a pre-registered model to this Module"""

        # All we need to do is double check that the model has already been registered
        try:
            Registry.lookup_resource_creator(subtype, model)
        except ResourceNotFoundError:
            raise ValueError(f"Cannot add model because it has not been registered. Subtype: {subtype}. Model: {model}")

    async def validate_config(self, request: ValidateConfigRequest) -> ValidateConfigResponse:
        config: ComponentConfig = request.config
        subtype = Subtype.from_string(config.api)
        model = Model.from_string(config.model)
        validator = Registry.lookup_validator(subtype, model)
        try:
            dependencies = validator(config)
            return ValidateConfigResponse(dependencies=dependencies)
        except Exception as e:
            raise ValidationError(f"{type(Exception)}: {e}").grpc_error
