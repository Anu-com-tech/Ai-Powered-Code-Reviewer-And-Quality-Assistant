from groq import Groq

# TEMPORARY: hardcode key to avoid Streamlit secrets issues
client = Groq(api_key="gsk_xxxxxxxxxxxxxxxxxxxxxxxxx")

def call_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You generate Python docstrings."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return (
            "Generates documentation describing the purpose and behavior "
            "of the function based on its implementation."
        )
# core/docstring_engine/llm_integration.py

def generate_docstring_content(fn: dict):
    # dummy function for tests
    return "Generated docstring"




