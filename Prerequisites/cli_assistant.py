from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


final_prompt = ChatPromptTemplate.from_template("""
You are an assistant. Answer the following question in technical terms.
Do NOT add any extra text or explanation outside the answer.

Question: {question}
""")


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.1,
    api_key=os.getenv("GROQ_API_KEY")
)


def call_llm(question):
    chain = final_prompt | llm
    response = chain.invoke({
        "question": question
    })

    return response.content.strip()
    

question = input("Enter you Question: ")

response = call_llm(question)
print(response)