from .upload import Command as UploadCommand
from .process_csv import Command as ProcessCSV


class Command:
    name = "image_and_csv_upload"
    help = "process panoramic images and upload to Mapilio"

    def add_basic_arguments(self, parser):
        ProcessCSV().add_basic_arguments(parser)
        UploadCommand().add_basic_arguments(parser)

    def run(self, args: dict):
        ProcessCSV().run(args)
        UploadCommand().run(args)
