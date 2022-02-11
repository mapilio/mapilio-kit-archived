from .api_v1 import MAPILIO_GRAPH_API_ENDPOINT_DOWNLOAD
from .download_config import QUALITY


def download(
        organization_key: str,
        project_key: str,
        download_path: str,
):
    """

    :param organization_key: your organization key, you can get your dashboard
    :param project_key: your organization key, you can get your dashboard
    :param download_path: where will be saving path
    :param quality: which quality will be downloading
    :return:
    """
    print(organization_key)
    print("\n")
    print(project_key)
    print("\n")
    print(download_path)
    print("\n")
    print(QUALITY)
