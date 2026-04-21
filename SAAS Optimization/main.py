from langchain.tools import tool
from langchain.agents import create_agent
from model import model

@tool
def retrieve_context():
    pass


tools = [retrieve_context]

prompt="""
"""

agent = create_agent(model, tools, system_prompt=prompt)

query = input("Give me your audit:\n\n")
for event in agent.stream(
    {"messages": [{"role":"user", "content": query}]}
):
    event["messages"][-1].pretty_print()