from pydantic import BaseModel


class ChatResponse(BaseModel):
    """
    Represents the chatbot response.
    """

    answer: str