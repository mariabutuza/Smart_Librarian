import json
from pathlib import Path
from textwrap import dedent
from typing import Any

from openai import OpenAI

from app.config import CHAT_MODEL, OPENAI_API_KEY
from app.services.rag_service import RagService
from app.tools.summary_tool import SummaryTool


INTENT_CLASSIFIER_PROMPT = """
You classify messages for a book assistant.

Return exactly one word:

BOOK
NON_BOOK

Return BOOK when the latest message, considered together with the
conversation history, is about books, reading, authors, literature,
genres, summaries, recommendations, or continues a previous
book-related conversation.

Examples that can be BOOK when the history is about books:
- another one
- mai dă-mi una
- something similar
- altceva
- tell me more
- spune-mi mai multe
- compare it with the previous one
- cine a scris-o

Return NON_BOOK when the request is unrelated to books or literature.

Do not explain the classification.
"""


SEARCH_QUERY_PROMPT = """
Rewrite the latest user message as one standalone semantic search query
for a book vector database.

Use the conversation history to resolve references such as:
- another one
- something similar
- the previous book
- it / that book / this one
- mai dă-mi una
- ceva asemănător
- spune-mi mai multe despre ea
- una mai scurtă
- una mai întunecată

Rules:
- Preserve the user's language.
- Include relevant genre, themes, mood, author, title, or constraints
  found in the conversation.
- When the user asks for another recommendation, make clear that a
  different book is required and include previously recommended titles
  as titles to avoid.
- When the user asks about an exact title or asks for more details about
  a previously mentioned title, include that exact title.
- Do not answer the user.
- Do not recommend a book.
- Return only the search query, without labels, quotes, or explanation.
"""


class LLMService:
    """
    Coordinate intent classification, conversation history,
    contextual RAG retrieval, tool calling and response generation.

    Conversation persistence is owned by the caller. The complete recent
    history must be supplied to ``chat`` for every request.
    """

    MAX_HISTORY_MESSAGES = 20

    def __init__(
        self,
        rag_service: RagService,
        summary_tool: SummaryTool,
    ) -> None:
        self._rag_service = rag_service
        self._summary_tool = summary_tool

        self._client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

        self._system_prompt = self._load_system_prompt()
        self._tools = self._build_tools()

    @staticmethod
    def _load_system_prompt() -> str:
        prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "system_prompt.txt"
        )

        if not prompt_path.exists():
            raise FileNotFoundError(
                f"System prompt not found: {prompt_path}"
            )

        return prompt_path.read_text(
            encoding="utf-8"
        ).strip()

    @staticmethod
    def _build_tools() -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "name": "get_summary_by_title",
                "description": (
                    "Return the complete summary of a book using its exact "
                    "title from the retrieved context."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": (
                                "The exact title of the selected book."
                            ),
                        }
                    },
                    "required": ["title"],
                    "additionalProperties": False,
                },
                "strict": True,
            }
        ]

    @classmethod
    def _normalize_history(
        cls,
        history: list[dict[str, str]] | None,
    ) -> list[dict[str, str]]:
        if not history:
            return []

        normalized_history: list[dict[str, str]] = []

        for message in history[-cls.MAX_HISTORY_MESSAGES:]:
            role = message.get("role")
            content = message.get("content")

            if role not in {"user", "assistant"}:
                continue

            if not isinstance(content, str) or not content.strip():
                continue

            normalized_history.append(
                {
                    "role": role,
                    "content": content.strip(),
                }
            )

        return normalized_history

    @staticmethod
    def _format_history(
        history: list[dict[str, str]],
    ) -> str:
        if not history:
            return "No previous conversation."

        return "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history
        )

    def _classify_intent(
        self,
        question: str,
        history: list[dict[str, str]],
    ) -> str:
        classifier_input = dedent(
            f"""
            Conversation history:
            {self._format_history(history)}

            Latest user message:
            {question}
            """
        ).strip()

        response = self._client.responses.create(
            model=CHAT_MODEL,
            instructions=INTENT_CLASSIFIER_PROMPT,
            input=classifier_input,
        )

        intent = response.output_text.strip().upper()
        intent = intent.rstrip(".! ")

        if intent not in {"BOOK", "NON_BOOK"}:
            return "NON_BOOK"

        return intent

    def _generate_non_book_response(
        self,
        question: str,
    ) -> str:
        response = self._client.responses.create(
            model=CHAT_MODEL,
            instructions=(
                "Reply in the same language as the user's message. "
                "Politely explain that I can only help "
                "with books, authors, reading and literature. "
                "Keep the answer to one or two short sentences."
            ),
            input=question,
        )

        text = response.output_text.strip()

        if not text:
            raise RuntimeError(
                "The model returned an empty scope response."
            )

        return text

    def _build_search_query(
        self,
        question: str,
        history: list[dict[str, str]],
    ) -> str:
        """
        Build a standalone query for Chroma using both user and assistant
        messages. This resolves conversational references before retrieval.
        """
        if not history:
            return question

        contextualizer_input = [
            *history,
            {
                "role": "user",
                "content": question,
            },
        ]

        response = self._client.responses.create(
            model=CHAT_MODEL,
            instructions=SEARCH_QUERY_PROMPT,
            input=contextualizer_input,
        )

        search_query = response.output_text.strip()

        # Retrieval should still work if contextualization unexpectedly
        # produces no text.
        return search_query or question

    @staticmethod
    def _build_context_message(
        retrieved_documents: list[str],
    ) -> str:
        context = "\n\n---\n\n".join(retrieved_documents)

        return dedent(
            f"""
            Book context retrieved for the latest user request:

            {context}

            Use this context only as the allowed source of book knowledge.
            Use the preceding conversation to understand references and
            follow-up requests. Do not repeat a previously recommended title
            when the user asks for another recommendation. Follow the user's
            requested number of recommendations. For one selected book or an
            exact-title request, call get_summary_by_title with the exact title.
            Respond entirely in the language of the latest user message.
            """
        ).strip()

    @classmethod
    def _build_model_input(
        cls,
        history: list[dict[str, str]],
        question: str,
        retrieved_documents: list[str],
    ) -> list[dict[str, str]]:
        """
        Keep the real user message as the final conversational message.
        The RAG context is supplied separately as a developer message.
        """
        return [
            *history,
            {
                "role": "developer",
                "content": cls._build_context_message(
                    retrieved_documents
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ]

    def _execute_tool_call(
        self,
        tool_name: str,
        arguments: str,
    ) -> str:
        if tool_name != "get_summary_by_title":
            raise ValueError(
                f'Unsupported tool requested: "{tool_name}".'
            )

        try:
            parsed_arguments = json.loads(arguments)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "The tool arguments are not valid JSON."
            ) from exc

        title = parsed_arguments.get("title")

        if not isinstance(title, str) or not title.strip():
            raise ValueError(
                "The tool call must contain a valid book title."
            )

        normalized_title = title.strip()

        try:
            summary = self._summary_tool.get_summary_by_title(
                title=normalized_title
            )

            result = {
                "success": True,
                "title": normalized_title,
                "summary": summary,
            }

        except ValueError as exc:
            result = {
                "success": False,
                "title": normalized_title,
                "error": str(exc),
            }

        return json.dumps(
            result,
            ensure_ascii=False,
        )

    def _generate_no_results_response(
        self,
        question: str,
        history: list[dict[str, str]],
    ) -> str:
        response = self._client.responses.create(
            model=CHAT_MODEL,
            instructions=(
                "Reply in the language of the latest user message. "
                "Use the conversation history to understand the request. "
                "Politely explain that no suitable book was found and ask "
                "for one useful alternative preference, such as another "
                "genre, theme, or mood. Keep the response concise."
            ),
            input=[
                *history,
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )

        text = response.output_text.strip()

        if not text:
            raise RuntimeError(
                "The model returned an empty no-results response."
            )

        return text

    def chat(
        self,
        question: str,
        history: list[dict[str, str]] | None = None,
        n_results: int = 5,
    ) -> str:
        normalized_question = question.strip()

        if not normalized_question:
            raise ValueError(
                "The user question cannot be empty."
            )

        if n_results <= 0:
            raise ValueError(
                "n_results must be greater than zero."
            )

        normalized_history = self._normalize_history(history)

        intent = self._classify_intent(
            question=normalized_question,
            history=normalized_history,
        )

        if intent == "NON_BOOK":
            return self._generate_non_book_response(
                normalized_question
            )

        search_query = self._build_search_query(
            question=normalized_question,
            history=normalized_history,
        )

        retrieved_documents = self._rag_service.search(
            query=search_query,
            n_results=n_results,
        )

        if not retrieved_documents:
            return self._generate_no_results_response(
                question=normalized_question,
                history=normalized_history,
            )

        model_input = self._build_model_input(
            history=normalized_history,
            question=normalized_question,
            retrieved_documents=retrieved_documents,
        )

        initial_response = self._client.responses.create(
            model=CHAT_MODEL,
            instructions=self._system_prompt,
            input=model_input,
            tools=self._tools,
            tool_choice="auto",
        )

        tool_outputs: list[dict[str, str]] = []

        for output_item in initial_response.output:
            if output_item.type != "function_call":
                continue

            tool_result = self._execute_tool_call(
                tool_name=output_item.name,
                arguments=output_item.arguments,
            )

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": output_item.call_id,
                    "output": tool_result,
                }
            )

        if not tool_outputs:
            initial_text = initial_response.output_text.strip()

            if not initial_text:
                raise RuntimeError(
                    "The model returned neither text nor a tool call."
                )

            return initial_text

        final_response = self._client.responses.create(
            model=CHAT_MODEL,
            instructions=self._system_prompt,
            previous_response_id=initial_response.id,
            input=tool_outputs,
        )

        final_text = final_response.output_text.strip()

        if not final_text:
            raise RuntimeError(
                "The model returned an empty response."
            )

        return final_text