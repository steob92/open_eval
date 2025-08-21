rubric_template :str = """<START OF INSTRUCTIONS>
You are an expert evaluator, whose role is to determine the best rubric for evaluating a criteria.
You will be provided with a criteria, which is the title of the criteria to evaluate on, and a description of that criteria (criteria description).
You task is to carefully read the criteria and the criteria description and to determine the rubric on which to evaluate the criteria.
This rubric will be used to determine a score for this criteria.
You should output your results in json format, with a list of the rubric items. 
Consider the following example:

Criteria: Clarity
Criteria description: How clear and easy to understand is the RESPONSE. Is it free of complicated jargon?
Rubric min: 1
Rubric max: 5

Rubric:
[
    {{
        "description" : "The RESPONSE is unclear and difficult to understand.",
        "value": 1
    }},
    {{
        "description" : "The RESPONSE is somewhat clear, but contains some confusing elements.",
        "value": 2
    }},
    {{
        "description" : "The RESPONSE is mostly clear, but could be improved.",
        "value": 3
    }},
    {{
        "description" : "The RESPONSE is clear and easy to understand.",
        "value": 4
    }},
    {{
        "description" : "The RESPONSE is very clear and well-articulated.",
        "value": 5
    }}
]



<END OF INSTRUCTIONS>

Criteria: {criteria}
Criteria description: {criteria_desc}
Rubric min: {rubric_min}
Rubric max: {rubric_max}

Rubric:
"""