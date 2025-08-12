

from open_eval.criteria.criteria_base import CriteriaBase
from open_eval.data_types.llm_test_case import LLMResponse
from open_eval.models.model_base import ModelBase
from open_eval.data_types import EvaluationScore
from typing import List, Optional, Union
import logging
import asyncio



async def _evaluate_async(criterion, resp, model):
    loop = asyncio.get_event_loop()
    
    # If criterion.evaluate is async, await it directly
    if asyncio.iscoroutinefunction(criterion.evaluate):
        return await criterion.evaluate(
            model=model,
            input=resp.input,
            response=resp.output,
            context=resp.context
        )
    # Otherwise, run it in a thread pool to avoid blocking
    return await loop.run_in_executor(
        None,
        lambda: criterion.evaluate(
            model=model,
            input=resp.input,
            response=resp.output,
            context=resp.context
        )
    )


class Evaluator():

    def __init__(self, criteria: CriteriaBase | List[CriteriaBase]):
        if isinstance(criteria, CriteriaBase):
            self.criteria = [criteria]
        else:
            self.criteria = criteria



    async def _batch_evaluate(self, llm_response, model):
        tasks = [
            _evaluate_async(criterion, resp, model)
            for resp in llm_response
            for criterion in self.criteria
        ]
        return await asyncio.gather(*tasks)
    

    async def a_evaluate(
        self, 
        model: ModelBase, 
        llm_response: Union[LLMResponse, List[LLMResponse]], 
        batch_size: int = 8
    ):
        if not isinstance(llm_response, list):
            llm_response = [llm_response]

        all_scores = []
        for i in range(0, len(llm_response), batch_size):
            logging.info(
                f"Evaluating batch {i // batch_size + 1}: size {len(llm_response[i:i + batch_size])} "
                f"(items {i} to {min(i + batch_size, len(llm_response)) - 1})"
            )
            batch = llm_response[i:i + batch_size]
            scores = await self._batch_evaluate(batch, model)
            all_scores.extend(scores)
        return all_scores

    def evaluate(
        self, 
        model: "ModelBase", 
        llm_response: "LLMResponse | list[LLMResponse]", 
        batch_size: int = 8
    ):
        """Sync wrapper for a_evaluate, asyncio-only."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop: safe to run directly
            return asyncio.run(self.a_evaluate(model, llm_response, batch_size))
        else:
            # Already in a running loop — can't block without threads
            raise RuntimeError(
                "Cannot call evaluate() from inside async code. "
                "Use `await a_evaluate(...)` instead."
        )