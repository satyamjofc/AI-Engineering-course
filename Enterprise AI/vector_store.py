from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from loader import docs, split_docs

embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_documents(docs, embeddings)
retriever_chroma = db.add_documents(documents=split_docs)