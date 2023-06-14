from typing import Any
from langchain.tools import BaseTool

import json
import openai


class ImageGenerationTool(BaseTool):
    name="image-gen"
    description=(
        "Use this tool if you want to visualize something. When describing the image to be generated provice the folliwing as a string:"
        "Subject represented by nouns suggests what scene to generate."
        "Description implies additional information related to the subject such as adjectives (stunning, lovely), background description, etc."
        "Always end with 'photograph from disposable camera'"
    )
    return_direct=True
    handle_tool_error=True

    def _run(self, query: str, *args: Any, **kwargs: Any) -> str:
        response = openai.Image.create(
            prompt=query,
            n=1,
            size="1024x1024"
        )
        
        print(response)

        return json.dumps({
            "image_url": response['data'][0]['url']
        })
    
    def _arun(self, *args: Any, **kwargs: Any):
        raise NotImplemented()
