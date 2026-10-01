# Multi-Agent Research System

A React and FastAPI research workspace that combines web search, webpage extraction, report generation, and critical review into one workflow.

## Live Demo

Try the deployed application at [multi-agent-research-sys.onrender.com](https://multi-agent-research-sys.onrender.com/).

## What It Does

The system processes a research question through four stages:

1. **Search** relevant web sources with Tavily.
2. **Extract** readable page content with `requests` and Trafilatura.
3. **Write** a structured report with Google Gemini.
4. **Review** the report with an LLM-based critic.

The React interface presents the source overview, extracted notes, report, and critique in separate views. Reports can be downloaded as Markdown files.

## Architecture

```text
app.py                 FastAPI API and production static-file host
frontend/src/          React + TypeScript interface
  -> src/pipelines/pipeline.py
       -> src/agents/agents.py
            -> src/tools/tools.py
```

- `app.py`: FastAPI endpoints and built frontend hosting.
- `frontend/src/App.tsx`: Research workspace interface.
- `src/pipelines/pipeline.py`: Orchestrates the research stages.
- `src/agents/agents.py`: Configures LangChain agents and report chains.
- `src/tools/tools.py`: Provides Tavily search and webpage extraction tools.

## Requirements

- Python 3.11 or newer
- A Tavily API key
- A Google Gemini API key
- A Groq API key for the configured Groq client

The pinned Python dependencies are listed in [`requirements.txt`](requirements.txt).

## Setup

### 1. Create and activate an environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```dotenv
GEMINI_3_8_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
```

.

### 4. Start the application locally

Install the frontend dependencies and create its production bundle:

```bash
cd frontend
npm install
npm run build
cd ..
```

Start the API and frontend host:

```bash
uvicorn app:app --reload
```

Open `http://localhost:8000`. During frontend development, run `npm run dev` inside `frontend`; Vite proxies `/api` requests to the FastAPI server.

## Docker deployment

The repository includes a multi-stage [`Dockerfile`](Dockerfile) that builds the React client with Node and copies only the compiled assets into a small Python runtime image. The container runs as a non-root user, exposes only port `8000`, includes a health check, and supports configurable worker concurrency.

Build and run it with Docker:

```bash
docker build -t research-lab:latest .
docker run --rm -p 8000:8000 \
  --env-file .env \
  -e WEB_CONCURRENCY=2 \
  research-lab:latest
```

Or use Compose for a restart policy, read-only filesystem, and local environment loading:

```bash
docker compose up --build -d
docker compose ps
docker compose logs -f research-lab
```

Copy `.env` from the configuration example above before using Compose. In a hosted environment, inject secrets through the platform's secret manager instead of baking them into an image or committing them to source control.

The production process is:

```text
browser -> uvicorn workers -> FastAPI API -> research pipeline -> Tavily/Gemini/Groq
```

Put a TLS-terminating reverse proxy or managed load balancer in front of the container for HTTPS, and set `WEB_CONCURRENCY` based on the available CPU and memory. The `/api/health` endpoint is safe to use for liveness/readiness checks and does not call external model providers.

## Usage

1. Enter a focused research question.
2. Choose how many search results should be considered.
3. Select **Start research**.
4. Review the sources, extracted notes, generated report, and critical review.
5. Download the report from the **Report** view when needed.

Research quality depends on source availability, webpage accessibility, and the responses returned by the configured model providers. Review generated content before using it for decisions or publication.

## Development Notes

Run checks before committing changes:

```bash
python -m py_compile app.py
```

Build the production frontend and image:

```bash
cd frontend && npm ci && npm run build && cd ..
docker build -t research-lab:local .
```

The current console entry point in `main.py` runs a hard-coded research example. Use the API application in `app.py` for the interactive application.

## License

See [LICENSE](LICENSE).
