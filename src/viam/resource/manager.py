from threading import RLock
from typing import Dict, List, Type, TypeVar

from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.services.service_base import ServiceBase

from ..components.component_base import ComponentBase
from ..errors import DuplicateResourceError, ResourceNotFoundError

ResourceType = TypeVar("ResourceType", bound=ResourceBase)


class ResourceManager:
    """
    Registry containing all components registered to this server.
    """

    resources: Dict[ResourceName, ResourceBase]
    _short_to_long_name: Dict[str, List[ResourceName]]
    _lock: RLock

    def __init__(self, components: List[ResourceBase] = []) -> None:
        self._lock = RLock()
        self.resources = {}
        self._short_to_long_name = {}
        for component in components:
            self.register(component)

    def register(self, component: ResourceBase):
        """
        Register a new component with the registry.
        Components may not have the same name.
        If a component is remote and the short name is unique, save a short name version.

        Raises:
            DuplicateComponentError: Error if attempting to register component
                                     with the name of an existing component

        Args:
            component (ResourceBase): The component to register
        """
        _BaseClasses = (ResourceBase, ComponentBase, ServiceBase)
        rnames: Dict[ResourceName, ResourceBase] = {}
        for subtype in component.__class__.mro():
            if subtype in _BaseClasses:
                continue
            if hasattr(subtype, "get_resource_name"):
                rn = subtype.get_resource_name(component.name)  # type: ignore
                rnames[rn] = component
        for rn in rnames:
            if ":" in rn.name:
                short_name = rn.name.split(":")[-1]
                if short_name in self._short_to_long_name and rn not in self._short_to_long_name[short_name]:
                    self._short_to_long_name[short_name].append(rn)
                elif short_name not in self._short_to_long_name:
                    self._short_to_long_name[short_name] = [rn]

        if rnames.keys() & self.resources.keys():
            raise DuplicateResourceError(component.name)

        with self._lock:
            self.resources.update(rnames)

    def get_resource(self, of_type: Type[ResourceType], name: ResourceName) -> ResourceType:
        """
        Return a resource from the registry.
        If a unique short name version is given, return a remote resource with the name.

        Args:
            of_type (Type[ResourceType]): The type of the resource
            name (viam.proto.common.ResourceName): The name of the resource

        Raises:
            ResourceNotFoundError: Error if resource with the given type
                                    and name does not exist in the registry

        Returns:
            ResourceType: The resource
        """
        with self._lock:
            resource = self.resources.get(name, None)
            if resource and isinstance(resource, of_type):
                return resource

            if name.name in self._short_to_long_name and len(self._short_to_long_name[name.name]) == 1:
                return self.get_resource(of_type, self._short_to_long_name[name.name][0])
            raise ResourceNotFoundError(name.subtype, name.name)

    def remove_resource(self, name: ResourceName):
        """Remove the resource with the specified ```ResourceName```.

        Args:
            name (viam.proto.common.ResourceName): The ResourceName of the resource
        """
        with self._lock:
            del self.resources[name]

    def _resource_by_name_only(self, name: str) -> ResourceBase:
        for rname, resource in self.resources.items():
            if rname.name == name:
                return resource
        raise ResourceNotFoundError("resource", name)
