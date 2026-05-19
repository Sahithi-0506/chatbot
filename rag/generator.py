from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config import GEMINI_MODEL


def generate_answer(prompt_data: dict) -> str:
    model = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.3)
    prompt = PromptTemplate.from_template(prompt_data["template"])
    response = (prompt | model).invoke(prompt_data["values"])
    return response.content
