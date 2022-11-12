import subprocess
from typing import Dict, Union

from collections import ChainMap

__RULES__ = [{('hero7', 'wide', '4:3'): 122.6}, {('hero7', 'wide', '16:9'): 118.2},
             {('hero7', 'linear', '4:3'): 86.7}, {('hero7', 'linear', '16:9'): 87.6},
             {('hero8', 'wide', '4:3'): 122.6}, {('hero8', 'wide', '16:9',): 118.2},
             {('hero8', 'linear', '4:3'): 86.7}, {('hero7', 'linear', '4:3'): 86.0},
             {('hero7', 'linear', '4:3'): 86.7}, {('hero7', 'linear', '16:9'): 85.8},
             {('hero7', 'linear', '16:9'): 87.6}, {('hero7', 'linear', '16:9'): 50.0},
             {('hero7', 'linear', '16:9'): 51.0},
             {('hero8', 'narrow', '4:3'): 68.0}, {('hero8', 'unknown (x)', '16:9'): 122.6},
             {('hero8', 'linear', '16:9'): 85.8}, {('hero8', 'linear', '16:9'): 87.6},
             {('hero8', 'narrow', '16:9'): 68.0}, {('gopro', 'super view', '16:9'): 99.0},
             {('hero9 black', 'wide', '4:3'): 122.0}, {('gopro', 'linear', '16:9'): 75.0},
             {('hero9 black', 'linear', '4:3'): 92.0}, {('gopro', 'linear', '16:9'): 87.0},
             {('hero9 black', 'narrow', '4:3'): 73.0}, {('gopro', 'linear', '16:9'): 92.0},
             {('hero9 black', 'unknown (x)', '16:9'): 121.0}, {('gopro', 'wide', '16:9'): 92.0},
             {('hero9 black', 'wide', '16:9'): 118.0}, {('gopro', 'wide', '16:9'): 109.0},
             {('hero9 black', 'linear', '16:9'): 92.0}, {('gopro', 'wide', '16:9'): 118.0},
             {('hero9 black', 'narrow', '16.9'): 73.0}, {('gopro', 'linear + horizon levelling', '16:9'): 75.0},
             {('gopro max', 'unknown (x)', '4:3'): 148.8}, {('gopro', 'linear + horizon levelling', '16:9'): 87.0},
             {('gopro max', 'wide', '4:3'): 122.6}, {('gopro max', 'linear', '4:3'): 86.0},
             {('gopro max', 'narrow', '4:3'): 68.0}, {('gopro', 'narrow', '16:9'): 75.0},
             {('gopro max', 'unknown (x)', '16:9'): 148.8}, {('gopro', 'narrow', '16:9'): 67.0},
             {('gopro max', 'wide', '16:9'): 122.6}, {('gopro max', 'linear', '16:9'): 73.0},
             {('gopro max', 'narrow', '16:9'): 68.0}, {('gopro', 'unknown (x)', '4:3'): 94.0},
             {('gopro', 'unknown (x)', '16:9'): 121.0}, {('gopro', 'wide', '4:3'): 92.0},
             {('gopro', 'wide', '4:3'): 113.0}, {('gopro', 'wide', '4:3'): 122.0}, {('gopro', 'linear', '4:3'): 75.0},
             {('gopro', 'linear', '4:3'): 87.0}, {('gopro', 'linear', '4:3'): 92.0},
             {('gopro', 'linear + horizon levelling', '4:3'): 75.0},
             {('gopro', 'linear + horizon levelling', '4:3'): 87.0}, {('gopro', 'narrow', '4:3'): 73.0},
             {('gopro', 'narrow', '4:3'): 67.0},
             {('gopro', 'max superview', '16:9'): 128.0}, {('gopro', 'max superview', '16:9'): 140.0},
             {('gopro', 'wide', '16:9'): 109.0}, {('gopro', 'wide', '16:9'): 122.0},
             {('gopro', 'linear', '16:9'): 88.0},
             {('gopro', 'linear', '16:9'): 86.0}, {('gopro', 'max superview', '4:3'): 128.0},
             {('gopro', 'max superview', '4:3'): 140.0},
             {('gopro', 'wide', '4:3'): 113.0}, {('gopro', 'wide', '4:3'): 122.0}, {('gopro', 'linear', '4:3'): 88.0},
             {('gopro', 'linear', '4:3'): 92.0}, {('gopro', 'wide', '169:95'): 122.0},
             {('hero8', 'wide', '16:9',): 62.2}, {('hero8', 'linear', '16:9',): 50.0},
             {('hero8', 'linear', '16:9',): 51.0}, {('hero8', 'linear', '4:3',): 51.0},
             {('hero8', 'linear', '4:3',): 50.0}, {('gopro max', 'max superview', '4:3'): 148.8},
             {('gopro max', 'max superview', '16:9'): 148.8}, {('gopro max', 'wide', '4:3'): 122.6},
             {('gopro max', 'wide', '16:9'): 122.6}, {('gopro max', 'linear', '4:3'): 86.0},
             {('gopro max', 'linear', '16:9'): 86.0}, {('gopro max', 'narrow', '4:3'): 68.0},
             {('gopro max', 'narrow', '16:9'): 68.0}

             ]
"""
Source:
https://gopro.com/help/articles/question_answer/hero7-field-of-view-fov-information?sf96748270=1
https://community.gopro.com/s/article/HERO8-Black-Digital-Lenses-formerly-known-as-FOV?language=en_US
https://community.gopro.com/s/article/HERO9-Black-Digital-Lenses-FOV-Information?language=en_US
https://community.gopro.com/s/article/MAX-Digital-Lenses-formerly-known-as-FOV?language=en_US
"""


def find_fov2(model, mode, asp_rat):
    result = ChainMap(*__RULES__)
    return result[(model, mode, asp_rat)]


def calculate_aspect_ratio(image_size: str) -> str:
    """

    Args:
        image_size: "1920x1080" format

    Returns:
        "16:9"
    """
    width, height = int(image_size.split("x")[0]), int(image_size.split("x")[1]),

    def gcd(a, b):
        """En büyük ortak böleni bulan fonksiyon"""
        return a if b == 0 else gcd(b, a % b)

    r = gcd(width, height)
    x = int(width / r)
    y = int(height / r)

    return f"{x}:{y}"


def get_exiftool_specific_feature(video_or_image_path: str) -> Dict[str, Union[None, str, float]]:
    """

    Args:
        video_or_image_path:

    Returns:

    """

    process = subprocess.Popen(["exiftool", video_or_image_path], stdout=subprocess.PIPE)
    dict_object = {
        'field_of_view': None,
        'device_make': None,
        'device_model': None,
        'image_size': None,
        'roll': None,
        'yaw': None,
        'pitch': None,
        'carSpeed': None,
        'megapixels': None

    }
    fov_str = None
    fov_deg = None
    gyroscope = {"gyroscope": {"x": 3,
                               "y": 4,
                               "z": 5
                               }}
    while True:
        try:
            line = process.stdout.readline()

            filtered_line = (line.rstrip().decode('utf-8')).lower()

            if not line:  # noqa
                break
            if 'megapixels' in filtered_line:
                dict_object['megapixels'] = float(filtered_line.split(':')[1].lstrip(' '))

            if 'yaw' in filtered_line:
                dict_object['yaw'] = float(filtered_line.split(':')[1].lstrip(' '))

            if 'pitch' in filtered_line:
                dict_object['pitch'] = float(filtered_line.split(':')[1].lstrip(' '))

            if 'roll' in filtered_line:
                dict_object['roll'] = float(filtered_line.split(':')[1].lstrip(' '))

            if 'carspeed' in filtered_line:
                dict_object['carSpeed'] = float(filtered_line.split(':')[1].lstrip(' '))

            if 'field of view' in filtered_line:
                fov_str = filtered_line.split(':')[1].lstrip(' ')
                dict_object['field_of_view'] = fov_str

            elif 'camera elevation angle' in filtered_line:
                fov_deg = float(filtered_line.split(':')[1].lstrip(' '))
            if 'color mode' in filtered_line:
                dict_object['device_make'] = filtered_line.split(':')[1].lstrip(' ')
            elif 'make' in filtered_line:
                dict_object['device_make'] = filtered_line.split(':')[1].lstrip(' ')
            if 'camera model name' in filtered_line:
                dict_object['device_model'] = filtered_line.split(':')[1].lstrip(' ')
            if 'image size' in filtered_line:
                dict_object['image_size'] = filtered_line.split(':')[1].lstrip(' ')
        except TypeError:
            raise f"Exif data does not Exist !" \
                  f"Please remove this video file {video_or_image_path}"

    if dict_object['field_of_view'] and "deg" in dict_object['field_of_view']:
        dict_object['field_of_view'] = float(dict_object['field_of_view'].replace('deg', ''))
        return dict_object
    if isinstance(fov_deg, float):
        dict_object['field_of_view'] = fov_deg
        return dict_object
    if isinstance(fov_str, str):
        aspect_ratio = calculate_aspect_ratio(dict_object['image_size'])
        dict_object['field_of_view'] = find_fov2(dict_object['device_make'],
                                                 dict_object['field_of_view'],
                                                 aspect_ratio)
        return dict_object


def photo_uuid_generate(user_email: str, descs: list) -> list:
    """

    Args:
        user_email:
        descs: descriptions

    Returns:
        add new column as name "Id" create hash
    """
    import hashlib

    for desc in descs[:-1]:
        code = f'{user_email}--{desc["captureTime"]}'
        hash_object = hashlib.md5(code.encode())
        desc['photoUuid'] = hash_object.hexdigest()

    return descs
