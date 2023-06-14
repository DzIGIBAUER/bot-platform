from langchain.agents.conversational_chat.output_parser import ConvoOutputParser
from langchain.schema import AgentAction, AgentFinish, OutputParserException
from langchain.output_parsers.json import parse_json_markdown
import json

FORMAT_INSTRUCTIONS = """
When responding to user MAKE SURE to use the following syntax:
```json
{{{{
"text": "Your response goes here."
}}}}
```
When using a tool MAKE SURE to use the following syntax:
Make sure BOTH `tool` and `input` keys are present.
```json
{{{{
"tool": "Place name of the tool here",
"input": "Place input for the tool here"
}}}}
```
REPLY WITH NOTHING ELSE EXCEPT THE JSON OBJECT
"""



class OutputParser(ConvoOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> AgentAction | AgentFinish:
        try:
            response = parse_json_markdown(text)

            if response.get("text"):
                return AgentFinish({"output": json.dumps(response)}, text)
            else:
                return AgentAction(response["tool"], response["input"], text)
            
        except Exception as e:
            raise OutputParserException(f"Could not parse LLM output: {text}") from e
