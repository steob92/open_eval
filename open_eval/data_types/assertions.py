import json
from typing import List

from .data_base import ListLikeExtraction

class Assertions(ListLikeExtraction):
    """
    A Pydantic model representing a JSON structure.
    """
    __name__ = "extracted_assertions"

    @property
    def assertions(self)-> List[str]:
        return self.extracted
    
    @assertions.setter
    def assertions(self, assertions:List[str])->None:
        self.extracted = assertions

