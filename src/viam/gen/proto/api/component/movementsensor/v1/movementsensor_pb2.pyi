"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
from ...... import proto
import typing
import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class GetLinearVelocityRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    'Name of a movement sensor'

    def __init__(self, *, name: typing.Text=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___GetLinearVelocityRequest = GetLinearVelocityRequest

class GetLinearVelocityResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LINEAR_VELOCITY_FIELD_NUMBER: builtins.int

    @property
    def linear_velocity(self) -> proto.api.common.v1.common_pb2.Vector3:
        """linear velocity contains velocity in mm/s across x/y/z axes"""
        pass

    def __init__(self, *, linear_velocity: typing.Optional[proto.api.common.v1.common_pb2.Vector3]=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['linear_velocity', b'linear_velocity']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['linear_velocity', b'linear_velocity']) -> None:
        ...
global___GetLinearVelocityResponse = GetLinearVelocityResponse

class GetAngularVelocityRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    'Name of a movement sensor'

    def __init__(self, *, name: typing.Text=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___GetAngularVelocityRequest = GetAngularVelocityRequest

class GetAngularVelocityResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ANGULAR_VELOCITY_FIELD_NUMBER: builtins.int

    @property
    def angular_velocity(self) -> proto.api.common.v1.common_pb2.Vector3:
        """angular velocity contains velocity in degrees/s across x/y/z axes"""
        pass

    def __init__(self, *, angular_velocity: typing.Optional[proto.api.common.v1.common_pb2.Vector3]=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['angular_velocity', b'angular_velocity']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['angular_velocity', b'angular_velocity']) -> None:
        ...
global___GetAngularVelocityResponse = GetAngularVelocityResponse

class GetCompassHeadingRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    'Name of a movement sensor'

    def __init__(self, *, name: typing.Text=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___GetCompassHeadingRequest = GetCompassHeadingRequest

class GetCompassHeadingResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    VALUE_FIELD_NUMBER: builtins.int
    value: builtins.float
    'A number from 0-359 where\n    0 is North, 90 is East, 180 is South, and 270 is   West\n    '

    def __init__(self, *, value: builtins.float=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['value', b'value']) -> None:
        ...
global___GetCompassHeadingResponse = GetCompassHeadingResponse

class GetOrientationRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    'Name of a movement sensor'

    def __init__(self, *, name: typing.Text=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___GetOrientationRequest = GetOrientationRequest

class GetOrientationResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ORIENTATION_FIELD_NUMBER: builtins.int

    @property
    def orientation(self) -> proto.api.common.v1.common_pb2.Orientation:
        ...

    def __init__(self, *, orientation: typing.Optional[proto.api.common.v1.common_pb2.Orientation]=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['orientation', b'orientation']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['orientation', b'orientation']) -> None:
        ...
global___GetOrientationResponse = GetOrientationResponse

class GetPositionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    'Name of a movement sensor'

    def __init__(self, *, name: typing.Text=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___GetPositionRequest = GetPositionRequest

class GetPositionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    COORDINATE_FIELD_NUMBER: builtins.int
    ALTITUDE_MM_FIELD_NUMBER: builtins.int

    @property
    def coordinate(self) -> proto.api.common.v1.common_pb2.GeoPoint:
        ...
    altitude_mm: builtins.float

    def __init__(self, *, coordinate: typing.Optional[proto.api.common.v1.common_pb2.GeoPoint]=..., altitude_mm: builtins.float=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['coordinate', b'coordinate']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['altitude_mm', b'altitude_mm', 'coordinate', b'coordinate']) -> None:
        ...
global___GetPositionResponse = GetPositionResponse

class GetPropertiesRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    'Name of a movement sensor'

    def __init__(self, *, name: typing.Text=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___GetPropertiesRequest = GetPropertiesRequest

class GetPropertiesResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LINEAR_VELOCITY_SUPPORTED_FIELD_NUMBER: builtins.int
    ANGULAR_VELOCITY_SUPPORTED_FIELD_NUMBER: builtins.int
    ORIENTATION_SUPPORTED_FIELD_NUMBER: builtins.int
    POSITION_SUPPORTED_FIELD_NUMBER: builtins.int
    COMPASS_HEADING_SUPPORTED_FIELD_NUMBER: builtins.int
    linear_velocity_supported: builtins.bool
    angular_velocity_supported: builtins.bool
    orientation_supported: builtins.bool
    position_supported: builtins.bool
    compass_heading_supported: builtins.bool

    def __init__(self, *, linear_velocity_supported: builtins.bool=..., angular_velocity_supported: builtins.bool=..., orientation_supported: builtins.bool=..., position_supported: builtins.bool=..., compass_heading_supported: builtins.bool=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['angular_velocity_supported', b'angular_velocity_supported', 'compass_heading_supported', b'compass_heading_supported', 'linear_velocity_supported', b'linear_velocity_supported', 'orientation_supported', b'orientation_supported', 'position_supported', b'position_supported']) -> None:
        ...
global___GetPropertiesResponse = GetPropertiesResponse

class GetAccuracyRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    'Name of a movement sensor'

    def __init__(self, *, name: typing.Text=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['name', b'name']) -> None:
        ...
global___GetAccuracyRequest = GetAccuracyRequest

class GetAccuracyResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class AccuracyMmEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: builtins.float

        def __init__(self, *, key: typing.Text=..., value: builtins.float=...) -> None:
            ...

        def ClearField(self, field_name: typing_extensions.Literal['key', b'key', 'value', b'value']) -> None:
            ...
    ACCURACY_MM_FIELD_NUMBER: builtins.int

    @property
    def accuracy_mm(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, builtins.float]:
        ...

    def __init__(self, *, accuracy_mm: typing.Optional[typing.Mapping[typing.Text, builtins.float]]=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['accuracy_mm', b'accuracy_mm']) -> None:
        ...
global___GetAccuracyResponse = GetAccuracyResponse