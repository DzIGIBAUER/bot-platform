SUFFIX = """
If you don't poses information required to properly respond to user questions you can use following tools:
{{tools}}

{format_instructions}

Reply to this: {{{{input}}}}
DO NOT include ANYTHING else in response except for the json object.
"""


SYSTEM = """
You are in a simulation where you roleplay a character. Your character is name {{{{name}}}}.
{{{{behaviour}}}}
"""

TEMPLATE_TOOL_RESPONSE = """Some more data that could help you reply: 
{observation}
Remember to follow reply instructions.
"""
