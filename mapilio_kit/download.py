import time

from tqdm import tqdm
from .download_config import select_quality
from .upload import fetch_user_items
import json
import requests
import logging
import os.path
import urllib.request
import typing as T
import cv2
from .api_v1 import URL_Sequences, URL_CDN, URL_Images

LOG = logging.getLogger(__name__)

MAX_LIMIT = 999999


def download(
        organization_key: str,
        project_key: str,
        download_path: str,
        user_name: str,
) -> None:
    """
    Args:
        organization_key: your organization key, you can get your dashboard
        project_key: your organization key, you can get your dashboard
        download_path: where will be saving path
        user_name: user authenticate

    Returns:

    """
    get_quality = select_quality()
    user_items = fetch_user_items(user_name, organization_key)

    sequences = get_seqeuence_and_image_detail_request(
        organization_key=organization_key,
        project_key=project_key,
        bearer=user_items['user_upload_token'],
        req="sequence"
    )
    save_base_path = os.path.join(download_path, "Mapilio", organization_key, project_key)
    for seqeunce in sequences:
        images_details = get_seqeuence_and_image_detail_request(
            organization_key=organization_key,
            project_key=project_key,
            bearer=user_items['user_upload_token'],
            sequence_uuid=seqeunce['sequence_uuid'],
            req="image_detail"
        )
        end_save_path = os.path.join(save_base_path, seqeunce['sequence_uuid'])
        for image_detail in tqdm(images_details, desc="Downloading"):
            save_image(
                uploaded_hash=image_detail['uploaded_hash'],
                filename=image_detail['filename'],
                end_save_path=end_save_path,
                quality=get_quality
            )
    LOG.info("All Sequences Has Downloaded!")


def get_seqeuence_and_image_detail_request(
        organization_key: str,
        project_key: str,
        bearer: str,
        sequence_uuid: T.Optional[str] = None,
        req: str = "sequence"
) -> json:
    """
    This method get SequenceUUID according to organization key and project key
    Args:
        organization_key:
        project_key:
        bearer: user auth bearer key
        sequence_uuid: each packet unique id optional
        req: sequence or image key value

    Returns: json data

    """
    payload = json.dumps({
        "options": {
            "parameters": {
                "organization_key": organization_key,
                "project_key": project_key,
                "sequence_uuid": "None" if req == "sequence" else sequence_uuid
            },
            "limit": MAX_LIMIT
        }
    })
    headers = {
        'Authorization': f'Bearer {bearer}',
        'Content-Type': 'application/json'
    }
    URL = URL_Sequences if req == "sequence" else URL_Images
    response = requests.request("GET", URL, headers=headers, data=payload)
    response = json.loads(response.text)

    return response['data']

def url_to_image(url: str):
    """
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    :param url:
    :return:
    """
    import requests
    import numpy as np
    number_of_tries = 3
    for _ in range(number_of_tries):
        try:
            resp = requests.get(url, stream=True).raw
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            return image
        except Exception:
            time.sleep(2)
    else:
        raise


def save_image(
        uploaded_hash: str,
        filename: str,
        end_save_path: str,
        quality: str
) -> None:
    """
    Args:
        uploaded_hash:
        filename:
        end_save_path:
        quality: image quality such as 240, 480, 1080

    Returns:

    """
    image_full_url = os.path.join(URL_CDN, uploaded_hash, filename, quality)
    image_path = os.path.join(end_save_path, filename)

    if os.path.exists(image_path):
        pass
        # LOG.info(f"The image already existed!")
    else:
        if not os.path.exists(end_save_path):
            # LOG.info(f"The Folder does not exist! -->> New Folder is creating")
            os.makedirs(end_save_path)
        image = url_to_image(image_full_url)
        cv2.imwrite(image_path + filename, image)
