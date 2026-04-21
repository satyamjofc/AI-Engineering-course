from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from model import model
import json

def format_prompt(code_chunk):
    return [
        {
            "role": "system",
            "content": f"""You are a senior software engineer performing a professional code review.

                        Your job is to analyze the given code and provide precise, actionable feedback.
                        - Focus on correctness, robustness, and maintainability over minor stylistic suggestions.

                        Strict rules:
                        - Only comment on what is visible in the provided code.
                        - Do NOT assume missing context.
                        - If something depends on external code, say "Insufficient context".
                        - Avoid generic advice like "improve readability" unless you give a concrete suggestion.
                        - Be concise but specific.
                        - Do NOT report issues that are language-specific unless they are actually valid for the given language.
                        -Avoid theoretical or unlikely issues (e.g., integer overflow in Python).
                        - Only report issues that are realistic and meaningful in practice.
                        - Prefer high-signal issues over trivial suggestions.
                        - If no real bugs are present, return an empty bugs list.
                        Return ONLY valid JSON. Do not include explanations, markdown, or extra text."""
        },
        {
            "role": "user",
            "content": f"""Review the following code chunk. This may be a partial code snippet. If context is missing, say "Insufficient context".

                        Code:
                        {code_chunk}

                        Provide output in the following structured format:

                        {{
                            "summary": "Brief explanation of what this code does",

                            "bugs": [
                                {{
                                  "issue": "...",
                                  "reason": "...",
                                  "severity": "low | medium | high"
                                }}
                                  ],

                                  "performance": [
                                    {{
                                      "issue": "...",
                                      "suggestion": "..."
                                    }}
                                      ],

                                  "security": [
                                    {{
                                      "issue": "...",
                                      "risk": "..."
                                    }}
                                      ],

                                  "readability": [
                                    {{
                                      "issue": "...",
                                      "suggestion": "..."
                                    }}
                                      ]
                        }}"""
        }
    ]


splitters = {
    "python": RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=500, chunk_overlap=100
    ),
    "javascript": RecursiveCharacterTextSplitter.from_language(
        language=Language.JS, chunk_size=500, chunk_overlap=100
    ),
    "java": RecursiveCharacterTextSplitter.from_language(
        language=Language.JAVA, chunk_size=500, chunk_overlap=100
    ),
    "cpp": RecursiveCharacterTextSplitter.from_language(
        language=Language.CPP, chunk_size=500, chunk_overlap=100
    ),
    "ruby": RecursiveCharacterTextSplitter.from_language(
        language=Language.RUBY, chunk_size=500, chunk_overlap=100
    ),
}

# language = input("Input the language of your code : ").strip().lower()
# code_input = input("Paste your code here:\n")
language = "python"
code_input = """num = int(input("Enter a number: "))
                n = num
                power = len(str(num))
                total = 0

                while n > 0:
                    digit = n % 10
                    total += digit ** power
                    n //= 10

                if total == num:
                    print("Armstrong Number")
                else:
                    print("Not an Armstrong Number")"""

if language not in splitters:
    raise ValueError("Unsupported language. Choose from: python, javascript, java, cpp, ruby")

splitter = splitters[language]
chunks = splitter.create_documents([code_input])

all_reviews = []

def call_llm(messages):
    response = model.invoke(messages)
    return response.content.strip()

for chunk in chunks:
    messages = format_prompt(chunk.page_content)
    response = call_llm(messages)
    try:
        parsed = json.loads(response)
        print(parsed)
    except Exception as e:
        print("JSON ERROR:", e)
        print("RAW RESPONSE:", response)
    # all_reviews.append(response)
print(all_reviews)