from .base import ResponseModel
from .hello import Hello
from .hugs import Hugs

MODELS = {
    "hello": Hello,
    "hugs": Hugs,
}

__all__ = ["MODELS", "ResponseModel"]
