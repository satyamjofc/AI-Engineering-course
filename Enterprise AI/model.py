from langchain_groq import ChatGroq
from langchain.tools import tool
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from vector_store import db

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=1024
)

@tool("context_retriever", description="tool to search from given PDFs")
def retrieve_context(query: str) ->str:
    """Retrieve information to help answer a query"""
    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k":3, "fetch_k":10, "filer": {"type": "pdf"}})
    retrieved_docs = retriever.invoke(query)
    if not retrieved_docs:
        return "No relevant context found."
    serialized = "\n\n".join(
        (f"source: {doc.metadata}\n context: {doc.page_content}")
        for doc in retrieved_docs
    )
    
    return serialized


tools = [retrieve_context]

prompt = """
You are a helpful assistant answering questions for an Enterprise employees.

You have access to a tool called `retrieve_context`.

Use the tool when needed.

- Answer based on the retrieved context only.
- Combine relevant points into a coherent answer.
- Do not infer or guess
- Do not add your own extra infromation beyond the context provided

If the answer is not found, say "Don't know".

Do not copy raw text. Produce a clean explanation.
"""

agent = create_agent(llm, tools, system_prompt=prompt)


while True:
    query = input("What do you wanna know (type 'exit' to quit): ").strip()

    if query.lower() in {"exit", "quit"}:
        print("Exiting...")
        break

    try:
        for event in agent.stream(
            {"messages": [{"role": "user", "content": query}]},
            stream_mode="values",
        ):
            event["messages"][-1].pretty_print()
    except Exception as e:
        print(f"Error: {e}")


def generate_answer():
    pass