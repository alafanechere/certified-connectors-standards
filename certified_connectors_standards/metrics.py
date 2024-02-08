from __future__ import annotations
from typing import TYPE_CHECKING
from datasets import CERTIFIED_PYTHON_SOURCE_CONNECTORS

if TYPE_CHECKING:
    import pandas as pd


class ConnectorMetrics:
    def __init__(self, connectors: pd.DataFrame) -> None:
        self.connectors = connectors

    @property
    def total(self) -> int:
        return len(self.connectors)

    @property
    def num_with_base_image(self) -> int:
        return len(self.connectors[self.connectors["is_using_base_image"]])

    @property
    def num_without_base_image(self) -> int:
        return self.total - self.num_with_base_image

    @property
    def migration_to_base_image_progress(self) -> float:
        return self.num_with_base_image / self.total

    @property
    def num_with_poetry(self) -> int:
        return len(self.connectors[self.connectors["is_using_poetry"]])

    @property
    def num_without_poetry(self) -> int:
        return self.total - self.num_with_poetry

    @property
    def migration_to_poetry_progress(self) -> float:
        return self.num_with_poetry / self.total

    @property
    def num_with_low_code(self) -> int:
        return len(self.connectors[self.connectors["is_low_code"]])

    @property
    def num_without_low_code(self) -> int:
        return self.total - self.num_with_low_code

    @property
    def migration_to_low_code_progress(self) -> float:
        return self.num_with_low_code / self.total

    @property
    def num_on_pypi(self) -> int:
        return len(self.connectors[self.connectors["is_on_pypi"]])

    @property
    def num_not_on_pypi(self) -> int:
        return self.total - self.num_on_pypi

    @property
    def migration_to_pypi_progress(self) -> float:
        return self.num_on_pypi / self.total


CERTIFIED_PYTHON_SOURCE_CONNECTORS_METRICS = ConnectorMetrics(
    CERTIFIED_PYTHON_SOURCE_CONNECTORS
)
