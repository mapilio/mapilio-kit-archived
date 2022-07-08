import argparse
import logging
import sys

from . import VERSION
from .commands import authenticate
from .commands import process
from .commands import process_and_upload
from .commands import sample_video
from .commands import upload
from .commands import video_process
from .commands import video_process_and_upload
from .commands import zip
from .commands import image_and_csv_upload
from .commands import download
from .commands import gopro_360max

# do not use __name__ here is because if you run tools as a module, __name__ will be "__main__"
LOG = logging.getLogger("mapilio_kit")

def logger_configuration(logger: logging.Logger, level, stream=None) -> None:
    formatter = logging.Formatter("%(asctime)s - %(levelname)-6s - %(message)s")
    handler = logging.StreamHandler(stream)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def general_arguments(parser, command):
    if command == "authenticate":
        return
    if command == "gopro360max_process":
        return
    if command in ["sample_video", "video_process", "video_process_and_upload"]:
        parser.add_argument(
            "video_import_path",
            help="Path to a video or directory with one or more video files.",
        )
        parser.add_argument(
            "import_path",
            help='Path to where the images from video sampling will be saved. If not specified, it will default to '
                 '"mapilio_sampled_video_frames" under your video import path',
            nargs="?",
        )
        parser.add_argument(
            "--skip_subfolders",
            help="Skip all subfolders and import only the images in the given video_import_path",
            action="store_true",
            default=False,
            required=False,
        )
    elif command in ["upload", "image_and_csv_upload"]:
        parser.add_argument(
            "import_path",
            help="Path to your images",
        )
    elif command in ["download"]:
        parser.add_argument(
            "download_path",
            help="Path to your images",
        )
    elif command in ["zip"]:
        parser.add_argument(
            "import_path",
            help="Path to your images",
        )
        parser.add_argument(
            "zip_dir",
            help="Path to store zipped images",
        )
    else:
        parser.add_argument(
            "import_path",
            help="Path to your images",
        )
        parser.add_argument(
            "--skip_subfolders",
            help="Skip all subfolders and import only the images in the given import_path",
            action="store_true",
            default=False,
            required=False,
        )

def main():
    mapilio_tools_commands = [
        process,
        zip,
        upload,
        process_and_upload,
        sample_video,
        video_process,
        video_process_and_upload,
        authenticate,
        image_and_csv_upload,
        download,
        gopro_360max
    ]
    parser = argparse.ArgumentParser(
        "mapilio_kit",
    )
    parser.add_argument(
        "--version",
        help="show the version of mapilio tools and exit",
        action="version",
        version=f"Mapilio tools version : {VERSION}",
    )
    parser.add_argument(
        "--verbose",
        help="Show verbose",
        action="store_true",
        default=False,
        required=False,
    )

    all_commands = [module.Command() for module in mapilio_tools_commands]  # all processing initializing

    subparsers = parser.add_subparsers(
        description="please choose one of the available subcommands",
    )
    for command in all_commands:  # sequence commands
        cmd_parser = subparsers.add_parser(
            command.name, help=command.help, conflict_handler="resolve"
        )
        general_arguments(cmd_parser, command.name)
        command.add_basic_arguments(cmd_parser)  # commands args initialing
        cmd_parser.set_defaults(func=command.run)  # run the processing

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger_configuration(LOG, sys.stderr)
    LOG.setLevel(log_level)
    LOG.debug(f"argparse vars: {vars(args)}")
    args.func(vars(args))

if __name__ == "__main__":
    main()