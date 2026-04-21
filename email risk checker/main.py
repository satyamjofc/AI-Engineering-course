import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
load_dotenv()

final_prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a corporate email compliance assistant.

Your job is to analyze outgoing business emails and detect risks related to:
- Legal commitments
- Pricing errors or misleading financial statements
- Confidential or sensitive business information
- NDA violations
- Exposure of personal data (emails, phone numbers, addresses)
- Unprofessional or insulting language
- Overpromising or guarantees

You must be strict, realistic, and business-aware. Do not ignore subtle risks.

------------------------
OUTPUT FORMAT (STRICT JSON ONLY)
------------------------

Return ONLY valid JSON in the following structure:

{{
  "risks": [
    {{
      "type": "<risk category>",
      "text_snippet": "<exact risky part of the email>",
      "why_risk": "<clear explanation>",
      "suggestion": "<improved safer wording>",
      "severity": <integer from 1 to 10>
    }}
  ],
  "overall_severity": <integer from 1 to 10>
}}

------------------------
RULES
------------------------

1. If no risks are found, return:
{{
  "risks": [],
  "overall_severity": 1
}}

2. Severity guidelines:
- 1-3 → minor tone or wording issue
- 4-6 → moderate business risk
- 7-8 → serious legal/compliance concern
- 9-10 → critical risk (legal exposure, data breach, binding commitment)

3. Be precise:
- Always extract the exact problematic phrase as "text_snippet"
- Do NOT rewrite the entire email

4. Suggestions must:
- Preserve intent
- Reduce legal or business risk
- Sound professional

5. Do NOT include any explanation outside JSON.

------------------------
EXAMPLES
------------------------

Example Input:
"We guarantee delivery by tomorrow and will refund 100% if not."

Example Output:
{{
  "risks": [
    {{
      "type": "Legal Commitment",
      "text_snippet": "We guarantee delivery by tomorrow",
      "why_risk": "Creates a binding promise that may expose the company to liability if unmet.",
      "suggestion": "We aim to deliver by tomorrow, subject to operational conditions.",
      "severity": 8
    }}
  ],
  "overall_severity": 8
}}
6. DO NOT hallucinate or modify text.
- "text_snippet" must be copied EXACTLY from the input email.
- Do not paraphrase or invent phrases.

7. Use ONLY the following risk categories:
- Legal Commitment
- Pricing Issue
- Confidential Information
- NDA Violation
- Personal Data Exposure
- Unprofessional Language
- Overpromising

Do not create new category names.

8. Do not misclassify:
- Refunds, guarantees → Legal Commitment or Overpromising
- Prices → Pricing Issue

9. Suggestions must:
- Only rephrase the risky sentence
- NOT change business policy (e.g., do not replace refund with partial refund)
     
"""),

    ("human", "Analyze the following email:\n\n{email}")
])


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

def call_llm(email):
    chain = final_prompt | llm
    response = chain.invoke({
        "email": email
    })
    parsed = json.loads(response.content)
    save_report(email, parsed)
    return response.content.strip()


FILE_PATH = "reports.json"
def save_report(email, analysis):
    record = {
        "timestamp": datetime.now().isoformat(),
        "email": email,
        "analysis": analysis
    }

    # if file exists → append
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=2)


email= input("Paste your email here:\n\n")

response = call_llm(email)
print(response)