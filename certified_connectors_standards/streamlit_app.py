import streamlit as st
from consts import OSS_REGISTRY_URL, DATA_REFRESH_INTERVAL
from datasets import (
    CONNECTORS_NOT_ON_PYPI,
    CONNECTORS_NOT_USING_BASE_IMAGE,
    CONNECTORS_NOT_USING_LATEST_BASE_IMAGE_VERSION,
    CONNECTORS_NOT_USING_POETRY,
    CONNECTORS_ON_PYPI,
    CONNECTORS_USING_POETRY,
    LATEST_BASE_IMAGE_VERSION,
    LOW_CODE_CONNECTORS,
    NON_LOW_CODE_CONNECTORS,
)
from metrics import CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS


st.title(
    "👮 Tracking compliance of our certified Python source connectors to our standards"
)
st.markdown(
    """This app helps tracking our progress in enforcing a set of standards on our certified Python connectors:
- **Adopting the low-code CDK**: to reduce the maintenance burden and improve the connectors reliability.
- **Adopting our base image**: to improve build process consistency and security of our connectors.
- **Adopting `poetry`**: to get reproducible builds (by locking dependencies) and avoid unexpected regression.
- **Publishing to PyPi**: to make connectors available to `airbyte-lib`.
"""
)

low_code_progress, base_image_progress, poetry_progress, pypi_progress = st.columns(
    (1, 1, 1, 1)
)
low_code_progress.metric(
    "Low-code migration",
    f"{round(CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.migration_to_low_code_progress * 100)}%  🧩",
)
base_image_progress.metric(
    "Base image migration",
    f"{round(CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.migration_to_base_image_progress * 100)}%  🐳",
)
poetry_progress.metric(
    "Poetry migration",
    f"{round(CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.migration_to_poetry_progress * 100)}%  📜",
)
pypi_progress.metric(
    "PyPi migration",
    f"{round(CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.migration_to_pypi_progress * 100)}%  📦",
)

st.header("Details")

low_code_tab, base_image_tab, poetry_tab, pypi_tab = st.tabs(
    ["Low-code CDK adoption", "Base image adoption", "Poetry adoption", "PyPi adoption"]
)

with low_code_tab:
    left, middle, right = st.columns((1, 1, 1))
    left.metric(
        "Migration progress",
        f"{round(CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.migration_to_low_code_progress * 100)}%  🎉",
    )
    middle.metric(
        "Certified low-code connectors",
        f"{CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.num_with_low_code} 🟢",
    )
    right.metric(
        "Non low-code connectors",
        f"{CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.num_without_low_code} 🔴",
    )
    st.dataframe(LOW_CODE_CONNECTORS, use_container_width=True, hide_index=True)
    st.dataframe(NON_LOW_CODE_CONNECTORS, use_container_width=True, hide_index=True)

with base_image_tab:
    left, middle, right = st.columns((1, 1, 1))
    left.metric(
        "Migration progress",
        f"{round(CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.migration_to_base_image_progress * 100)}%  🎉",
    )
    middle.metric(
        "Using our base image",
        f"{CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.num_with_base_image} 🟢",
    )
    right.metric(
        "Not using our base image",
        f"{CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.num_without_base_image} 🔴",
    )
    st.dataframe(
        CONNECTORS_NOT_USING_BASE_IMAGE, use_container_width=True, hide_index=True
    )
    st.metric("Latest base image version", LATEST_BASE_IMAGE_VERSION)
    st.subheader(
        f"{len(CONNECTORS_NOT_USING_LATEST_BASE_IMAGE_VERSION)} connectors not using the latest base image version"
    )
    st.dataframe(
        CONNECTORS_NOT_USING_LATEST_BASE_IMAGE_VERSION,
        use_container_width=True,
        hide_index=True,
    )

with poetry_tab:
    left, middle, right = st.columns((1, 1, 1))
    left.metric(
        "Migration progress",
        f"{round(CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.migration_to_poetry_progress * 100)}%  🎉",
    )
    middle.metric(
        "Using poetry",
        f"{CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.num_with_poetry} 🟢",
    )
    right.metric(
        "Not using poetry",
        f"{CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.num_without_poetry} 🔴",
    )
    st.dataframe(CONNECTORS_USING_POETRY, use_container_width=True, hide_index=True)
    st.dataframe(CONNECTORS_NOT_USING_POETRY, use_container_width=True, hide_index=True)

with pypi_tab:
    left, middle, right = st.columns((1, 1, 1))
    left.metric(
        "Migration progress",
        f"{round(CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.migration_to_pypi_progress * 100)}%  🎉",
    )
    middle.metric(
        "On PyPi", f"{CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.num_on_pypi} 🟢"
    )
    right.metric(
        "Not on PyPi",
        f"{CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS.num_not_on_pypi} 🔴",
    )
    st.dataframe(CONNECTORS_ON_PYPI, use_container_width=True, hide_index=True)
    st.dataframe(CONNECTORS_NOT_ON_PYPI, use_container_width=True, hide_index=True)

st.markdown(
    f"""
#### Datasource
All these metrics are computed from the [Airbyte OSS registry]({OSS_REGISTRY_URL}) and by direct access to code files using `raw.github.com`.

The data is refreshed every {str(DATA_REFRESH_INTERVAL)} hours to ensure the most accurate information is displayed.

Reach out to [@alafanechere](https://github.com/alafanechere) for feedback or question about this app!
"""
)
