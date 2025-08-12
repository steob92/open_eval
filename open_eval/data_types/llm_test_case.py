from pydantic import BaseModel, ValidationError
import json
from typing import List, Dict, Any, Optional


class LLMResponse(BaseModel):

    input : Optional[str]
    output : Optional[str]
    context : Optional[str]


    def __call__(self, *args: Any, **kwargs: Any) -> str:
        ret = {}
        if self.input is not None:
            ret["input"] = self.input
        if self.output is not None:
            ret["output"] = self.output
        if self.context is not None:
            ret["context"] = self.context
        return ret
