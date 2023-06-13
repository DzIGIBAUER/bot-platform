from langchain.agents import Tool

def run(input: str) -> str:
    pass



tool = Tool(
    name="image-gen",
    description="Use this tool if you want to visualize something. Pass the description of the image to be generated.",
    func=run,
    return_direct=True,
    handle_tool_error=True
)