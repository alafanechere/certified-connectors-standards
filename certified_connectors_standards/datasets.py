import semver

import data_access

SOURCE_CONNECTORS = data_access.get_connectors_from_registry("source")
PYTHON_CONNECTORS = SOURCE_CONNECTORS[SOURCE_CONNECTORS["language"] == "python"]
CERTIFIED_PYTHON_SOURCE_CONNECTORS = PYTHON_CONNECTORS[
    PYTHON_CONNECTORS["support_level"] == "certified"
]
CONNECTORS_NOT_USING_BASE_IMAGE = CERTIFIED_PYTHON_SOURCE_CONNECTORS[
    ~CERTIFIED_PYTHON_SOURCE_CONNECTORS["is_using_base_image"]
][["technical_name"]].rename(
    columns={"technical_name": "Connectors not using our base image"}
)
LATEST_BASE_IMAGE_VERSION = str(
    max(
        [
            semver.Version.parse(v)
            for v in CERTIFIED_PYTHON_SOURCE_CONNECTORS["base_image_version"].to_list()
            if v
        ]
    )
)
CONNECTORS_BASE_IMAGE_VERSION = CERTIFIED_PYTHON_SOURCE_CONNECTORS[
    CERTIFIED_PYTHON_SOURCE_CONNECTORS["is_using_base_image"]
][["technical_name", "base_image_version"]].rename(
    columns={"technical_name": "Connector", "base_image_version": "Base image version"}
)
CONNECTORS_NOT_USING_LATEST_BASE_IMAGE_VERSION = CERTIFIED_PYTHON_SOURCE_CONNECTORS[
    ~CERTIFIED_PYTHON_SOURCE_CONNECTORS["base_image_version"].isin(
        [str(LATEST_BASE_IMAGE_VERSION)]
    )
][["technical_name", "base_image_version"]].rename(
    columns={"technical_name": "Connector", "base_image_version": "Base image version"}
)
LOW_CODE_CONNECTORS = CERTIFIED_PYTHON_SOURCE_CONNECTORS[
    CERTIFIED_PYTHON_SOURCE_CONNECTORS["is_low_code"]
][["technical_name"]].rename(
    columns={"technical_name": "Certified low-code connectors"}
)
NON_LOW_CODE_CONNECTORS = CERTIFIED_PYTHON_SOURCE_CONNECTORS[
    ~CERTIFIED_PYTHON_SOURCE_CONNECTORS["is_low_code"]
][["technical_name"]].rename(columns={"technical_name": "Non low-code connectors"})
CONNECTORS_USING_POETRY = CERTIFIED_PYTHON_SOURCE_CONNECTORS[
    CERTIFIED_PYTHON_SOURCE_CONNECTORS["is_using_poetry"]
][["technical_name"]].rename(columns={"technical_name": "Connectors using poetry"})
CONNECTORS_NOT_USING_POETRY = CERTIFIED_PYTHON_SOURCE_CONNECTORS[
    ~CERTIFIED_PYTHON_SOURCE_CONNECTORS["is_using_poetry"]
][["technical_name"]].rename(columns={"technical_name": "Connectors not using poetry"})
CONNECTORS_ON_PYPI = CERTIFIED_PYTHON_SOURCE_CONNECTORS[
    CERTIFIED_PYTHON_SOURCE_CONNECTORS["is_on_pypi"]
][["technical_name"]].rename(columns={"technical_name": "Connectors on PyPi"})
CONNECTORS_NOT_ON_PYPI = CERTIFIED_PYTHON_SOURCE_CONNECTORS[
    ~CERTIFIED_PYTHON_SOURCE_CONNECTORS["is_on_pypi"]
][["technical_name"]].rename(columns={"technical_name": "Connectors not on PyPi"})
