prompt = """You need to act as an Information extractor. Here is the text: {text}.
From this text above, I need you to provide me with a JSON output which must contain the following things:
User Name
Email
Issue Summary
Urgency level, which can be either of High, Medium or Low only.

You have to analyse the Urgency level from the text provided and make an understandable summary of the Issue.
Don't fake email if not available.

The output provided in JSON should be in this format strictly:
{{
"User Name": "",
"Email": "",
"Issue summary": "",
"Urgency level": "[High, Medium, Low]"
}}

If any of the mentioned things above is not available in the text provided, you need to explicitly write "Data missing" in that section, and rest should be as it should be.
There should not be any clutter, extra information or explaination at start or end of the output.
"""



from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key= api_key)


def call_llm(user_input, prompt=prompt):
    final_prompt = prompt.format(text = user_input)

    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": final_prompt}
        ],
        temperature= 0.7,
        max_tokens=200
    )
    return response.choices[0].message.content

user_input = input("Enter you text: ")
output = call_llm(user_input)

print(output)