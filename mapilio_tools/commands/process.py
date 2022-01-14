import inspect
import argparse

from ..insert_MAPJson import insert_MAPJson
from ..process_geotag_properties import process_geotag_properties
from ..process_import_meta_properties import (
    process_import_meta_properties,
)
from ..process_sequence_properties import process_sequence_properties


class Command:
    name = "process"
    help = "process images"

    def add_basic_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "--skip_process_errors",
            help="Skip process errors.",
            action="store_true",
            default=False,
            required=False,
        )
        group = parser.add_argument_group("process EXIF options")
        group.add_argument(
            "--overwrite_all_EXIF_tags",
            help="Overwrite the rest of the EXIF tags, whose values are changed during the processing. Default is False"
                 ", which will result in the processed values to be inserted only in the EXIF Image Description tag.",
            action="store_true",
            default=False,
            required=False,
        )
        group.add_argument(
            "--overwrite_EXIF_time_tag",
            help="Overwrite the capture time EXIF tag with the value obtained in process.",
            action="store_true",
            default=False,
            required=False,
        )
        group.add_argument(
            "--overwrite_EXIF_gps_tag",
            help="Overwrite the GPS EXIF tag with the value obtained in process.",
            action="store_true",
            default=False,
            required=False,
        )
        group.add_argument(
            "--overwrite_EXIF_direction_tag",
            help="Overwrite the camera direction EXIF tag with the value obtained in process.",
            action="store_true",
            default=False,
            required=False,
        )
        group.add_argument(
            "--overwrite_EXIF_orientation_tag",
            help="Overwrite the orientation EXIF tag with the value obtained in process.",
            action="store_true",
            default=False,
            required=False,
        )

        group_metadata = parser.add_argument_group("process metadata options")
        group_metadata.add_argument(
            "--device_make",
            help="Specify device manufacturer. Note this input has precedence over the input read from "
                 "the import source file.",
            default=None,
            required=False,
        )
        group_metadata.add_argument(
            "--device_model",
            help="Specify device model. Note this input has precedence over the input read from"
                 " the import source file.",
            default=None,
            required=False,
        )
        group_metadata.add_argument(
            "--add_file_name",
            help="Add original file name to EXIF. Note this input has precedence over the input read from the "
                 "import source file.",
            action="store_true",
            required=False,
        )
        group_metadata.add_argument(
            "--exclude_import_path",
            help="If local file name is to be added exclude import_path from the name.",
            action="store_true",
            required=False,
        )
        group_metadata.add_argument(
            "--exclude_path",
            help="If local file name is to be added, specify the path to be excluded.",
            default=None,
            required=False,
        )
        group_metadata.add_argument(
            "--add_import_date",
            help="Add import date.",
            action="store_true",
            required=False,
        )
        group_metadata.add_argument(
            "--windows_path",
            help="If local file name is to be added with --add_file_name, added it as a windows path.",
            action="store_true",
            required=False,
        )
        group_metadata.add_argument(
            "--orientation",
            help="Specify the image orientation in degrees. Note this might result in image rotation. "
                 "Note this input has precedence over the input read from the import source file.",
            choices=[0, 90, 180, 270],
            type=int,
            default=None,
            required=False,
        )
        group_metadata.add_argument(
            "--GPS_accuracy",
            help="GPS accuracy in meters. Note this input has precedence over the input read from "
                 "the import source file.",
            default=None,
            required=False,
        )
        group_metadata.add_argument(
            "--camera_uuid",
            help="Custom string used to differentiate different captures taken with the same camera make and model.",
            default=None,
            required=False,
        )
        group_metadata.add_argument(
            "--custom_meta_data",
            help='Add custom meta data to all images. Required format of input is a string, consisting of '
                 'the meta data name, type and value, separated by a comma for each entry, where entries are '
                 'separated by semicolon. Supported types are long, double, string, boolean, date. '
                 'Example for two meta data entries "random_name1,double,12.34;random_name2,long,1234"',
            default=None,
            required=False,
        )

        group_geotagging = parser.add_argument_group("process geotagging options")
        group_geotagging.add_argument(
            "--desc_path",
            help="Specify the path to store mapilio image descriptions as JSON. By default it is "
                 "{IMPORT_PATH}/mapilio_image_description.json",
            default=None,
            required=False,
        )
        group_geotagging.add_argument(
            "--geotag_source",
            help="Provide the source of date/time and GPS information needed for geotagging",
            action="store",
            choices=["exif", "gpx", "gopro_videos", "nmea"],
            default="exif",
            required=False,
        )
        group_geotagging.add_argument(
            "--geotag_source_path",
            help="Provide the path to the file source of date/time and GPS information needed for geotagging",
            action="store",
            default=None,
            required=False,
        )
        group_geotagging.add_argument(
            "--offset_time",
            default=0.0,
            type=float,
            help="time offset, in seconds, that will be added to your image timestamps",
            required=False,
        )
        group_geotagging.add_argument(
            "--offset_angle",
            default=0.0,
            type=float,
            help="camera angle offset, in degrees, that will be added to your image camera angles",
            required=False,
        )

        group_sequence = parser.add_argument_group("process sequence options")
        group_sequence.add_argument(
            "--cutoff_distance",
            default=600.0,
            type=float,
            help="maximum GPS distance in meters within a sequence",
            required=False,
        )
        group_sequence.add_argument(
            "--cutoff_time",
            default=60.0,
            type=float,
            help="maximum time interval in seconds within a sequence",
            required=False,
        )
        group_sequence.add_argument(
            "--interpolate_directions",
            help="perform interploation of directions",
            action="store_true",
            required=False,
        )
        group_sequence.add_argument(
            "--duplicate_distance",
            help="max distance for two images to be considered duplicates in meters",
            type=float,
            default=2,
            required=False,
        )
        group_sequence.add_argument(
            "--duplicate_angle",
            help="max angle for two images to be considered duplicates in degrees",
            type=float,
            default=5,
            required=False,
        )

    def run(self, vars_args: dict):

        process_import_meta_properties(
            **(
                {
                    k: v
                    for k, v in vars_args.items()
                    if k in inspect.getfullargspec(process_import_meta_properties).args
                }
            )
        )

        process_geotag_properties(
            **(
                {
                    k: v
                    for k, v in vars_args.items()
                    if k in inspect.getfullargspec(process_geotag_properties).args
                }
            )
        )

        process_sequence_properties(
            **(
                {
                    k: v
                    for k, v in vars_args.items()
                    if k in inspect.getfullargspec(process_sequence_properties).args
                }
            )
        )

        insert_MAPJson(
            **(
                {
                    k: v
                    for k, v in vars_args.items()
                    if k in inspect.getfullargspec(insert_MAPJson).args
                }
            )
        )
