import json
from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError

from .data_base import ListLikeExtraction, ScoreLike


class EvaluationSteps(ListLikeExtraction):
    """
    A Pydantic model representing a JSON structure.
    """
    __name__ = "evaluation_steps"

    @property
    def evaluation_steps(self)-> List[str]:
        return self.extracted
    
    @evaluation_steps.setter
    def evaluation_steps(self, evaluation_steps:List[str])->None:
        self.extracted = evaluation_steps

class EvaluationScore(BaseModel):

    rationale : str
    score : float

    @classmethod
    def from_string(cls, json_str : str) -> "EvaluationScore":
        try:
            json_str = json_str.replace("```json","").replace("```","")
            return EvaluationScore(**json.loads(json_str))
        except Exception as e:
            raise


    def __str__(self):
        return f"EvaluationScore(\n{{\n\t description={self.description}, \n\t value={self.value}\n}})"