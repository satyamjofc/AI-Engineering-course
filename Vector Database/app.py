from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader("data.pdf")
docs = loader.load()

split = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
)
all_splits = split.split_documents(docs)

embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_documents(docs, embeddings)
db.add_documents(all_splits)

query = input("What to Search?:\n").strip().lower()

response = db.similarity_search(query, k=3)

print(response)