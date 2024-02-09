import pandas as pd
import semver

import data_access

import streamlit as st


def get_source_connectors() -> pd.DataFrame:
    return data_access.get_connectors_from_registry("source")


def get_destination_connectors() -> pd.DataFrame:
    return data_access.get_connectors_from_registry("destination")


def filter_connectors(
    connectors: pd.DataFrame,
    connector_type: str | None = None,
    support_level: str | None = None,
    is_low_code: bool | None = None,
    is_using_base_image: bool | None = None,
    is_using_poetry: bool | None = None,
    is_on_pypi: bool | None = None,
    base_image_version: str | None = None,
    language: str | None = None,
) -> pd.DataFrame:
    if connector_type is not None:
        connectors = connectors[connectors["type"] == connector_type]
    if support_level is not None:
        if support_level not in SUPPORT_LEVELS:
            raise ValueError(f"Unknown support level: {support_level}")
        else:
            connectors = connectors[connectors["support_level"] == support_level]
    if language is not None:
        connectors = connectors[connectors["language"] == language]
    if is_low_code is not None:
        connectors = connectors[connectors["is_low_code"] == is_low_code]

    if is_using_base_image is not None:
        connectors = connectors[
            connectors["is_using_base_image"] == is_using_base_image
        ]

    if is_using_poetry is not None:
        connectors = connectors[connectors["is_using_poetry"] == is_using_poetry]

    if is_on_pypi is not None:
        connectors = connectors[connectors["is_on_pypi"] == is_on_pypi]

    if base_image_version is not None:
        connectors = connectors[connectors["base_image_version"] == base_image_version]

    return connectors


PYTHON_SOURCE_CONNECTORS = filter_connectors(
    get_source_connectors(), connector_type="source", language="python"
)
SUPPORT_LEVELS = list(PYTHON_SOURCE_CONNECTORS["support_level"].unique())

LATEST_BASE_IMAGE_VERSION = str(
    max(
        [
            semver.Version.parse(v)
            for v in PYTHON_SOURCE_CONNECTORS[
                PYTHON_SOURCE_CONNECTORS["base_image_version"].notnull()
            ]["base_image_version"].to_list()
        ]
    )
)
