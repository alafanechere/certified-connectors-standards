import pandas as pd
import streamlit as st


from consts import OSS_REGISTRY_URL, DATA_REFRESH_INTERVAL
from metrics import ConnectorMetrics


try:
    from datasets import (
        filter_connectors,
        get_latest_base_image_version,
        SUPPORT_LEVELS,
        get_python_source_connectors,
    )
except Exception as e:
    st.error(f"An error occurred while fetching data: {e}")
    raise e

PYTHON_SOURCE_CONNECTORS = get_python_source_connectors()
LATEST_BASE_IMAGE_VERSION = get_latest_base_image_version()

SUPPORT_LEVELS_CONFIG = {
    "certified": {
        "title": "Certified 🏅",
        "description": "Connectors that are certified by Airbyte.",
        "data": filter_connectors(PYTHON_SOURCE_CONNECTORS, support_level="certified"),
    },
    "community": {
        "title": "Community 🍼",
        "description": "Connectors that are community maintained.",
        "data": filter_connectors(PYTHON_SOURCE_CONNECTORS, support_level="community"),
    },
}

for support_level in SUPPORT_LEVELS_CONFIG.keys():
    if support_level not in SUPPORT_LEVELS:
        raise ValueError(f"Unknown support level: {support_level}")


def print_adoption(connectors: pd.DataFrame):
    if support_level not in SUPPORT_LEVELS:
        st.error(f"Unknown support level: {support_level}")
        return

    adoption_metrics = ConnectorMetrics(connectors)
    low_code_subset = filter_connectors(connectors, is_low_code=True)
    non_low_code_subset = filter_connectors(connectors, is_low_code=False)

    base_image_subset = filter_connectors(connectors, is_using_base_image=True)
    non_base_image_subset = filter_connectors(connectors, is_using_base_image=False)
    non_latest_version_subset = base_image_subset[
        base_image_subset["base_image_version"] != LATEST_BASE_IMAGE_VERSION
    ]

    poetry_subset = filter_connectors(connectors, is_using_poetry=True)
    non_poetry_subset = filter_connectors(connectors, is_using_poetry=False)

    pypi_subset = filter_connectors(connectors, is_on_pypi=True)
    non_pypi_subset = filter_connectors(connectors, is_on_pypi=False)

    low_code_tab, base_image_tab, poetry_tab, pypi_tab = st.tabs(
        ["Low-code CDK 🧩", "Base image 🐳", "Poetry 📜", "PyPi 📦"]
    )

    with low_code_tab:
        left, middle, right = st.columns((1, 1, 1))
        left.metric(
            "Migration progress",
            f"{round(adoption_metrics.migration_to_low_code_progress * 100)}%  🎉",
        )
        middle.metric(
            "Low-code connectors",
            f"{adoption_metrics.num_with_low_code} 🟢",
        )
        right.metric(
            "Non low-code connectors",
            f"{adoption_metrics.num_without_low_code} 🔴",
        )
        st.dataframe(
            low_code_subset[["technical_name"]],
            use_container_width=True,
            hide_index=True,
            column_config={"technical_name": "Low-code connectors"},
        )
        st.dataframe(
            non_low_code_subset[["technical_name"]],
            use_container_width=True,
            hide_index=True,
            column_config={"technical_name": "Non Low-code connectors"},
        )

    with base_image_tab:
        left, middle, right = st.columns((1, 1, 1))
        left.metric(
            "Migration progress",
            f"{round(adoption_metrics.migration_to_base_image_progress * 100)}%  🎉",
        )
        middle.metric(
            "Using our base image",
            f"{adoption_metrics.num_with_base_image} 🟢",
        )
        right.metric(
            "Not using our base image",
            f"{adoption_metrics.num_without_base_image} 🔴",
        )

        st.dataframe(
            non_base_image_subset[["technical_name"]],
            use_container_width=True,
            hide_index=True,
            column_config={"technical_name": "Connectors not using our base image"},
        )

        if len(non_latest_version_subset) > 0:
            st.metric("Latest base image version", LATEST_BASE_IMAGE_VERSION)
            st.subheader(
                f"{len(non_latest_version_subset)} connectors not using the latest base image version"
            )
            st.dataframe(
                non_latest_version_subset[["technical_name", "base_image_version"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "technical_name": "Connectors not using the latest base image version",
                    "base_image_version": "Base image version",
                },
            )

    with poetry_tab:
        left, middle, right = st.columns((1, 1, 1))
        left.metric(
            "Migration progress",
            f"{round(adoption_metrics.migration_to_poetry_progress * 100)}%  🎉",
        )
        middle.metric(
            "Using poetry",
            f"{adoption_metrics.num_with_poetry} 🟢",
        )
        right.metric(
            "Not using poetry",
            f"{adoption_metrics.num_without_poetry} 🔴",
        )
        st.dataframe(
            poetry_subset[["technical_name"]],
            use_container_width=True,
            hide_index=True,
            column_config={"technical_name": "Connectors using poetry"},
        )
        st.dataframe(
            non_poetry_subset[["technical_name"]],
            use_container_width=True,
            hide_index=True,
            column_config={"technical_name": "Connectors not using poetry"},
        )

    with pypi_tab:
        left, middle, right = st.columns((1, 1, 1))
        left.metric(
            "Migration progress",
            f"{round(adoption_metrics.migration_to_pypi_progress * 100)}%  🎉",
        )
        middle.metric("On PyPi", f"{adoption_metrics.num_on_pypi} 🟢")
        right.metric(
            "Not on PyPi",
            f"{adoption_metrics.num_not_on_pypi} 🔴",
        )
        st.dataframe(
            pypi_subset[["technical_name"]],
            use_container_width=True,
            hide_index=True,
            column_config={"technical_name": "Connectors on PyPi"},
        )
        st.dataframe(
            non_pypi_subset[["technical_name"]],
            use_container_width=True,
            hide_index=True,
            column_config={"technical_name": "Connectors not on PyPi"},
        )


st.title("👮 Tracking compliance of our Python source connectors to our standards")

st.markdown(
    """This app helps tracking our progress in enforcing a set of standards on our  Python connectors:
- **Adopting the low-code CDK**: to reduce the maintenance burden and improve the connectors reliability.
- **Adopting our base image**: to improve build process consistency and security of our connectors.
- **Adopting `poetry`**: to get reproducible builds (by locking dependencies) and avoid unexpected regression.
- **Publishing to PyPi**: to make connectors available to `airbyte-lib`.
"""
)

st.subheader("High-level metrics")
certified_count, community_count = st.columns((1, 1))
certified_count.metric(
    "Num. of certified python source connectors",
    len(SUPPORT_LEVELS_CONFIG["certified"]["data"]),
)
community_count.metric(
    "Num. of community python source connectors",
    len(SUPPORT_LEVELS_CONFIG["community"]["data"]),
)

st.subheader("Standard adoption metrics")

for connectors, tab in zip(
    [
        support_level_config["data"]
        for support_level_config in SUPPORT_LEVELS_CONFIG.values()
    ],
    st.tabs(
        [
            support_level_config["title"]
            for support_level_config in SUPPORT_LEVELS_CONFIG.values()
        ]
    ),
):
    with tab:
        print_adoption(connectors)

st.markdown(
    f"""
#### Datasource
All these metrics are computed from the [Airbyte OSS registry]({OSS_REGISTRY_URL}) and by direct access to code files using `raw.github.com`.

The data is refreshed every {str(DATA_REFRESH_INTERVAL)} hours to ensure the most accurate information is displayed.

Reach out to [@alafanechere](https://github.com/alafanechere) for feedback or question about this app!
"""
)
