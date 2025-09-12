import google.generativeai as genai
from src.config import GEMINI_API_KEY,GROQ_API_KEY
from groq import Groq

def ask_groq(prompt:str)->str:
    """Send a natural language query to Groq and get back a response."""

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()


def ask_gemini(prompt:str)-> str:
    """Send a natural language query to gemini and get back a response."""
    genai.configure(api_key=GEMINI_API_KEY)
    llm1 = genai.GenerativeModel("gemini-2.5-flash")
    response = llm1.generate_content(prompt)

    return response.text.strip()



    