import json
from typing import List, Dict, Any
from .data_base import ListLikeExtraction

class ExtractedFacts(ListLikeExtraction):
    """
    Class for extracted facts
    """

    __name__ = "extracted_facts"

    @property
    def facts(self)-> List[str]:
        return self.extracted
    
    @facts.setter
    def facts(self, facts:List[str])->None:
        self.extracted = facts

