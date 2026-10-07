from fastapi.testclient import TestClient

from app.api import chat as chat_api
from app.api import images as images_api
from app.main import app


client = TestClient(app)


def test_root_endpoint_returns_health_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Smart Librarian API is running."


def test_chat_endpoint_returns_mocked_answer(monkeypatch):
    def fake_chat(question, history):
        assert question == "Recommend a fantasy book"
        assert history == []
        return "Try The Hobbit."

    monkeypatch.setattr(chat_api.llm_service, "chat", fake_chat)

    response = client.post(
        "/chat/",
        json={"message": "Recommend a fantasy book", "history": []},
    )

    assert response.status_code == 200
    assert response.json() == {"answer": "Try The Hobbit."}


def test_chat_endpoint_rejects_empty_message():
    response = client.post(
        "/chat/",
        json={"message": "", "history": []},
    )

    assert response.status_code == 422


def test_chat_endpoint_filters_prohibited_message():
    response = client.post(
        "/chat/",
        json={"message": "idiot", "history": []},
    )

    assert response.status_code == 200
    assert response.json()["answer"]


def test_image_endpoint_returns_mocked_image(monkeypatch):
    monkeypatch.setattr(
        images_api.image_service,
        "generate_book_image",
        lambda prompt: "data:image/png;base64,test-image",
    )

    response = client.post(
        "/images/generate",
        json={"prompt": "A mysterious library at night"},
    )

    assert response.status_code == 200
    assert response.json() == {"image": "data:image/png;base64,test-image"}


def test_image_endpoint_returns_bad_gateway_when_generation_fails(monkeypatch):
    def raise_generation_error(prompt):
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(
        images_api.image_service,
        "generate_book_image",
        raise_generation_error,
    )

    response = client.post(
        "/images/generate",
        json={"prompt": "A literary scene"},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == "The book illustration could not be generated."
