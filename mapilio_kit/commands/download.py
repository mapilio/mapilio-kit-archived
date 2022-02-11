import inspect

from ..download import download


class Command:
    name = "download"
    help = "Download command from your uploaded images via API"

    def add_basic_arguments(self, parser):
        group = parser.add_argument_group("upload options")

        group.add_argument(
            "--organization_key",
            help="Specify organization key",
            default=None,
            required=True,
        )
        group.add_argument(
            "--project_key",
            help="Specify project key",
            default=None,
            required=True,
        )

    def run(self, vars_args: dict):
        download(
            **(
                {
                    k: v
                    for k, v in vars_args.items()
                    if k in inspect.getfullargspec(download).args
                }
            )
        )