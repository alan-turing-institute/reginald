from .base import ResponseModel
from .hello import Hello
from .hugs import Hugs
from .openai import OpenAI

MODELS = {
    "hello": Hello,
    "hugs": Hugs,
    "openai": OpenAI,
}

__all__ = ["MODELS", "ResponseModel"]
