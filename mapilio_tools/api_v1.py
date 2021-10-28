import os
import requests
from typing import Union


MAPILIO_GRAPH_API_ENDPOINT = os.getenv(
    "MAPILIO_GRAPH_API_ENDPOINT", "https://end.mapilio.com/api"
)
MAPILIO_GRAPH_API_ENDPOINT_DESCRIPTION = MAPILIO_GRAPH_API_ENDPOINT + '/function/mapilio/imagery_exif/upload'
MAPILIO_UPLOAD_ENDPOINT_ZIP = "https://image.mapilio.com/api/upload/zip"

def get_upload_token(email: str, password: str) -> dict:
    resp = requests.post(
        f"{MAPILIO_GRAPH_API_ENDPOINT}/login",
        json={"email": email, "password": password},
    )
    resp.raise_for_status()

    return resp.json()


def fetch_organization(
        user_access_token: str, organization_id: Union[int, str]
) -> requests.Response:
    resp = requests.get(
        f"{MAPILIO_GRAPH_API_ENDPOINT}/{organization_id}",
        params={
            "fields": ",".join(["slug", "description", "name"]),
        },
        headers={
            "Authorization": f"OAuth {user_access_token}",
        },
    )
    resp.raise_for_status()
    return resp
