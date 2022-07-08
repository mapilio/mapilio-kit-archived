import inspect

from ..gps_from_gopro360 import gopro360max_stitch


class Command:
    name = "gopro360max_process"
    help = "Stitching GoProMax output format panoramic images"

    def add_basic_arguments(self, parser):
        group = parser.add_argument_group("upload options")
        group.add_argument('--video-file', '-vf', type=str, help='video file path', default=None)
        group.add_argument('--output-folder', '-of', type=str, help='output folder', default='/tmp/test')
        group.add_argument('--frame-rate', '-fps', type=int, help='how many frames to extract per frame', default=1)
        group.add_argument('--quality', '-q', type=int, help='frame extraction quality', default=2)
        group.add_argument('--bin-dir', '-b', type=str, help='directory that contains the MAX2spherebatch exec',
                           default='bin/')

    def run(self, vars_args: dict):
        gopro360max_stitch(
            **(
                {
                    k: v
                    for k, v in vars_args.items()
                    if k in inspect.getfullargspec(gopro360max_stitch).args
                }
            )
        )