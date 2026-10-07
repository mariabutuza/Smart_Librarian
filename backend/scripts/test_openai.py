from openai import OpenAI

from app.config import (
    CHAT_MODEL,
    EMBEDDING_MODEL,
    OPENAI_API_KEY,
)


def test_chat(client: OpenAI) -> None:
    """
    Test the OpenAI Chat API.
    """

    print("\nTesting Chat API...")

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "user",
                "content": "Say hello in Romanian.",
            }
        ],
    )

    print("Chat response:")
    print(response.choices[0].message.content)


def test_embeddings(client: OpenAI) -> None:
    """
    Test the OpenAI Embeddings API.
    """

    print("\nTesting Embeddings API...")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input="Harry Potter is a fantasy novel.",
    )

    embedding = response.data[0].embedding

    print(f"Embedding size: {len(embedding)}")
    print(f"First five values: {embedding[:5]}")


def main() -> None:
    """
    Run all OpenAI connectivity tests.
    """

    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    test_chat(client)

    test_embeddings(client)

    print("\nAll OpenAI tests passed successfully.")


if __name__ == "__main__":
    main()