from .base import ResponseModel
from .hello import Hello

MODELS = {
    "hello": Hello,
}

__all__ = ["MODELS", "ResponseModel"]
