eval_steps_template :str = """ <START OF INSTRUCTIONS>
You are an expert evaluator, whose role is to determine the steps to best evaluate a criteria.
You will be provided with a criteria, which is the title of the criteria to evaluate on, and a description of that criteria (criteria description).
You task is to carefully read the criteria and the criteria description and to determine steps on which to evaluate the criteria.
These steps will be used to determine a score for this criteria.
You should output your results in json format, with a list of the evaluation steps. 
Consider the following example:

Criteria: Clarity
Criteria description: How clear and easy to understand is the RESPONSE. Is it free of complicated jargon?

Evaluation steps:
{{
    "evaluation_steps" : [
        "Carefully read and understand the RESPONSE.",
        "Check check if there are any grammatical mistakes in the RESPONSE.".
        "Determine if the language used in the RESPONSE is easy to understand for an average user.",
        "Determine if there is any unnessicary jargo used in the RESPONSE that might confused the average user.",
        "Determine a score between 1-5 where 1 means the RESPONSE is unclear and 5 means the RESPONSE is clear and understandable."
    ]
}}


<END OF INSTRUCTIONS>

Criteria: {criteria}
Criteria description: {criteria_desc}

Evaluation steps:
"""