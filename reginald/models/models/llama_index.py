from __future__ import annotations

import logging
import math
import os
import pathlib
import re
import sys
from tempfile import TemporaryDirectory
from typing import Any, Optional

import nest_asyncio
import pandas as pd
from git import Repo
from langchain.embeddings import HuggingFaceEmbeddings
from llama_hub.github_repo import GithubClient, GithubRepositoryReader

# from llama_hub.github_repo_collaborators import (
#     GitHubCollaboratorsClient,
#     GitHubRepositoryCollaboratorsReader,
# )
from llama_hub.github_repo_issues import (
    GitHubIssuesClient,
    GitHubRepositoryIssuesReader,
)
from llama_index import (
    Document,
    PromptHelper,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index.indices.vector_store.base import VectorStoreIndex
from llama_index.llms import AzureOpenAI, HuggingFaceLLM, LlamaCPP, OpenAI
from llama_index.llms.base import LLM
from llama_index.llms.llama_utils import completion_to_prompt, messages_to_prompt
from llama_index.prompts import PromptTemplate
from llama_index.readers import SimpleDirectoryReader
from llama_index.response.schema import RESPONSE_TYPE

from reginald.models.models.base import MessageResponse, ResponseModel

nest_asyncio.apply()


LLAMA_INDEX_DIR = "llama_index_indices"
PUBLIC_DATA_DIR = "public"
INTERNAL_DATA_DIR = "turing_internal"


class LlamaIndex(ResponseModel):
    def __init__(
        self,
        model_name: str,
        max_input_size: int,
        data_dir: pathlib.Path,
        which_index: str,
        mode: str = "chat",
        k: int = 3,
        chunk_size: Optional[int] = None,
        chunk_overlap_ratio: float = 0.1,
        force_new_index: bool = False,
        num_output: int = 512,
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
        data_dir : pathlib.Path
            Path to the data directory.
        which_index : str
            Which index to construct (if force_new_index is True) or use.
            Options are "handbook", "wikis",  "public", or "all_data".
        mode : Optional[str], optional
            The type of engine to use when interacting with the data, options of "chat" or "query".
            Default is "chat".
        k : int, optional
            `similarity_top_k` to use in char or query engine, by default 3
        chunk_size : Optional[int], optional
            Maximum size of chunks to use, by default None.
            If None, this is computed as `ceil(max_input_size / k)`.
        chunk_overlap_ratio : float, optional
            Chunk overlap as a ratio of chunk size, by default 0.1
        force_new_index : bool, optional
            Whether or not to recreate the index vector store,
            by default False
        num_output : int, optional
            Number of outputs for the LLM, by default 512
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
        if chunk_size is None:
            chunk_size = math.ceil(max_input_size / (k + 1))
        self.mode = mode
        self.k = k
        self.chunk_size = chunk_size
        self.chunk_overlap_ratio = chunk_overlap_ratio
        self.data_dir = data_dir
        self.which_index = which_index
        self.documents = []

        # set up LLM
        llm = self._prep_llm()

        # initialise embedding model to use to create the index vectors
        embed_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

        # construct the prompt helper
        prompt_helper = PromptHelper(
            context_window=self.max_input_size,
            num_output=self.num_output,
            chunk_size_limit=self.chunk_size,
            chunk_overlap_ratio=self.chunk_overlap_ratio,
        )

        # construct the service context
        service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
            prompt_helper=prompt_helper,
            chunk_size=chunk_size,
        )

        if force_new_index:
            logging.info("Generating the index from scratch...")
            self._prep_documents()
            self.index = VectorStoreIndex.from_documents(
                self.documents, service_context=service_context
            )

            # save the service context and persist the index
            logging.info("Saving the index")
            self.index.storage_context.persist(
                persist_dir=self.data_dir / LLAMA_INDEX_DIR / which_index
            )

        else:
            logging.info("Loading the storage context")
            storage_context = StorageContext.from_defaults(
                persist_dir=self.data_dir / LLAMA_INDEX_DIR / which_index
            )

            logging.info("Loading the pre-processed index")
            self.index = load_index_from_storage(
                storage_context=storage_context, service_context=service_context
            )

        response_mode = "simple_summarize"
        if self.mode == "chat":
            self.chat_engine = {}
            logging.info("Done setting up Huggingface backend for chat engine.")
        elif self.mode == "query":
            self.query_engine = self.index.as_query_engine(
                response_mode=response_mode, similarity_top_k=k
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

    def _get_response(self, msg_in: str, user_id: str) -> str:
        """
        Method to obtain a response from the query/chat engine given
        a message and a user id.

        Parameters
        ----------
        msg_in : str
            Message from user
        user_id : str
            User ID

        Returns
        -------
        str
            String containing the response from the query engine.
        """
        response_mode = "simple_summarize"
        try:
            if self.mode == "chat":
                # create chat engine for user if does not exist
                if self.chat_engine.get(user_id) is None:
                    self.chat_engine[user_id] = self.index.as_chat_engine(
                        chat_mode="context",
                        response_mode=response_mode,
                        similarity_top_k=self.k,
                    )

                # obtain chat engine for particular user
                chat_engine = self.chat_engine[user_id]
                response = chat_engine.chat(msg_in)
            elif self.mode == "query":
                response = self.query_engine.query(msg_in)

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
            rf"{msg_in}"
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
        return answer

    def _prep_documents(self):
        """
        Method to prepare the documents for the index vector store.

        """
        # Prep the contextual documents
        gh_token = os.getenv("GITHUB_TOKEN")

        if gh_token is None:
            raise ValueError(
                "Please export your github personal access token as 'GITHUB_TOKEN'."
            )

        if self.which_index == "handbook":
            logging.info("Regenerating index only for the handbook")

            # load handbook from repo
            self._load_handbook(gh_token)

        elif self.which_index == "wikis":
            logging.info("Regenerating index only for the wikis")

            # load wikis
            self._load_wikis(gh_token)

        elif self.which_index == "public":
            logging.info("Regenerating index for all PUBLIC. Will take a long time...")

            # load in scraped turing.ac.uk website
            self._load_turing_ac_uk()

            # load public data from repos
            self._load_handbook(gh_token)
            self._load_rse_course(gh_token)
            self._load_rds_course(gh_token)
            self._load_turing_way(gh_token)

        elif self.which_index == "all_data":
            logging.info("Regenerating index for ALL DATA. Will take a long time...")

            # load in scraped turing.ac.uk website
            self._load_turing_ac_uk()

            # load public data from repos
            self._load_handbook(gh_token)
            self._load_rse_course(gh_token)
            self._load_rds_course(gh_token)
            self._load_turing_way(gh_token)

            # load hut23 data
            self._load_hut23(gh_token)

            # load wikis
            self._load_wikis(gh_token)

        else:
            logging.info("The data_files directory is unrecognized")

    def _load_turing_ac_uk(self):
        data_file = f"{self.data_dir}/public/turingacuk-no-boilerplate.csv"
        turing_df = pd.read_csv(data_file)
        turing_df = turing_df[~turing_df.loc[:, "body"].isna()]
        self.documents += [
            Document(text=row[1]["body"], extra_info={"url": row[1]["url"]})
            for row in turing_df.iterrows()
        ]

    def _load_handbook(self, gh_token):
        owner = "alan-turing-institute"
        repo = "REG-handbook"

        handbook_loader = GithubRepositoryReader(
            GithubClient(gh_token),
            owner=owner,
            repo=repo,
            verbose=False,
            filter_file_extensions=([".md"], GithubRepositoryReader.FilterType.INCLUDE),
            filter_directories=(["content"], GithubRepositoryReader.FilterType.INCLUDE),
        )
        self.documents.extend(handbook_loader.load_data(branch="main"))

    def _load_rse_course(self, gh_token):
        owner = "alan-turing-institute"
        repo = "rse-course"

        rse_course_loader = GithubRepositoryReader(
            GithubClient(gh_token),
            owner=owner,
            repo=repo,
            verbose=False,
            filter_file_extensions=(
                [".md", ".ipynb"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
        )
        self.documents.extend(rse_course_loader.load_data(branch="main"))

    def _load_rds_course(self, gh_token):
        owner = "alan-turing-institute"
        repo = "rds-course"

        rds_course_loader = GithubRepositoryReader(
            GithubClient(gh_token),
            owner=owner,
            repo=repo,
            verbose=False,
            filter_file_extensions=(
                [".md", ".ipynb"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
        )
        self.documents.extend(rds_course_loader.load_data(branch="develop"))

    def _load_turing_way(self, gh_token):
        owner = "the-turing-way"
        repo = "the-turing-way"

        turing_way_loader = GithubRepositoryReader(
            GithubClient(gh_token),
            owner=owner,
            repo=repo,
            verbose=False,
            filter_file_extensions=([".md"], GithubRepositoryReader.FilterType.INCLUDE),
        )
        self.documents.extend(turing_way_loader.load_data(branch="main"))

    def _load_hut23(self, gh_token):
        owner = "alan-turing-institute"
        repo = "Hut23"

        # load repo
        hut23_repo_loader = GithubRepositoryReader(
            GithubClient(gh_token),
            owner=owner,
            repo=repo,
            verbose=False,
            filter_file_extensions=(
                [".md", ".ipynb"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
            filter_directories=(
                [
                    "JDs",
                    "development",
                    "newsletters",
                    "objectives",
                    "rfc",
                ],  # we can adjust these
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
        )
        self.documents.extend(hut23_repo_loader.load_data(branch="main"))

        # load_issues
        hut23_issues_loader = GitHubRepositoryIssuesReader(
            GitHubIssuesClient(gh_token),
            owner=owner,
            repo=repo,
            verbose=True,
        )

        issue_docs = hut23_issues_loader.load_data()
        for doc in issue_docs:
            doc.metadata["api_url"] = str(doc.metadata["url"])
            doc.metadata["url"] = doc.metadata["source"]
        self.documents.extend(issue_docs)

        # load collaborators
        # hut23_collaborators_loader = GitHubRepositoryCollaboratorsReader(
        #     GitHubCollaboratorsClient(gh_token),
        #     owner=owner,
        #     repo=repo,
        #     verbose=True,
        # )
        # self.documents.extend(hut23_collaborators_loader.load_data())

    def _load_wikis(self, gh_token):
        wiki_urls = [
            "https://github.com/alan-turing-institute/research-engineering-group.wiki.git",
            "https://github.com/alan-turing-institute/Hut23.wiki.git",
        ]

        for url in wiki_urls:
            temp_dir = TemporaryDirectory()
            wiki_path = os.path.join(temp_dir.name, url.split("/")[-1])

            _ = Repo.clone_from(url, wiki_path)

            reader = SimpleDirectoryReader(
                input_dir=wiki_path,
                required_exts=[".md"],
                recursive=True,
                filename_as_id=True,
            )

            # get base url and file names
            base_url = url.removesuffix(".wiki.git")
            fnames = [str(file) for file in reader.input_files]

            # get file urls and create dictionary to map fname to url
            file_urls = [
                os.path.join(base_url, "wiki", fname.split("/")[-1].removesuffix(".md"))
                for fname in fnames
            ]
            file_urls_dict = {
                fname: file_url for fname, file_url in zip(fnames, file_urls)
            }

            def get_urls(fname):
                return {"url": file_urls_dict.get(fname)}

            # add `get_urls` function to reader
            reader.file_metadata = get_urls

            self.documents.extend(reader.load_data())

    def _prep_llm(self) -> LLM:
        """
        Method to prepare the LLM to be used.

        Returns
        -------
        LLM
            LLM to be used.

        Raises
        ------
        NotImplemented
            This must be implemented by a subclass of LlamaIndex.
        """
        raise NotImplementedError(
            "_prep_llm needs to be implemented by a subclass of LlamaIndex."
        )

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
        backend_response = self._get_response(message, user_id)

        return MessageResponse(backend_response)

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
        backend_response = self._get_response(message, user_id)

        return MessageResponse(backend_response)


class LlamaIndexLlamaCPP(LlamaIndex):
    def __init__(
        self,
        model_name: str,
        is_path: bool,
        n_gpu_layers: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        `LlamaIndexLlamaCPP` is a subclass of `LlamaIndex` that uses
        llama-cpp to implement the LLM.

        Parameters
        ----------
        model_name : str
            Either the path to the model or the URL to download the model from
        is_path : bool, optional
            If True, model_name is used as a path to the model file,
            otherwise it should be the URL to download the model
        n_gpu_layers : int, optional
            Number of layers to offload to GPU.
            If -1, all layers are offloaded, by default 0
        """
        self.is_path = is_path
        self.n_gpu_layers = n_gpu_layers
        super().__init__(*args, model_name=model_name, **kwargs)

    def _prep_llm(self) -> LLM:
        logging.info(
            f"Setting up LlamaCPP LLM (model {self.model_name}) on {self.n_gpu_layers} GPU layers"
        )
        logging.info(
            f"LlamaCPP-args: (context_window: {self.max_input_size}, num_output: {self.num_output})"
        )

        return LlamaCPP(
            model_url=self.model_name if not self.is_path else None,
            model_path=self.model_name if self.is_path else None,
            temperature=0.1,
            max_new_tokens=self.num_output,
            context_window=self.max_input_size,
            # kwargs to pass to __call__()
            generate_kwargs={},
            # kwargs to pass to __init__()
            model_kwargs={"n_gpu_layers": self.n_gpu_layers},
            # transform inputs into Llama2 format
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=True,
        )


class LlamaIndexHF(LlamaIndex):
    def __init__(
        self,
        model_name: str = "StabilityAI/stablelm-tuned-alpha-3b",
        device: str = "auto",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        `LlamaIndexHF` is a subclass of `LlamaIndex` that uses HuggingFace's
        `transformers` library to implement the LLM.

        Parameters
        ----------
        model_name : str, optional
            Model name from Huggingface's model hub,
            by default "StabilityAI/stablelm-tuned-alpha-3b".
        device : str, optional
            Device map to use for the LLM, by default "auto".
        """
        self.device = device
        super().__init__(*args, model_name=model_name, **kwargs)

    def _prep_llm(self) -> LLM:
        logging.info(
            f"Setting up Huggingface LLM (model {self.model_name}) on device {self.device}"
        )
        logging.info(
            f"HF-args: (context_window: {self.max_input_size}, num_output: {self.num_output})"
        )

        return HuggingFaceLLM(
            context_window=self.max_input_size,
            max_new_tokens=self.num_output,
            # TODO: allow user to specify the query wrapper prompt for their model
            query_wrapper_prompt=PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>"),
            generate_kwargs={"temperature": 0.1, "do_sample": False},
            tokenizer_name=self.model_name,
            model_name=self.model_name,
            device_map=self.device or "auto",
        )


class LlamaIndexGPTOpenAI(LlamaIndex):
    def __init__(
        self, model_name: str = "gpt-3.5-turbo", *args: Any, **kwargs: Any
    ) -> None:
        """
        Parameters
        ----------
        model_name : str, optional
            The model to use from the OpenAI API, by default "gpt-3.5-turbo"

        `LlamaIndexGPTOpenAI` is a subclass of `LlamaIndex` that uses OpenAI's
        API to implement the LLM.

        Must have `OPENAI_API_KEY` set as an environment variable.
        """
        if os.getenv("OPENAI_API_KEY") is None:
            raise ValueError("You must set OPENAI_API_KEY for OpenAI.")

        self.model_name = model_name
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.temperature = 0.7
        super().__init__(*args, model_name=self.model_name, **kwargs)

    def _prep_llm(self) -> LLM:
        return OpenAI(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.num_output,
            api_key=self.openai_api_key,
        )


class LlamaIndexGPTAzure(LlamaIndex):
    def __init__(
        self, model_name: str = "reginald-gpt35-turbo", *args: Any, **kwargs: Any
    ) -> None:
        """
        Parameters
        ----------
        model_name : str, optional
            The deployment name of the model, by default "reginald-gpt35-turbo"

        `LlamaIndexGPTAzure` is a subclass of `LlamaIndex` that uses Azure's
        instance of OpenAI's LLMs to implement the LLM.

        Must have the following environment variables set:
        - `OPENAI_API_BASE`: Azure endpoint which looks
          like https://YOUR_RESOURCE_NAME.openai.azure.com/
        - `OPENAI_API_KEY`: Azure API key
        """
        if os.getenv("OPENAI_AZURE_API_BASE") is None:
            raise ValueError(
                "You must set OPENAI_AZURE_API_BASE to your Azure endpoint. "
                "It should look like https://YOUR_RESOURCE_NAME.openai.azure.com/"
            )
        if os.getenv("OPENAI_AZURE_API_KEY") is None:
            raise ValueError("You must set OPENAI_AZURE_API_KEY for Azure OpenAI.")

        # deployment name can be found in the Azure AI Studio portal
        self.deployment_name = model_name
        self.openai_api_base = os.getenv("OPENAI_AZURE_API_BASE")
        self.openai_api_key = os.getenv("OPENAI_AZURE_API_KEY")
        self.openai_api_version = "2023-03-15-preview"
        self.temperature = 0.7
        super().__init__(*args, model_name="gpt-3.5-turbo", **kwargs)

    def _prep_llm(self) -> LLM:
        logging.info(f"Setting up AzureOpenAI LLM (model {self.deployment_name})")
        return AzureOpenAI(
            model=self.model_name,
            engine=self.deployment_name,
            temperature=self.temperature,
            max_tokens=self.num_output,
            api_key=self.openai_api_key,
            api_base=self.openai_api_base,
            api_type="azure",
            api_version=self.openai_api_version,
        )
