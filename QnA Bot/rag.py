from langchain.tools import tool
from model import model
from memory import vector_store


@tool
def retrieve_context(query: str) ->str:
    """Retrieve information to help answer a query"""
    # retrieved_docs = vector_store.similarity_search(query, k=2)
    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k":3, "fetch_k":10})
    retrieved_docs = retriever.invoke(query)
    if not retrieved_docs:
        return "No relevant context found."
    serialized = "\n\n".join(
        (f"source: {doc.metadata}\n context: {doc.page_content}")
        for doc in retrieved_docs
    )
    
    return serialized


from langchain.agents import create_agent

tools = [retrieve_context]
prompt = """
You are a helpful assistant answering questions from company policy documents.

You have access to a tool called `retrieve_context`.

Use the tool when needed.

Based on the retrieved context:
- Summarize clearly
- Combine relevant points into a coherent answer

If the answer is not found, say "Don't know".

Do not copy raw text. Produce a clean explanation.
"""

agent = create_agent(model, tools, system_prompt=prompt)

query = input("What do you wanna know")
for event in agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="values",
):
    event["messages"][-1].pretty_print()