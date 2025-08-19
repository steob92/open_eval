import json
import logging
import asyncio

from open_eval.models.ollama import OllamaModel
from open_eval.models.azure import AzureModel
from open_eval.prompt_templates.evaluation_steps import eval_steps_template
from open_eval.data_types.evaluation import EvaluationSteps
from open_eval.criteria.criteria_base import CriteriaBase
from open_eval.data_types.llm_test_case import LLMResponse
from open_eval.evaluator.evaluator import Evaluator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)



def main():


    criteria = "Completeness"
    criteria_desc = "How complete and thorough is the RESPONSE? Does it address all aspects of the INPUT?"
    formatted_eval_steps = eval_steps_template.format(criteria=criteria, criteria_desc=criteria_desc)
    # model = OllamaModel()
    model = OllamaModel(model = "gemma3:4b")
    # # ollama = OllamaModel(model = "qwen3:0.6b")
    # model = OllamaModel(model = "qwen3:4b")
    # # ollama = OllamaModel(model = "deepseek-r1:7b")
    # # ollama = OllamaModel(model = "deepseek-r1:1.5b")
    model.think = False
    # response = ollama.generate(formatted_eval_steps)
    # print("Raw response from model:")
    # print(response)
    # response = response.replace("\n", "").replace("```json", "").replace("```", "").strip()
    # steps = EvaluationSteps.from_dict(json.loads(response))
    # print(steps)


    # azure = AzureModel(
    #     endpoint = ,
    #     api_key = ,
    #     model =
    # )

    # res = model.generate("What is the weather like in Paris?")
    # print("Response from Azure:")
    # print(res)
    my_criteria = CriteriaBase(
        criteria=criteria, 
        criteria_desc=criteria_desc,
        # evaluation_steps=steps.evaluation_steps
    )


    my_criteria.eval_steps = my_criteria.generate_evaluation_steps(model)
    my_criteria.rubric = my_criteria.generate_rubric(model)
    print("Generated rubric:")
    print (my_criteria.rubric)

    # my_criteria_2 = CriteriaBase(
    #     criteria="Relevance", 
    #     criteria_desc="How relevant is the RESPONSE to the INPUT? Does it stay on topic and address the main points?",
    #     # evaluation_steps=steps.evaluation_steps
    # )


    # my_criteria_2.eval_steps = my_criteria_2.generate_evaluation_steps(model)
    # # print("Generated evaluation steps:")
    # # print(my_criteria.eval_steps)
    # # print(f"my_eval_steps : {my_criteria.eval_steps}")

    llm_test_case = [ LLMResponse(
        input="What is the capital of France?",
        output="The capital of France is Berlin.",
        context="There are multiple cities in France. Paris is the most well-known and is often considered the capital. Berlin is also a significant city in Europe."
    ) for i in range(2) ]


    my_evaluator = Evaluator([my_criteria])

    scores = my_evaluator.evaluate(model = model, llm_response=llm_test_case)
    print ("Evaluation scores:")
    print(scores)
    # # print (scores[0].evaluation_score.score)
    # # print (scores[0].evaluation_score.rationale)
if __name__ == "__main__":
    main()
