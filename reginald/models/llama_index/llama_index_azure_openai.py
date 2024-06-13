import logging
from typing import Any

from llama_index.core import set_global_tokenizer
from llama_index.llms.azure_openai import AzureOpenAI

from reginald.models.llama_index.base import LlamaIndex
from reginald.utils import get_env_var


class LlamaIndexGPTAzure(LlamaIndex):
    def __init__(
        self, model_name: str = "reginald-gpt4", *args: Any, **kwargs: Any
    ) -> None:
        """
         `LlamaIndexGPTAzure` is a subclass of `LlamaIndex` that uses Azure's
        instance of OpenAI's LLMs to implement the LLM.

        Must have the following environment variables set:
        - `OPENAI_API_BASE`: Azure endpoint which looks
          like https://YOUR_RESOURCE_NAME.openai.azure.com/
        - `OPENAI_API_KEY`: Azure API key

        Parameters
        ----------
        model_name : str, optional
            The deployment name of the model, by default "reginald-gpt4"
        """
        openai_azure_api_base = get_env_var("OPENAI_AZURE_API_BASE", secret_value=False)
        if openai_azure_api_base is None:
            raise ValueError(
                "You must set OPENAI_AZURE_API_BASE to your Azure endpoint. "
                "It should look like https://YOUR_RESOURCE_NAME.openai.azure.com/"
            )

        openai_azure_api_key = get_env_var("OPENAI_AZURE_API_KEY")
        if openai_azure_api_key is None:
            raise ValueError("You must set OPENAI_AZURE_API_KEY for Azure OpenAI.")

        # deployment name can be found in the Azure AI Studio portal
        self.deployment_name = model_name
        self.openai_api_base = openai_azure_api_base
        self.openai_api_key = openai_azure_api_key
        self.openai_api_version = "2023-09-15-preview"
        self.temperature = 0.7
        super().__init__(*args, model_name="gpt-4", **kwargs)

    def _prep_llm(self) -> AzureOpenAI:
        logging.info(f"Setting up AzureOpenAI LLM (model {self.deployment_name})")
        return AzureOpenAI(
            model=self.model_name,
            engine=self.deployment_name,
            temperature=self.temperature,
            max_tokens=self.num_output,
            api_key=self.openai_api_key,
            api_base=self.openai_api_base,
            api_type="azure",
            azure_endpoint=self.openai_api_base,
            api_version=self.openai_api_version,
        )

    def _prep_tokenizer(self) -> None:
        import tiktoken

        logging.info(f"Setting up tiktoken tokenizer for model {self.model_name}")
        tokenizer = tiktoken.encoding_for_model("gpt-4").encode
        set_global_tokenizer(tokenizer)
        return tokenizer
