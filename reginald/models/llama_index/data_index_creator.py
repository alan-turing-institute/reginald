import logging
import os
import pathlib
from tempfile import TemporaryDirectory

import pandas as pd
from git import Repo
from httpx import HTTPError
from llama_index.core import Document, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.settings import _Settings
from llama_index.readers.github import (
    GithubClient,
    GitHubIssuesClient,
    GitHubRepositoryIssuesReader,
    GithubRepositoryReader,
)

from reginald.defaults import LLAMA_INDEX_DIR
from reginald.utils import get_env_var


class DataIndexCreator:
    def __init__(
        self,
        data_dir: pathlib.Path | str,
        which_index: str,
        settings: _Settings,
    ) -> None:
        """
        Class for creating the data index.

        Parameters
        ----------
        data_dir : pathlib.Path | str
            Path to the data directory.
        which_index : str
            Which index to construct (if force_new_index is True) or use.
            Options are "handbook", "wikis",  "public", "reg" or "all_data".
        settings : _Settings
            llama_index.core.settings._Settings object to use to create the index.
        """
        self.data_dir: pathlib.Path = pathlib.Path(data_dir)
        self.which_index: str = which_index
        self.settings: _Settings = settings
        self.documents: list[str] = []
        self.index: VectorStoreIndex | None = None

    def prep_documents(self) -> None:
        """
        Method to prepare the documents for the index vector store.
        """
        # prep the contextual documents
        gh_token = get_env_var("GITHUB_TOKEN")

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

        elif self.which_index == "reg":
            logging.info("Regenerating index for REG. Will take a long time...")

            # load in scraped turing.ac.uk website
            self._load_turing_ac_uk()

            # load public data from repos
            self._load_handbook(gh_token)

            # load hut23 data
            self._load_hut23(gh_token)

            # load wikis
            self._load_wikis(gh_token)

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
            logging.info("The which_index provided is unrecognized")

    def _load_turing_ac_uk(self) -> None:
        """
        Load in the scraped turing.ac.uk website.

        For 'public' index and 'all_data' index.
        """
        data_file = f"{self.data_dir}/public/turingacuk-no-boilerplate.csv"
        turing_df = pd.read_csv(data_file)
        turing_df = turing_df[~turing_df.loc[:, "body"].isna()]
        self.documents += [
            Document(text=row[1]["body"], extra_info={"url": row[1]["url"]})
            for row in turing_df.iterrows()
        ]

    def _load_handbook(self, gh_token: str) -> None:
        """
        Load in the REG handbook.

        For 'handbook' index, 'public' index, and 'all_data' index.

        Parameters
        ----------
        gh_token : str
            Github token to use to access the handbook repo.
        """
        owner = "alan-turing-institute"
        repo = "REG-handbook"

        handbook_loader = GithubRepositoryReader(
            GithubClient(gh_token, fail_on_http_error=False),
            owner=owner,
            repo=repo,
            verbose=False,
            concurrent_requests=1,
            timeout=60,
            retries=3,
            filter_file_extensions=(
                [".md"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
            filter_directories=(
                ["content"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
        )
        self.documents.extend(handbook_loader.load_data(branch="main"))

    def _load_rse_course(self, gh_token: str) -> None:
        """
        Load in the REG RSE course.

        For 'public' index and 'all_data' index.

        Parameters
        ----------
        gh_token : str
            Github token to use to access the RSE course repo.
        """
        owner = "alan-turing-institute"
        repo = "rse-course"

        rse_course_loader = GithubRepositoryReader(
            GithubClient(gh_token, fail_on_http_error=False),
            owner=owner,
            repo=repo,
            verbose=False,
            concurrent_requests=1,
            timeout=60,
            retries=3,
            filter_file_extensions=(
                [".md", ".ipynb"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
        )
        self.documents.extend(rse_course_loader.load_data(branch="main"))

    def _load_rds_course(self, gh_token: str) -> None:
        """
        Load in REG RDS course.

        For 'public' index and 'all_data' index.

        Parameters
        ----------
        gh_token : str
            Github token to use to access the RDS course repo.
        """
        owner = "alan-turing-institute"
        repo = "rds-course"

        rds_course_loader = GithubRepositoryReader(
            GithubClient(gh_token, fail_on_http_error=False),
            owner=owner,
            repo=repo,
            verbose=False,
            concurrent_requests=1,
            timeout=60,
            retries=3,
            filter_file_extensions=(
                [".md", ".ipynb"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
        )
        self.documents.extend(rds_course_loader.load_data(branch="develop"))

    def _load_turing_way(self, gh_token: str) -> None:
        """
        Load in the Turing Way.

        For 'public' index and 'all_data' index.

        Parameters
        ----------
        gh_token : str
            Github token to use to access the Turing Way repo.
        """
        owner = "the-turing-way"
        repo = "the-turing-way"

        turing_way_loader = GithubRepositoryReader(
            GithubClient(gh_token, fail_on_http_error=False),
            owner=owner,
            repo=repo,
            verbose=False,
            concurrent_requests=1,
            timeout=60,
            retries=3,
            filter_file_extensions=(
                [".md"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
        )
        self.documents.extend(turing_way_loader.load_data(branch="main"))

    def _load_hut23(self, gh_token: str) -> None:
        """
        Load in documents from the Hut23 repo.

        For 'all_data' index.

        Parameters
        ----------
        gh_token : str
            Github token to use to access the Hut23 repo.
        """
        owner = "alan-turing-institute"
        repo = "Hut23"

        # load repo
        hut23_repo_loader = GithubRepositoryReader(
            GithubClient(gh_token, fail_on_http_error=False),
            owner=owner,
            repo=repo,
            verbose=False,
            concurrent_requests=1,
            timeout=60,
            retries=3,
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
                    "project-appraisal",
                    "rfc",
                    "team-meetings",
                ],  # we can adjust these
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
        )
        self.documents.extend(hut23_repo_loader.load_data(branch="main"))

        try:
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

        except HTTPError as e:
            logging.error(f"Failed to load Hut23 issues: {e}")

        # load collaborators
        # hut23_collaborators_loader = GitHubRepositoryCollaboratorsReader(
        #     GitHubCollaboratorsClient(gh_token),
        #     owner=owner,
        #     repo=repo,
        #     verbose=True,
        # )
        # self.documents.extend(hut23_collaborators_loader.load_data())

    def _load_wikis(self, gh_token: str) -> None:
        """
        Load in documents from the wikis.

        For 'wikis' index and 'all_data' index.

        Parameters
        ----------
        gh_token : str
            Github token to use to access the research-engineering-group
            and Hut23 repo wikis.
        """
        wiki_urls = [
            f"https://oauth2:{gh_token}@github.com/alan-turing-institute/research-engineering-group.wiki.git",
            f"https://oauth2:{gh_token}@github.com/alan-turing-institute/Hut23.wiki.git",
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

    def create_index(self) -> VectorStoreIndex:
        """
        Create the index vector store.
        """
        # obtain documents
        logging.info(f"Preparing documents for {self.which_index} index...")
        self.prep_documents()

        # create index
        logging.info("Creating index...")
        self.index = VectorStoreIndex.from_documents(
            self.documents, settings=self.settings
        )

        return self.index

    def save_index(self, directory: pathlib.Path | None = None) -> None:
        if directory is None:
            directory = self.data_dir / LLAMA_INDEX_DIR / self.which_index

        # save the settings and persist the index
        logging.info(f"Saving the index in {directory}...")
        self.index.storage_context.persist(persist_dir=directory)
