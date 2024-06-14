from __future__ import annotations

import logging
import pathlib
import re
import sys

import nest_asyncio
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.base.llms.base import BaseLLM
from llama_index.core.base.response.schema import RESPONSE_TYPE

from reginald.models.base import MessageResponse, ResponseModel
from reginald.utils import stream_iter_progress_wrapper, stream_progress_wrapper

nest_asyncio.apply()


from reginald.defaults import LLAMA_INDEX_DIR
from reginald.models.llama_index.data_index_creator import DataIndexCreator
from reginald.models.llama_index.llama_utils import (
    compute_default_chunk_size,
    setup_settings,
)


class LlamaIndex(ResponseModel):
    def __init__(
        self,
        model_name: str,
        max_input_size: int,
        data_dir: pathlib.Path | str,
        which_index: str,
        mode: str = "chat",
        k: int = 3,
        chunk_size: int | None = None,
        chunk_overlap_ratio: float = 0.1,
        num_output: int = 512,
        force_new_index: bool = False,
        *args,
        **kwargs,
    ) -> None:
        """
        Base class for models using llama-index.
        This class is not intended to be used directly, but rather subclassed
        to implement the `_prep_llm` method which constructs the LLM to be used.

        Parameters
        ----------
        model_name : str
            Model name to specify which LLM to use.
        max_input_size : int
            Context window size for the LLM.
        data_dir : pathlib.Path | str
            Path to the data directory.
        which_index : str
            Which index to construct (if force_new_index is True) or use.
            Options are "handbook", "wikis",  "public", "reg" or "all_data".
        mode : Optional[str], optional
            The type of engine to use when interacting with the data, options of "chat" or "query".
            Default is "chat".
        k : int, optional
            `similarity_top_k` to use in chat or query engine, by default 3
        chunk_size : int | None, optional
            Maximum size of chunks to use, by default None.
            If None, this is computed as `ceil(max_input_size / k)`.
        chunk_overlap_ratio : float, optional
            Chunk overlap as a ratio of chunk size, by default 0.1
        num_output : int, optional
            Number of outputs for the LLM, by default 512
        force_new_index : bool, optional
            Whether or not to recreate the index vector store,
            by default False
        """
        super().__init__(*args, emoji="llama", **kwargs)
        logging.info("Setting up Huggingface backend.")
        if mode == "chat":
            logging.info("Setting up chat engine.")
        elif mode == "query":
            logging.info("Setting up query engine.")
        else:
            logging.error("Mode must either be 'query' or 'chat'.")
            sys.exit(1)

        self.max_input_size = max_input_size
        self.model_name = model_name
        self.num_output = num_output
        self.mode = mode
        self.k = k
        self.chunk_size = chunk_size or compute_default_chunk_size(
            max_input_size=max_input_size, k=k
        )
        self.chunk_overlap_ratio = chunk_overlap_ratio
        self.data_dir = pathlib.Path(data_dir)
        self.which_index = which_index
        self.documents = []

        # set up LLM
        llm = self._prep_llm()

        # set up settings
        settings = setup_settings(
            llm=llm,
            max_input_size=self.max_input_size,
            num_output=self.num_output,
            chunk_size=self.chunk_size,
            chunk_overlap_ratio=self.chunk_overlap_ratio,
            k=self.k,
            tokenizer=self._prep_tokenizer(),
        )

        if force_new_index:
            logging.info("Generating the index from scratch...")
            data_creator = DataIndexCreator(
                which_index=self.which_index,
                data_dir=self.data_dir,
                settings=settings,
            )
            self.index: VectorStoreIndex = stream_progress_wrapper(
                data_creator.create_index,
                task_str="Generating the index from scratch...",
            )
            stream_progress_wrapper(
                data_creator.save_index,
                task_str="Saving the index...",
            )

        else:
            logging.info("Loading the storage context")
            storage_context = stream_progress_wrapper(
                StorageContext.from_defaults,
                task_str="Loading the storage context...",
                persist_dir=self.data_dir / LLAMA_INDEX_DIR / self.which_index,
            )

            logging.info("Loading the pre-processed index")
            self.index = stream_progress_wrapper(
                load_index_from_storage,
                task_str="Loading the pre-processed index...",
                storage_context=storage_context,
                settings=settings,
            )

        self.response_mode = "simple_summarize"
        if self.mode == "chat":
            self.chat_engine = {}
            logging.info("Done setting up Huggingface backend for chat engine.")
        elif self.mode == "query":
            self.query_engine = self.index.as_query_engine(
                response_mode=self.response_mode,
                similarity_top_k=k,
            )
            logging.info("Done setting up Huggingface backend for query engine.")

        self.error_response_template = (
            "Oh no! When I tried to get a response to your prompt, "
            "I got the following error:"
            "\n```\n{}\n```"
        )

    @staticmethod
    def _format_sources(response: RESPONSE_TYPE) -> str:
        """
        Method to format the sources used to compose the response.

        Parameters
        ----------
        response : RESPONSE_TYPE
            response object from the query engine

        Returns
        -------
        str
            String containing the formatted sources that
            were used to compose the response
        """
        texts = []
        for source_node in response.source_nodes:
            # obtain the URL for source
            try:
                node_url = source_node.node.extra_info["url"]
            except KeyError:
                node_url = source_node.node.extra_info["filename"]

            # add its similarity score and append to texts
            source_text = node_url + f" (similarity: {round(source_node.score, 2)})"
            texts.append(source_text)

        result = "I read the following documents to compose this answer:\n"
        result += "\n\n".join(texts)

        return result

    def _prep_llm(self) -> BaseLLM:
        """
        Method to prepare the LLM to be used.

        Returns
        -------
        BaseLLM
            LLM to be used.

        Raises
        ------
        NotImplemented
            This must be implemented by a subclass of LlamaIndex.
        """
        raise NotImplementedError(
            "_prep_llm needs to be implemented by a subclass of LlamaIndex."
        )

    def _prep_tokenizer(self) -> callable[str] | None:
        """
        Method to prepare the Tokenizer to be used.

        Returns
        -------
        callable[str] | None
            Tokenizer to use. A callable function on a string.
            Can also be None if using the default set by LlamaIndex.

        Raises
        ------
        NotImplemented
        """
        raise NotImplementedError(
            "_prep_tokenizer needs to be implemented by a subclass of LlamaIndex."
        )

    def _get_response(self, message: str, user_id: str) -> MessageResponse:
        """
        Method to respond to a message in Slack.

        Parameters
        ----------
        msg_in : str
            Message from user
        user_id : str
            User ID

        Returns
        -------
        MessageResponse
            Response from the query engine.
        """
        try:
            if self.mode == "chat":
                # create chat engine for user if does not exist
                if self.chat_engine.get(user_id) is None:
                    self.chat_engine[user_id] = self.index.as_chat_engine(
                        chat_mode="context",
                        response_mode=self.response_mode,
                        similarity_top_k=self.k,
                    )

                # obtain chat engine for particular user
                chat_engine = self.chat_engine[user_id]
                response = chat_engine.chat(message)
            elif self.mode == "query":
                self.query_engine._response_synthesizer._streaming = False
                response = self.query_engine.query(message)

            # concatenate the response with the resources that it used
            formatted_response = (
                response.response + "\n\n\n" + self._format_sources(response)
            )
        except Exception as e:  # ignore: broad-except
            formatted_response = self.error_response_template.format(repr(e))

        pattern = (
            r"(?s)^Context information is"
            r".*"
            r"Given the context information and not prior knowledge, answer the question: "
            rf"{message}"
            r"\n(.*)"
        )
        m = re.search(pattern, formatted_response)

        if m:
            answer = m.group(1)
        else:
            logging.warning(
                "Was expecting a backend response with a regular expression but couldn't find a match."
            )
            answer = formatted_response

        return MessageResponse(answer)

    def direct_message(self, message: str, user_id: str) -> MessageResponse:
        """
        Method to respond to a direct message in Slack.

        Parameters
        ----------
        msg_in : str
            Message from user
        user_id : str
            User ID

        Returns
        -------
        MessageResponse
            Response from the query engine.
        """
        return self._get_response(message=message, user_id=user_id)

    def channel_mention(self, message: str, user_id: str) -> MessageResponse:
        """
        Method to respond to a channel mention in Slack.

        Parameters
        ----------
        msg_in : str
            Message from user
        user_id : str
            User ID

        Returns
        -------
        MessageResponse
            Response from the query engine.
        """
        return self._get_response(message=message, user_id=user_id)

    def stream_message(self, message: str, user_id: str) -> None:
        """
        Method to respond to a stream message in Slack.

        Parameters
        ----------
        msg_in : str
            Message from user
        user_id : str
            User ID

        Returns
        -------
        MessageResponse
            Response from the query engine.
        """
        try:
            if self.mode == "chat":
                # create chat engine for user if does not exist
                if self.chat_engine.get(user_id) is None:
                    self.chat_engine[user_id] = self.index.as_chat_engine(
                        chat_mode="context",
                        response_mode=self.response_mode,
                        similarity_top_k=self.k,
                        streaming=True,
                    )

                # obtain chat engine for particular user
                chat_engine = self.chat_engine[user_id]
                response_stream = chat_engine.stream_chat(message)
            elif self.mode == "query":
                self.query_engine._response_synthesizer._streaming = True
                response_stream = self.query_engine.query(message)

            for token in stream_iter_progress_wrapper(response_stream.response_gen):
                print(token, end="", flush=True)

            formatted_response = "\n\n\n" + self._format_sources(response_stream)

            for token in re.split(r"(\s+)", formatted_response):
                print(token, end="", flush=True)
        except Exception as e:  # ignore: broad-except
            for token in re.split(
                r"(\s+)", self.error_response_template.format(repr(e))
            ):
                print(token, end="", flush=True)
