import json
from typing import TypedDict
from langchain import LLMChain
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.tools import DuckDuckGoSearchRun

from chatbot.models import Chatbot

from .output_parser import OutputParser
from .prompts import SUFFIX, SYSTEM, TEMPLATE_TOOL_RESPONSE
from .tools import tts

import logging

logging.basicConfig(level=logging.DEBUG)

llm = ChatOpenAI()


class ChatbotResponse(TypedDict):
    response: str | None
    audio_url: str | None
    audio_text: str | None


static_tools = [
    DuckDuckGoSearchRun()
]



def generate_response(chatbot: Chatbot, input: str, user: str | None = None, history: list[BaseMessage] | None = None) -> ChatbotResponse:
    
    tools = [
        tts.TextToSpeechTool(voice_name=chatbot.voice_name)
    ] + static_tools

    chat_history = ChatMessageHistory(messages=history)

    prompt = ConversationalChatAgent.create_prompt(
        tools,
        system_message="",
        human_message=SYSTEM + "\n" + SUFFIX,
        output_parser=OutputParser(),
        input_variables=["input", "chat_history", "agent_scratchpad", "behaviour", "name"]
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="input",
        ai_prefix=chatbot.name,
        human_prefix=user or "Human",
        return_messages=True,
        chat_memory=chat_history
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = ConversationalChatAgent(llm_chain=llm_chain, tools=tools, verbose=True, output_parser=OutputParser(), template_tool_response=TEMPLATE_TOOL_RESPONSE)
    agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)

    results = agent_chain.run(
        input=input,
        name=chatbot.name,
        behaviour=chatbot.behaviour
    )

    return json.loads(results)