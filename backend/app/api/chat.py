from fastapi import APIRouter, HTTPException

from app.dependencies import llm_service
from app.models.chat_request import ChatRequest
from app.models.chat_response import ChatResponse
from app.services.content_filter import contains_prohibited


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
) -> ChatResponse:
    if contains_prohibited(request.message):
        return ChatResponse(
            answer=(
                "Let’s keep the conversation polite. "
                "I can help you with book recommendations."
            )
        )
    """
    Generate a book recommendation using RAG and tool calling.
    """

    try:
        answer = llm_service.chat(
            question=request.message,
            history=[
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.history
        ],
    )

        return ChatResponse(
            answer=answer,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="The chatbot could not generate a response.",
        ) from exc
