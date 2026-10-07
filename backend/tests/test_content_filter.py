from app.services.content_filter import contains_prohibited


def test_contains_prohibited_detects_case_insensitive_words():
    assert contains_prohibited("Acest mesaj conține un IDIOT") is True


def test_contains_prohibited_ignores_punctuation():
    assert contains_prohibited("Ce om prost!") is True


def test_contains_prohibited_accepts_normal_book_request():
    assert contains_prohibited("Recomandă-mi o carte fantasy") is False


def test_contains_prohibited_accepts_empty_text():
    assert contains_prohibited("") is False
