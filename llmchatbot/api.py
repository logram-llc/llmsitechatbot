from fastapi import FastAPI
from pydantic import BaseModel
from llmchatbot.chatbot import Chatbot


class ChatbotQuery(BaseModel):
    message: str


app = FastAPI()
chatbot: Chatbot | None = None


@app.post("/")
def query(message: ChatbotQuery) -> dict[str, str | None]:
    if not chatbot:
        raise ValueError("Chatbot not initialized")
    response = chatbot.query(message.message)
    return {"message": response}
