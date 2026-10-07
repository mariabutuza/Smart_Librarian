"""Servicii pentru filtrarea limbajului in chat.

Furnizeaza o functie care returneaza o lista de cuvinte interzise
si o functie simpla pentru a verifica daca un text contine astfel
de cuvinte.
"""

from typing import List


def get_prohibited_words() -> List[str]:
    """Returneaza lista de cuvinte interzise (toate in litere mici).

    Modificati lista dupa necesitati. Lista contine exemple comune;
    pentru productii reale extindeti si normalizati (forme, diacritice etc.).
    """
    return [
        # exemple generice; inlocuiti sau extindeti conform politicii proiectului
        "prost",
        "idiot",
        "tâmpit",
        "retard",
        "nebun",
        "plictisit",
        "ură",
        "urăsc",
    ]


def contains_prohibited(text: str) -> bool:
    """Verifica daca textul contine vreun cuvant din lista interzisa.

    Comparatia este case-insensitive si cauta potriviri simple pe cuvinte.
    """
    if not text:
        return False
    lowered = text.lower()
    words = {w.strip(".,!?;:\"'()[]") for w in lowered.split()}
    prohibited = set(get_prohibited_words())
    return not words.isdisjoint(prohibited)
