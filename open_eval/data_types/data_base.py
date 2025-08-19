from pydantic import BaseModel, ValidationError
import json
from typing import List, Dict, Any


class ScoreLike(BaseModel):

    description: str
    value: float

    @classmethod
    def from_string(cls, json_str : str) -> "ScoreLike":
        try:
            json_str = json_str.replace("```json","").replace("```","")
            return ScoreLike(**json.loads(json_str))
        except Exception as e:
            raise

class ListLikeExtraction(BaseModel):
    """
    A Pydantic model representing a JSON structure.
    """
    extracted : List[str]
    __name__ :str = "ListLikeExtraction"

    @classmethod
    def from_dict(cls, input: Dict[str, Any])-> "ListLikeExtraction":
        try:
            key = list(input.keys())[0]
            input["extracted"] = input.pop(key)
            return cls(**input)
        except ValidationError:
            print (f"Error parsing input: {input}"
                   f" with error: {ValidationError}")
            raise ValueError(f"Invalid input format: {input}")

    @classmethod
    def new(cls) -> "ListLikeExtraction":
        return cls(**{"extracted" : []})

    @classmethod
    def from_json_str(cls, json_str: str) -> "ListLikeExtraction":
        """
        Create an instance of ListLikeExtraction from a JSON string.

        Args:
            json_str (str): A JSON string representing the evaluation steps.

        Returns:
            ListLikeExtraction: An instance of the ListLikeExtraction class.
        """
        try:
            data = json.loads(json_str.replace("```json","").replace("```", ""))
            return cls.from_dict(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")


    def __str__(self):
        return f"{self.__name__} = [\n\t" + ",\n\t".join(self.extracted) + "\n]"
