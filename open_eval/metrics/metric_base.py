from abc import ABC, abstractmethod


class MetricBase(ABC):
    """
    Abstract base class for evaluation metrics.
    Metrics evaluate a (prompt, response, context) triplet based on a specific criterion.
    """

    @abstractmethod
    def evaluate(self, data : Union[List[MetricData], MetricData], criteria) -> float:
        """
        Evaluate the (prompt, response, context) triplet.

        Args:
            prompt (str): The input prompt.
            response (str): The generated response.
            context (str): Additional context for evaluation.

        Returns:
            float: The evaluation score based on the metric's criterion.
        """
        pass