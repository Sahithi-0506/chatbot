from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config import GEMINI_MODEL


def rewrite_query(question: str, chat_history: list) -> str:
    if not chat_history:
        return question

    history = "\n".join(
        [f"User: {chat['question']}\nAssistant: {chat['answer']}" for chat in chat_history[-2:]]
    )

    prompt = PromptTemplate.from_template("""
Rewrite the user's current question into a clear standalone search query for retrieving academic PDF content.
Do not answer the question. Only rewrite it.

Previous conversation:
{history}

Current question:
{question}

Standalone search query:
""")

    model = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.1)
    response = (prompt | model).invoke({"history": history, "question": question})
    return response.content.strip()
