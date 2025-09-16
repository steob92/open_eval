extract_facts : str = """<START OF INSTRUCTIONS>
You are an expert fact extractor, whose role is to extract facts from a given text.
You will be provided with a text, which is the content from which to extract facts.
A fact is a statement that can be verified as true or false, with a clear and unambiguous meaning.
Your task is to carefully read the text and extract all relevant facts.
You should output your results in json format, with a list of the extracted facts.
Do not include any opinions, interpretations, or subjective statements.
Do not make up any facts that are not present in the text.

Consider the following example:

Text: "The colour of the sky is blue. The freezing point of water is 0 degrees Celsius. The Earth revolves around the Sun. The Earth sometimes smells like apples."

Extracted facts:
{{
    "extracted facts" : [
        "The sky is blue.",
        "Water freezes at 0 degrees Celsius.",
        "The Earth revolves around the Sun."
    ]
}}
<END OF INSTRUCTIONS>
Text: "{text}"
Extracted facts:
"""



extract_assertions : str = """ <start of instructions>
You are an expert assertion extractor, whose role is to extract assertions from a given text.
You will be provided with a text, which is the content from which to extract assertions.
An assertion is a statement that expresses a belief, opinion, or claim, which may or may  not be verifiable.
Your task is to carefully read the text and extract all relevant assertions.
You should output your results in json format, with a list of the extracted assertions.
Do not include any facts, interpretations, or subjective statements.
Do not make up any assertions that are not present in the text.
Consider the following example:

Text: "The sky is blue. I believe that the sky is blue. The freezing point of water is 0 degrees Celsius. I think that the Earth revolves around the Sun."
Extracted assertions:
{{
    "extracted assertions" : [
        "I believe that the sky is blue.",
        "I think that the Earth revolves around the Sun."
    ]
}}
<end of instruction>
Text: "{text}"

Extracted assertions:
"""