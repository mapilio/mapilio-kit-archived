import subprocess
from typing import Dict, Union

from collections import ChainMap

__RULES__ = [{('HERO7', 'Wide', '4:3'): 122.6}, {('HERO7', 'Wide ', '16:9'): 188.2},
             {('HERO7', 'Linear', '4:3'): 86.7}, {('HERO7', 'Linear', '16:9'): 85.8},
             {('HERO8', 'Unknown (X)', '16:9'): 122.6}, {('HERO8', 'Wide', '16:9'): 118.2},
             {('HERO8', 'Wide', '4:3'): 122.6}, {('HERO8', 'Linear', '16:9'): 85.8},
             {('HERO8', 'Linear', '4:3'): 86.0}, {('HERO8', 'Narrow', '16:9'): 68.0},
             {('HERO8', 'Narrow', '4:3'): 68.0}, {('HERO9', 'Wide', '16:9'): 118.0},
             {('HERO9 Black', 'Linear', '16:9'): 92.0}, {('HERO9 Black', 'Super View', '16:9'): 121.0},
             {('HERO9 Black', 'Wide', '4:3'): 122.0}, {('HERO9 Black', 'Linear', '4:3'): 92.0},
             {('HERO9 Black', 'Narrow', '16:9'): 73.0}, {('HERO9 Black', 'Narrow', '4:3'): 73.0},
             {('GoPro Max', 'Wide', '16:9'): 118.0}, {('GoPro Max', 'Linear', '16:9'): 92.0},
             {('GoPro Max', 'Unknown (X)', '16:9'): 121.0}, {('GoPro Max', 'Narrow', '16:9'): 73.0}]


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
        'image_size': None
    }
    fov_str = None
    fov_deg = None
    while True:
        line = process.stdout.readline()
        filtered_line = line.rstrip().decode('utf-8')
        if not line: # noqa
            break
        if 'Field Of View' in filtered_line:
            fov_str = filtered_line.split(':')[1].lstrip(' ')
            dict_object['field_of_view'] = fov_str

        elif 'Camera Elevation Angle' in filtered_line:
            fov_deg = float(filtered_line.split(':')[1].lstrip(' '))

        if 'Camera Model Name' in filtered_line:
            dict_object['device_make'] = filtered_line.split(':')[1].lstrip(' ')

        if 'Color Mode' in filtered_line:
            dict_object['device_model'] = filtered_line.split(':')[1].lstrip(' ')

        if 'Image Size' in filtered_line:
            dict_object['image_size'] = filtered_line.split(':')[1].lstrip(' ')

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
