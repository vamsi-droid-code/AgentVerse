# AgentVerse

AgentVerse is a small multi-agent app. You describe an idea in the chat, and the backend routes it to specialist agents, then combines their notes into one reply. Generation runs on a local [Ollama](https://ollama.com) server. There is no Hugging Face token.

## Layout

- `frontend/` is the app you open in the browser. Vite, React, and TypeScript. Pages are home, signup, login, and the dashboard chat.
- `backend/` is the FastAPI API. `agents/` calls the model and routes work. `handlers/` cleans the request. `database/` talks to Pinecone for memory. `step5_aggregrator/` combines agent notes.
- The root `package.json` is a separate, unused Vite shell. Run the UI from `frontend/`.

## Run Ollama

Ollama must be running before you ask for an answer. No Hugging Face key is used.

```bash
ollama serve
ollama pull qwen2.5:0.5b
```

The API calls `http://127.0.0.1:11434` and model `qwen2.5:0.5b` unless you override them:

- `OLLAMA_BASE_URL` (default `http://127.0.0.1:11434`)
- `OLLAMA_MODEL` (default `qwen2.5:0.5b`)

## Run the API

From `backend/`:

```bash
pip install -r requirements.txt requests pinecone sentence-transformers psycopg2-binary
uvicorn main:app --host 127.0.0.1 --port 8000
```

`requirements.txt` lists FastAPI, Uvicorn, CrewAI, LangChain, OpenAI, and python-dotenv. The process also imports `requests`, `pinecone`, `sentence-transformers`, and `psycopg2`.

The Pinecone client is created when the process starts, so set `PINECONE_API_KEY` in the environment before you start the API. If that key is rejected, memory search and save are skipped and the chat still returns the model reply. Do not put the key in the repo.

Accounts are stored only in memory. They disappear when the API restarts. Signup and login do not use a database.

## Run the frontend

From `frontend/`:

```bash
npm install
npm run dev
```

The dev server listens on port **8080**. Open [http://127.0.0.1:8080](http://127.0.0.1:8080).

The pages call the API at **http://127.0.0.1:8000**:

- `POST /signup` and `POST /login` from the signup and login pages
- `POST /analyze` from the dashboard

`localhost` is not used. Use `127.0.0.1` so the browser hits the IPv4 API.

## Sign up, then sign in

1. Start Ollama, the API, and the frontend.
2. Open [http://127.0.0.1:8080/signup](http://127.0.0.1:8080/signup) and create an account.
3. Sign in at [http://127.0.0.1:8080/login](http://127.0.0.1:8080/login) with that same email and password.
4. The dashboard at [http://127.0.0.1:8080/dashboard](http://127.0.0.1:8080/dashboard) sends your message to `POST http://127.0.0.1:8000/analyze`.
