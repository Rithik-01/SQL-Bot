import google.generativeai as genai
from config import GEMINI_API_KEY


def ask_gemini(prompt:str)-> str:
    """Send a natural language query to gemini and get back a response."""

    genai.configure(api_key=GEMINI_API_KEY)
    llm = genai.GenerativeModel("gemini-2.5-flash")
    response = llm.generate_content(prompt)

    return response.text.strip()



    