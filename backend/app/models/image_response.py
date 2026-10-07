from pydantic import BaseModel


class ImageResponse(BaseModel):
    image: str
