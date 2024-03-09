from dataclasses import dataclass
from typing import List, Optional


@dataclass(kw_only=True)
class Connector:
    is_on_pypi: bool
    is_using_base_image: bool
    is_using_poetry: bool
    support_level: str
    tags: List
    technical_name: str
    type_: str
    base_image_version: Optional[str] = None

    @property
    def language(self) -> str:
        for tag in self.tags:
            if "language" in tag:
                return tag.split(":")[1]

    @property
    def is_low_code(self):
        return "cdk:low-code" in self.tags

    def to_dict(self):
        return {
            "is_on_pypi": self.is_on_pypi,
            "is_using_base_image": self.is_using_base_image,
            "is_using_poetry": self.is_using_poetry,
            "support_level": self.support_level,
            "tags": self.tags,
            "technical_name": self.technical_name,
            "type": self.type_,
            "base_image_version": self.base_image_version,
            "is_low_code": self.is_low_code,
            "language": self.language,
        }
