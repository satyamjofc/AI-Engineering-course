from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY")
)