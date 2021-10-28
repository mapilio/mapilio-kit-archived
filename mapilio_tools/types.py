import datetime
import sys
import typing as T

if sys.version_info >= (3, 8):
    from typing import TypedDict, Literal  # pylint: disable=no-name-in-module
else:
    from typing_extensions import TypedDict, Literal


class User(TypedDict, total=False):
    OrganizationKey: str
    OrganizationProjectKey: str
    SettingsUsername: str
    SettingsUserKey: str
    user_upload_token: str


# class CompassHeading(TypedDict, total=True):
#     Heading: float
#     # MagneticHeading: float


class ImageRequired(TypedDict, total=True):
    Latitude: float
    Longitude: float
    CaptureTime: str


class Image(ImageRequired, total=False):
    Altitude: float
    PhotoUUID: str
    Heading: float
    # Heading: CompassHeading


class _SequenceOnly(TypedDict, total=True):
    SequenceUUID: str


class Sequence(_SequenceOnly, total=False):
    Heading: float


class MetaProperties(TypedDict, total=False):
    MetaTags: T.Dict
    DeviceMake: str
    DeviceModel: str
    GPSAccuracyMeters: float
    CameraUUID: str
    Filename: str
    Orientation: int


class FinalImageDescription(_SequenceOnly, User, Image):
    pass


class ImageDescriptionJSON(FinalImageDescription):
    filename: str


class FinalImageDescriptionError(TypedDict):
    filename: str
    error: T.Dict


FinalImageDescriptionOrError = T.Union[
    FinalImageDescriptionError, FinalImageDescription
]


class FinalImageDescriptionFromGeoJSON(FinalImageDescription):
    pass


UserItemSchema = {
    "type": "object",
    "properties": {
        "OrganizationKey": {"type": "string"},
        "OrganizationProjectKey": {"type": "string"},
        "SettingsUsername": {"type": "string"},
        "SettingsUserKey": {"type": "string"},
        "user_upload_token": {"type": "string"},
    },
    "required": ["SettingsUserKey", "user_upload_token"],
    "additionalProperties": False,
}

FinalImageDescriptionSchema = {
    "type": "object",
    "properties": {
        "Latitude": {"type": "number", "description": "Latitude of the image"},
        "Longitude": {"type": "number", "description": "Longitude of the image"},
        "Altitude": {"type": "number", "description": "Altitude of the image"},
        "CaptureTime": {
            "type": "string",
            "description": "Capture time of the image",
        },
        "PhotoUUID": {"type": "string"},
        "Heading": {"type": "number"},
        "SequenceUUID": {
            "type": "string",
            "description": "Arbitrary key used to group images",
        },
        "DeviceModel": {"type": "string"},
        "DeviceMake": {"type": "string"},
        "CameraUUID": {"type": "string"},
        "Filename": {"type": "string"},
        "Orientation": {"type": "integer"},
    },
    "required": [
        "Latitude",
        "Longitude",
        "CaptureTime",
    ],
    "additionalProperties": False,
}


def merge_schema(*schemas: T.Dict):
    for s in schemas:
        assert s.get("type") == "object", "must be all object schemas"
    properties = {}
    all_required = []
    additional_properties = True
    for s in schemas:
        properties.update(s.get("properties", {}))
        all_required += s.get("required", [])
        if "additionalProperties" in s:
            additional_properties = s["additionalProperties"]
    return {
        "type": "object",
        "properties": properties,
        "required": list(set(all_required)),
        "additionalProperties": additional_properties,
    }


ImageDescriptionJSONSchema = merge_schema(
    FinalImageDescriptionSchema,
    {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "The image file's path relative to the image directory",
            },
        },
        "required": [
            "filename",
        ],
    },
)

Process = Literal[
    "import_meta_data_process",
    "geotag_process",
    "sequence_process",
    "mapilio_image_description",
]

Status = Literal["success", "failed"]


def datetime_to_map_capture_time(time: datetime.datetime) -> str:
    return datetime.datetime.strftime(time, "%Y_%m_%d_%H_%M_%S_%f")[:-3]


def map_capture_time_to_datetime(time: str) -> datetime.datetime:
    return datetime.datetime.strptime(time, "%Y_%m_%d_%H_%M_%S_%f")


class GPXPoint(T.NamedTuple):
    # Put it first for sorting
    time: datetime.datetime
    lat: float
    lon: float
    alt: T.Optional[float]

    def as_desc(self) -> Image:
        desc: Image = {
            "Latitude": self.lat,
            "Longitude": self.lon,
            "CaptureTime": datetime_to_map_capture_time(self.time),
        }
        if self.alt is not None:
            desc["Altitude"] = self.alt
        return desc


class GPXPointAngle(T.NamedTuple):
    point: GPXPoint
    angle: T.Optional[float]

    def as_desc(self) -> Image:
        desc = self.point.as_desc()
        if self.angle is not None:
            desc["Heading"] = self.angle
        return desc


if __name__ == "__main__":
    import json

    print(json.dumps(ImageDescriptionJSONSchema, indent=4))
