from pydantic import BaseModel, Field


class ImageRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=1200)
