import re
import pandas as pd
import requests
import streamlit as st

from consts import OSS_REGISTRY_URL, DATA_REFRESH_INTERVAL
from models import Connector

DOCKER_IMAGE_VERSION_PATTERN = r":([0-9]+\.[0-9]+\.[0-9]+)@"


def check_if_poetry_lockfile_exists(connector_technical_name: str) -> bool:
    response = requests.get(
        f"https://raw.githubusercontent.com/airbytehq/airbyte/master/airbyte-integrations/connectors/{connector_technical_name}/poetry.lock"
    )
    return response.status_code == 200


@st.cache_data(ttl=DATA_REFRESH_INTERVAL, show_spinner="Fetching data from the connector registry and Github...")
def get_connectors_from_registry(connector_type: str) -> pd.DataFrame:
    progress_bar = st.progress(
        0, text=f"Loading {connector_type} connectors from registry..."
    )

    if not connector_type in ["source", "destination"]:
        raise ValueError("connector_type must be either 'source' or 'destination'")

    registry = requests.get(OSS_REGISTRY_URL).json()
    connectors = []
    for i, entry in enumerate(registry[f"{connector_type}s"]):
        progress_bar.progress(i / len(registry[f"{connector_type}s"]))
        is_using_base_image = False
        base_image_version = None
        if base_image := entry.get("connectorBuildOptions", {}).get("baseImage", False):
            is_using_base_image = True
            base_image_version = re.search(
                DOCKER_IMAGE_VERSION_PATTERN, base_image
            ).group(1)
        connector_technical_name = entry["dockerRepository"].split("/")[-1]
        connectors.append(
            Connector(
                type_=connector_type,
                technical_name=connector_technical_name,
                support_level=entry.get("supportLevel", "community"),
                is_on_pypi=entry.get("remoteRegistries", {})
                .get("pypi", {})
                .get("enabled", False),
                tags=entry.get("tags", []),
                is_using_base_image=is_using_base_image,
                base_image_version=base_image_version,
                is_using_poetry=check_if_poetry_lockfile_exists(
                    connector_technical_name
                ),
            ).to_dict()
        )
    progress_bar.empty()
    return pd.DataFrame(connectors)
