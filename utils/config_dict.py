from typing import TypedDict

from pydantic import ConfigDict as ConfigDict_pydantic
from sqlalchemy import BinaryExpression

from database import Base


class AnnotateJoin(TypedDict, total=False):
    model: Base
    onclause: BinaryExpression | None


class ConfigDict(ConfigDict_pydantic, total=False):
    relation_prefix: dict[str, AnnotateJoin]
