from fastapi import APIRouter, HTTPException

from app.models.image_request import ImageRequest
from app.models.image_response import ImageResponse
from app.services.image_service import ImageService


router = APIRouter(
    prefix="/images",
    tags=["Images"],
)

image_service = ImageService()


@router.post(
    "/generate",
    response_model=ImageResponse,
)
def generate_image(request: ImageRequest) -> ImageResponse:
    try:
        image = image_service.generate_book_image(request.prompt)
        return ImageResponse(image=image)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="The book illustration could not be generated.",
        ) from exc
