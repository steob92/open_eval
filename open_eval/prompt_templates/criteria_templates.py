generic_criteria_template = """\
You are given a set of evaluation criteria.

Criteria: {CRITERIA}
Description: {CRITERIA_DESCRIPTION}


{EVALUATION_STEPS}

{EVALUATION_RUBRIC}

{INPUT}

{RESPONSE}

{CONTEXT}


Based on the above, evaluate how well the response meets the criteria. Return your RATIONALE for the SCORE in JSON format, for example:
{
    "rationale" : "One to two sentences detailing the rationale behind your score",
    "score" : "Your score here"
}

Your evaluation:
"""