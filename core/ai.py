import os

import dotenv
import google.generativeai as genai

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_content(prompt: str):
    response = model.generate_content(prompt) if prompt else None
    return response.text if response else "..."
