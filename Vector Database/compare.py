from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

texts = [
    "Football",
    "Investing",
    "Machine",
    "Cooking",
]

embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_texts(texts, embeddings)
retriever_chroma = db.as_retriever()

query = input("What to match?:\n")
response = retriever_chroma.invoke(query)
print(response)

def search(query, texts = texts):
    result=[]
    for text in texts:
        if query.lower() in text.lower():
            result.append(text)
    return result
response2 = search(query)
print(response2)