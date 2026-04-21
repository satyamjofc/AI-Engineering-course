from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

texts = [
    "Football is a popular sport",
    "Investing in stocks is risky",
    "Machine learning models learn patterns",
    "Cooking requires proper ingredients",
]

embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_texts(texts, embeddings)
retriever_chroma = db.as_retriever()

query = input("What to match?:\n")
response = retriever_chroma.invoke(query)
print(response)