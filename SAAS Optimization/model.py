import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from output_schema import schema

load_dotenv()


model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY")
)

structured_model = model.with_structured_output(schema)