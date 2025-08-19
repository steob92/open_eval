from pydantic import BaseModel, ValidationError
from abc import ABC, abstractmethod
from typing import List, Optional
import json

# local
from open_eval.data_types import EvaluationSteps, EvaluationScore, Rubric
from open_eval.models.model_base import ModelBase
from open_eval.data_types.llm_test_case import LLMResponse
from open_eval.prompt_templates import (
    eval_steps_template,
    generic_criteria_template,
    rubric,
    rubric_template
)



from dataclasses import dataclass


@dataclass
class CriteriaResult:
    evaluation_score: EvaluationScore
    criteria_name: str
    criteria_description: str
    llm_input: LLMResponse


class CriteriaBase(ABC):


    def __init__(self, criteria : str, criteria_desc : str, evaluation_steps: Optional[List[str]] = None, rubric: Optional[Rubric] = None):
        self.criteria = criteria
        self.criteria_desc = criteria_desc
        self.rubric = rubric
        if evaluation_steps :
            self._eval_steps = EvaluationSteps.new()
            self._eval_steps.evaluation_steps = evaluation_steps
        else :
            self._eval_steps = None
            

    @property
    def eval_steps(self) -> EvaluationSteps:
        """Get the evaluation steps for this criteria."""
        return self._eval_steps
    
    @eval_steps.setter
    def eval_steps(self, evaluation_steps: EvaluationSteps) -> None:
        """Set the evaluation steps for this criteria."""
        if not isinstance(evaluation_steps, EvaluationSteps):
            raise TypeError("eval_steps must be an instance of EvaluationSteps")
        self._eval_steps = evaluation_steps

    # @abstractmethod
    def format_eval_prompt(self):
        """Format the evaluation generation prompt based on the criteria and description
        
        """
        return eval_steps_template.format(
            criteria = self.criteria, 
            criteria_desc = self.criteria_desc,
        )
    

    def format_rubric_prompt(self, rubric_range:Optional[str] = None):
        """Format the evaluation generation prompt based on the criteria and description
        
        """

        rubric_range = rubric_range or "1-5"
        return rubric_template.format(
            criteria = self.criteria, 
            criteria_desc = self.criteria_desc,
            rubric_min = rubric_range.split("-")[0].strip(),
            rubric_max = rubric_range.split("-")[1].strip()
        )

    def evaluate(
            self,
            model: ModelBase,
            input : Optional[str] = None, 
            response: Optional[str] = None, 
            context: Optional[str] = None
        ) ->  EvaluationScore :
        prompt = generic_criteria_template

        if self.criteria:
            prompt = prompt.replace("{CRITERIA}", self.criteria)
        if self.criteria_desc:
            prompt = prompt.replace("{CRITERIA_DESCRIPTION}", self.criteria_desc)
        # if self._eval_steps:
        #     eval_str = "\n- ".join(self._eval_steps.evaluation_steps)
        #     prompt += f"\nEvaluation Steps: {eval_str}"

        if input:
            prompt = prompt.replace("{INPUT}", "input: ".upper() + input)
        if response:
            prompt = prompt.replace("{RESPONSE}", "response: ".upper() + response)
        if context:
            prompt = prompt.replace("{CONTEXT}", "context: ".upper() + context)

        if self.eval_steps:
            eval_str = "\n- ".join(self.eval_steps.evaluation_steps)
            prompt = prompt.replace("{EVALUATION_STEPS}", f"\nEvaluation Steps: {eval_str}")

        prompt = prompt.replace("{EVALUATION_RUBRIC}", self.rubric if self.rubric else "")
        # print(f"Prompt for evaluation: {prompt}")
        response = model.generate(prompt)
        # print (f"Response from model: {response}")
        try:
            return CriteriaResult(
                evaluation_score=EvaluationScore.from_string(response),
                criteria_name=self.criteria,
                criteria_description=self.criteria_desc,
                llm_input=LLMResponse(input=input, output=response, context=context)
            )
        except ValidationError as e:
            self.logger.error(f"Error parsing evaluation score: {e}")
            print(f"Response: {response}")
            raise ValueError(f"Invalid evaluation score format: {response}") from e
        
        # return prompt

    def generate_evaluation_steps(self, model : ModelBase) -> EvaluationSteps:
        """Generate evaluation steps using the specified model.

        Args:
            model (ModelBase): The model to use for generating evaluation steps.

        Returns:
            EvaluationSteps: The generated evaluation steps.
        """
        prompt = self.format_eval_prompt()
        response = model.generate(prompt)
        # print (response)
        return EvaluationSteps.from_json_str(response) 
    

    def generate_rubric(self, model: ModelBase, rubric_range : Optional[str]= "1-5") -> Rubric:
        """Generate a rubric using the specified model.

        Args:
            model (ModelBase): The model to use for generating the rubric.

        Returns:
            Rubric: The generated rubric.
        """
        prompt = self.format_rubric_prompt(rubric_range=rubric_range)
        print (f"Prompt for rubric generation: {prompt}")
        response = model.generate(prompt)
        print (f"Response from model: {response}")
        data = json.loads(response.strip().replace("```json", "").replace("```", ""))
        descr = [ datum.get('description') for datum in data]
        value = [ float(datum.get('value')) for datum in data]
        print (descr)
        print (value)

        data = {"descriptions" : descr, "values" : value}
        return Rubric(**data)