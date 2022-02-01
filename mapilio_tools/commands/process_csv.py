import inspect
from ..process_csv_to_description import process_csv_to_description


class Command:
    name = "process_csv"
    help = "create panorama csv to description format to Mapilio"

    def add_basic_arguments(self, parser):
        group = parser.add_argument_group("upload options")
        group.add_argument(
            "--user_name", help="Upload to which Mapilio user account", required=False
        )
        group.add_argument(
            "--csv_path",
            help="Specify organization user name",
            default=None,
            required=False,
        )

    def run(self, vars_args: dict):

        process_csv_to_description(
            **(
                {
                    k: v
                    for k, v in vars_args.items()
                    if k in inspect.getfullargspec(process_csv_to_description).args
                }
            )
        )