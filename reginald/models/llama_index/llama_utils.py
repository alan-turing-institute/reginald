import logging
from math import ceil
from typing import Callable

from llama_index.core import PromptHelper, Settings
from llama_index.core.base.llms.base import BaseLLM
from llama_index.core.settings import _Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def compute_default_chunk_size(max_input_size: int, k: int) -> int:
    """
    Compute the default chunk size to use for the index vector store.

    Parameters
    ----------
    max_input_size : int
        Maximum input size for the LLM.
    k : int
        `similarity_top_k` to use in chat or query engine.

    Returns
    -------
    int
        Default chunk size to use for the index vector store.
    """
    return ceil(max_input_size / (k + 1))


def setup_settings(
    llm: BaseLLM,
    max_input_size: int | str,
    num_output: int | str,
    chunk_overlap_ratio: float | str,
    chunk_size: int | str | None = None,
    k: int | str | None = None,
    tokenizer: Callable[[str], int] | None = None,
) -> _Settings:
    """
    Helper function to set up the settings.
    Can pass in either chunk_size or k.
    If chunk_size is not provided, it is computed as
    `ceil(max_input_size / k)`.
    If chunk_size is provided, k is ignored.

    Parameters
    ----------
    llm : BaseLLM
        LLM to use to create the index vectors.
    max_input_size : int | str
        Context window size for the LLM.
    num_output : int, optional
        Number of outputs for the LLM.
    chunk_overlap_ratio : float, optional
        Chunk overlap as a ratio of chunk size._
    chunk_size : int | None, optional
        Maximum size of chunks to use, by default None.
        If None, this is computed as `ceil(max_input_size / k)`.
    k : int | str | None, optional
        `similarity_top_k` to use in chat or query engine,
        by default None
    tokenizer: Callable[[str], int] | None, optional
        Tokenizer to use. A callable function on a string.
        Can also be None if using the default set by LlamaIndex.

    Returns
    -------
    Settings
        _Settings object to use to create the index vectors.
    """
    if chunk_size is None and k is None:
        raise ValueError("Either chunk_size or k must be provided.")

    # convert to int or float if necessary
    if isinstance(max_input_size, str):
        max_input_size = int(max_input_size)
    if isinstance(num_output, str):
        num_output = int(num_output)
    if isinstance(chunk_overlap_ratio, str):
        chunk_overlap_ratio = float(chunk_overlap_ratio)
    if isinstance(chunk_size, str):
        chunk_size = int(chunk_size)
    if isinstance(k, str):
        k = int(k)

    # if chunk_size is not provided, compute a default value
    chunk_size = chunk_size or compute_default_chunk_size(
        max_input_size=max_input_size, k=k
    )

    # initialise embedding model to use to create the index vectors
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-mpnet-base-v2",
        embed_batch_size=128,
    )

    # construct the prompt helper
    prompt_helper = PromptHelper(
        context_window=max_input_size,
        num_output=num_output,
        chunk_size_limit=chunk_size,
        chunk_overlap_ratio=chunk_overlap_ratio,
        tokenizer=tokenizer,
    )

    # construct the settings (and logging the settings set)
    Settings.llm = llm
    logging.info(f"Settings llm: {llm}")
    Settings.embed_model = embed_model
    logging.info(f"Settings embed_model: {embed_model}")
    logging.info(f"Embedding model initialised on device {embed_model._device}")
    Settings.prompt_helper = prompt_helper
    logging.info(f"Settings prompt_helper: {prompt_helper}")
    Settings.chunk_size = chunk_size
    logging.info(f"Settings chunk_size: {chunk_size}")
    Settings.tokenizer = tokenizer
    logging.info(f"Settings tokenizer: {tokenizer}")

    return Settings
