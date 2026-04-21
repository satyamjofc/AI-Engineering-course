from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma, DocArrayInMemorySearch

# docs
docs = [
    Document(page_content="Football is a popular sport"),
    Document(page_content="Investing in stocks is risky"),
    Document(page_content="Machine learning models learn patterns"),
    Document(page_content="Cooking requires proper ingredients"),
]

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db_chroma = Chroma.from_documents(docs, embedding)
retriever_chroma = db_chroma.as_retriever()

db_memory = DocArrayInMemorySearch.from_documents(docs, embedding)
retriever_memory = db_memory.as_retriever()

query = "How to learn AI?"

print("Chroma Results:")
for doc in retriever_chroma.invoke(query):
    print("-", doc.page_content)

print("\nMemory Results:")
for doc in retriever_memory.invoke(query):
    print("-", doc.page_content)