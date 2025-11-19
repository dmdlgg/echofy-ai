from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.playlist_creator import create_playlist
from dotenv import load_dotenv
import os

model = ChatOpenAI(model="gpt-5-nano")
agent = create_agent(model=model, tools=[create_playlist])
result = agent.invoke({"messages": [{"role": "user", "content": "quero musicas felizes"}]})
print(result["messages"][-1].content)