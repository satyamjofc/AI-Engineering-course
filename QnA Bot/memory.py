from langchain_core.vectorstores import InMemoryVectorStore
from embedding import embeddings
from chunking import all_splits

vector_store = InMemoryVectorStore(embeddings)

documents_ids = vector_store.add_documents(documents=all_splits)
# print(documents_ids[:3])