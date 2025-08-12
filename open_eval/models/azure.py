import logging
import asyncio

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage


from .model_base import ModelBase




class AzureModel(ModelBase):
    def __init__(self, endpoint: str, model: str, api_key : str, name : str = None):


        if model is None:
            model = AZURE_DEFAULT_MODEL
        if name is None:
            name = f"Azure-{model}"

        super().__init__(name=name)

        self.default_parameters = {
            # "max_completion_tokens" : 13107,
            "temperature" : 1.0,
            "top_p" : 1.0,
            "frequency_penalty" : 0.0,
            "presence_penalty" : 0.0,
        }

        self.endpoint : str = endpoint
        self.model : str = model
        self.client = ChatCompletionsClient(
            endpoint = self.endpoint,
            credential =  AzureKeyCredential(api_key),
        )
        self.logger.info(f"Initialized with model {self.model}")

    def generate(self, message: str) -> str:

        self.logger.debug(f"Generating response for input: {message}")
        response  = self.client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content=message),
            ],
            model=self.model,
            **self.default_parameters
        )

            
        return response.choices[0].message["content"]

    async def a_generate(self, message: str) -> str:
        self.logger.debug(f"Generating async response for input: {message}")
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content=message),
            ],
            model=self.model,
            **self.default_parameters
            )

        )
        return response.choices[0].message["content"]


