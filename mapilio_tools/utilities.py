import subprocess
from typing import Dict, Union


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
    while True:
        line = process.stdout.readline()
        filtered_line = line.rstrip().decode('utf-8')
        if not line:
            break
        if 'Field Of View' in filtered_line:
            fov_str = filtered_line.split(':')[1].lstrip(' ')
            if not fov_str in ["Wide", "Unknown"]:
                dict_object['field_of_view'] = float(fov_str.replace('deg', ''))

        if 'Camera Model Name' in filtered_line:
            dict_object['device_make'] = filtered_line.split(':')[1].lstrip(' ')

        if 'Color Mode' in filtered_line:
            dict_object['device_model'] = filtered_line.split(':')[1].lstrip(' ')

        if 'Image Size' in filtered_line:
            dict_object['image_size'] = filtered_line.split(':')[1].lstrip(' ')

    return dict_object
