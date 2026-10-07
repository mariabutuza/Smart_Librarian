# Smart Librarian

Smart Librarian este o aplicație web pentru recomandări de cărți. Utilizatorul poate descrie genul, atmosfera, temele sau autorii preferați, iar aplicația folosește un chatbot cu RAG pentru a găsi recomandări relevante din baza locală de cărți.

Aplicația include și funcționalități opționale:

- Text-to-Speech pentru ascultarea răspunsurilor;
- Speech-to-Text pentru întrebări rostite la microfon;
- generarea unei ilustrații reprezentative pentru o recomandare;
- teste automate pentru backend.

## Tehnologii

### Frontend

- React 19;
- Vite;
- Tailwind CSS v4;
- `lucide-react` pentru iconițe;
- Web Speech API pentru Text-to-Speech și Speech-to-Text.

### Backend

- Python;
- FastAPI;
- Uvicorn;
- OpenAI Responses API pentru clasificare, contextualizare și răspunsuri;
- OpenAI Embeddings pentru reprezentări vectoriale;
- OpenAI Images API pentru ilustrații;
- ChromaDB pentru vector store persistent local;
- Pydantic pentru validarea request-urilor și response-urilor.

## Structura proiectului

```text
SmartLibrarian/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   └── images.py
│   │   ├── data/
│   │   │   └── book_summaries.json
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── services/
│   │   │   ├── embedding_service.py
│   │   │   ├── image_service.py
│   │   │   ├── llm_service.py
│   │   │   └── rag_service.py
│   │   ├── vector_store/
│   │   │   └── chroma_db/
│   │   └── main.py
│   ├── scripts/
│   │   ├── ingest_books.py
│   │   ├── test_chroma.py
│   │   ├── test_openai.py
│   │   └── test_rag.py
│   ├── tests/
│   ├── requirements.txt
│   └── pytest.ini
└── frontend/
    ├── src/
    │   ├── api/chatApi.js
    │   ├── components/
    │   └── App.jsx
    ├── .env
    └── package.json
```

## Cerințe

Instalează:

- Python 3.11+;
- Node.js 18+;
- npm;
- o cheie API OpenAI cu acces la modelele folosite.

## Configurarea backend-ului

Intră în folderul backend și creează sau verifică fișierul `.env`:

```env
OPENAI_API_KEY=cheia_ta_openai
CHAT_MODEL=gpt-5.5
EMBEDDING_MODEL=text-embedding-3-small
IMAGE_MODEL=gpt-image-2
CHROMA_COLLECTION=books
```

Nu publica niciodată cheia API în GitHub sau în frontend. Fișierul `.env` trebuie să fie în `.gitignore`.

Instalează dependențele:

```powershell
cd C:\Users\mbutuza\SmartLibrarian\backend
.\.venv\Scripts\pip.exe install -r requirements.txt
```

Dacă virtual environment-ul nu există:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.\.venv\Scripts\pip.exe install -r requirements.txt
```

## Ingestia cărților în ChromaDB

Datele originale sunt în:

```text
backend/app/data/book_summaries.json
```

Pentru a genera embeddings și a popula ChromaDB:

```powershell
cd C:\Users\mbutuza\SmartLibrarian\backend
.\.venv\Scripts\python.exe scripts\ingest_books.py
```

Vector store-ul persistent este creat în:

```text
backend/app/vector_store/chroma_db/
```

Colecția implicită este `books`, iar embeddings sunt generate cu `text-embedding-3-small`.

## Pornirea backend-ului

Backend-ul folosit de frontend rulează pe portul `8000`:

```powershell
cd C:\Users\mbutuza\SmartLibrarian\backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Verifică serverul la:

```text
http://127.0.0.1:8000/
```

Răspunsul așteptat este:

```json
{
  "message": "Smart Librarian API is running."
}
```

## Configurarea și pornirea frontend-ului

Fișierul `frontend/.env` trebuie să conțină:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Pornește frontend-ul:

```powershell
cd C:\Users\mbutuza\SmartLibrarian\frontend
npm.cmd install
npm.cmd run dev
```

Deschide:

```text
http://localhost:5173
```

Dacă PowerShell blochează comanda `npm`, folosește `npm.cmd`, așa cum apare mai sus.

## Funcționalități

### Recomandări cu RAG

1. Frontend-ul trimite întrebarea către `POST /chat/`.
2. Backend-ul clasifică intenția: mesaj despre cărți sau mesaj în afara domeniului.
3. Pentru întrebări despre cărți, istoricul conversației este folosit pentru contextualizare.
4. ChromaDB caută documentele similare semantic.
5. Documentele găsite sunt trimise modelului ca informație de context.
6. Modelul generează recomandarea și, când este necesar, poate folosi tool-ul pentru rezumatul unei cărți.

### Text-to-Speech

Sub fiecare răspuns al asistentului există butonul `Ascultă`.

Implementarea folosește `window.speechSynthesis`, deci:

- nu necesită backend suplimentar;
- nu salvează fișiere audio;
- folosește vocile disponibile în browser și sistemul de operare.

### Speech-to-Text

Butonul cu microfon din câmpul de mesaj pornește modul vocal.

Fluxul este:

```text
Microfon → browser → text transcris → POST /chat/
```

Utilizatorul trebuie să permită accesul la microfon. Funcționalitatea este suportată cel mai bine în Chrome și Edge și funcționează pe `localhost`.

Audio-ul nu este salvat de aplicație și nu este trimis direct backend-ului; backend-ul primește doar textul transcris.

### Generare de imagini

Sub răspunsurile normale există butonul `Imagine`. Utilizatorul apasă butonul, introduce o descriere într-un câmp, imaginea este generată după transmiterea descrierii, contextul conversației fiind folosit ca referință.

Frontend-ul trimite promptul către:

```text
POST /images/generate
```

Backend-ul apelează OpenAI Images API cu `gpt-image-2`, apoi returnează imaginea ca Data URL Base64. Imaginea este afișată în mesaj și păstrată doar în memoria frontend-ului.

Imaginea nu este salvată permanent în baza de date sau pe disk în versiunea actuală.

## API

### Health check

```http
GET /
```

### Chat

```http
POST /chat/
Content-Type: application/json
```

Request:

```json
{
  "message": "Recomandă-mi un roman fantasy",
  "history": [
    {
      "role": "user",
      "content": "Îmi plac aventurile"
    },
    {
      "role": "assistant",
      "content": "Îți recomand..."
    }
  ]
}
```

Response:

```json
{
  "answer": "Îți recomand..."
}
```


## Teste automate

Testele automate se află în:

```text
backend/tests/
```

Rulează testele cu:

```powershell
cd C:\Users\mbutuza\SmartLibrarian\backend
.\.venv\Scripts\python.exe -m pytest -q
```

Testele acoperă:

- filtrarea conținutului;
- încărcarea și căutarea cărților;
- health check-ul API;
- validarea endpoint-ului `/chat/`;
- răspunsurile mock-uite ale chatbotului;
- endpoint-ul `/images/generate`;
- erorile serviciului de generare imagini.

Testele OpenAI sunt mock-uite și nu fac request-uri reale către servicii externe.

## Scripturi manuale

Scripturile din `backend/scripts/` sunt verificări manuale sau experimentale:

```text
test_openai.py  → verificări OpenAI
test_chroma.py  → verificări ChromaDB
test_rag.py     → verificări RAG
ingest_books.py → populează ChromaDB
```

Ele nu sunt executate de aplicație la pornire. Suita automată folosește doar fișierele din `backend/tests/`.

## Depanare

### Frontend-ul afișează `Failed to fetch`

Verifică dacă backend-ul rulează:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
```

Verifică și `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

După modificarea unui fișier `.env`, repornește Vite.

### Endpoint-ul returnează HTTP 500

Verifică:

- `OPENAI_API_KEY`;
- accesul la internet al backend-ului;
- modelul configurat în `.env`;
- logurile procesului Uvicorn;
- existența embeddings în ChromaDB.

### Nu se generează recomandări

Rulează din nou ingestia:

```powershell
.\.venv\Scripts\python.exe scripts\ingest_books.py
```

### Microfonul nu funcționează

- acceptă permisiunea pentru microfon;
- folosește Chrome sau Edge;
- verifică dacă altă aplicație folosește microfonul;
- testează pe `localhost` sau HTTPS.

### Nu apare butonul de imagine

Butonul apare doar sub răspunsurile normale ale asistentului. Nu apare pentru indicatorul de loading sau pentru mesajele de eroare.

## Siguranță și costuri

- Nu pune `OPENAI_API_KEY` în frontend.
- Nu publica fișierul `backend/.env`.
- Generarea unei imagini folosește credit API.
- Imaginea este generată doar când utilizatorul apasă butonul `Imagine`.
- În versiunea actuală imaginile nu sunt persistente.
- Pentru producție, imaginile ar trebui salvate într-un object storage, iar în baza de date ar trebui păstrat doar URL-ul.

## Licență și utilizare

Acest proiect este destinat utilizării educaționale și demonstrative. Verifică termenii și costurile serviciilor OpenAI înainte de folosirea aplicației într-un mediu public sau comercial.
