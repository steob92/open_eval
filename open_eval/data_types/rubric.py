import json
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel, ValidationError

from .data_base import ListLikeExtraction, ScoreLike

class Rubric(BaseModel):
    descriptions: List[str]
    values: List[int]

    def __str__(self):
        ret = "\n*"
        ret += "\n*".join([f" {val} : {desc}" for desc, val in zip(self.descriptions, self.values)])
        return ret