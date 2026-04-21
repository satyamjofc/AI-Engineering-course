from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# loading
loader = PyPDFLoader("data.pdf")
docs = loader.load()

# chunking
split = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 100,
)
all_splits = split.split_documents(docs)

# embedding
embeddings = HuggingFaceBgeEmbeddings(model_name = "all-MiniLM-L6-v2")
# vectorize
vector_store = InMemoryVectorStore(embeddings)
vector_store.add_documents(all_splits)
# store
# document_ids = vector_store.add_documents(all_splits)

# retrieval
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k":3, "fetch_k":10})

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_template("""Answer the given question by the user, from the provided context.
DO NOT give answer, if the answer is not available in the given context, Insted write, "Answer not known".
                                          
Here is the context:
{context}
                                          
Question:
{question}""")

question = input("What's your Question:\n")

retriever_docs = retriever.invoke(question)
context = "\n\n".join([doc.page_content for doc in docs])

chain = prompt | model
response = chain.invoke({
    "context": context,
    "question": question
})

print(response.content)