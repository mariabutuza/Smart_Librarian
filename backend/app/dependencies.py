from app.repositories.book_repository import BookRepository
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.rag_service import RagService
from app.tools.summary_tool import SummaryTool


book_repository = BookRepository()

embedding_service = EmbeddingService()

rag_service = RagService(
    embedding_service=embedding_service,
)

summary_tool = SummaryTool(
    repository=book_repository,
)

llm_service = LLMService(
    rag_service=rag_service,
    summary_tool=summary_tool,
)