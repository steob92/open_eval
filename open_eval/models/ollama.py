import logging
import asyncio

from ollama import chat
from ollama import ChatResponse

from .model_base import ModelBase



OLLAMA_DEFAULT_MODEL = "gemma3:1b"

class OllamaModel(ModelBase):
    def __init__(self, base_url: str = "http://localhost:11434/api/generate", model: str = None, name : str = None):


        if model is None:
            model = OLLAMA_DEFAULT_MODEL
        if name is None:
            name = f"Ollama-{model}"

        super().__init__(name=name)



        self.base_url : str = base_url
        self.model : str = model
        self.logger.info(f"Initialized with model {self.model}")

    def generate(self, message: str) -> str:

        self.logger.debug(f"Generating response for input: {message}")
        response : ChatResponse = chat(
            model=self.model, 
            messages=[
                {"role": "user", "content": message}
                ],
                stream = False,
                think = self.think,
            )
        
        return response.message["content"]

    async def a_generate(self, message: str) -> str:
        self.logger.debug(f"Generating async response for input: {message}")
        loop = asyncio.get_event_loop()
        response: ChatResponse = await loop.run_in_executor(
            None,
            lambda: chat(
                model=self.model,
                messages=[{"role": "user", "content": message}],
                stream=False,
                think=self.think,
            )
        )
        return response.message["content"]


