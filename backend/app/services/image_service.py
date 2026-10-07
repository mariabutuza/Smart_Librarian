from openai import OpenAI

from app.config import IMAGE_MODEL, OPENAI_API_KEY


class ImageService:
    """Generate ephemeral book illustrations through the OpenAI Images API."""

    def __init__(self) -> None:
        self._client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_book_image(self, prompt: str) -> str:
        response = self._client.images.generate(
            model=IMAGE_MODEL,
            prompt=(
                "Create a tasteful editorial illustration inspired by this "
                "book recommendation. Do not reproduce a real book cover, "
                "author likeness, logo, or readable text. Use atmospheric "
                "lighting, symbolic objects, and a refined literary mood. "
                f"Recommendation: {prompt}"
            ),
            size="1024x1024",
            quality="low",
        )

        image_data = response.data[0]

        if getattr(image_data, "b64_json", None):
            return f"data:image/png;base64,{image_data.b64_json}"

        if getattr(image_data, "url", None):
            return image_data.url

        raise RuntimeError("The image service returned no image data.")
