# Multi-Agent Research System

A Streamlit research workspace that combines web search, webpage extraction, report generation, and critical review into one workflow.

## What It Does

The system processes a research question through four stages:

1. **Search** relevant web sources with Tavily.
2. **Extract** readable page content with `requests` and Trafilatura.
3. **Write** a structured report with Google Gemini.
4. **Review** the report with an LLM-based critic.

The Streamlit interface presents the source overview, extracted notes, report, and critique in separate views. Reports can be downloaded as Markdown files.

## Architecture

```text
app.py
  -> src/pipelines/pipeline.py
       -> src/agents/agents.py
            -> src/tools/tools.py
```

- `app.py`: Streamlit user interface and request handling.
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

Do not commit `.env` or publish API keys. Use a secret manager for deployed environments.

### 4. Start the application

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, usually `http://localhost:8501`.

## Usage

1. Enter a focused research question.
2. Choose how many search results should be considered.
3. Select **Start research**.
4. Review the sources, extracted notes, generated report, and critical review.
5. Download the report from the **Report** view when needed.

Research quality depends on source availability, webpage accessibility, and the responses returned by the configured model providers. Review generated content before using it for decisions or publication.

## Development Notes

Run a syntax check before committing changes:

```bash
python -m py_compile app.py
```

The current console entry point in `main.py` runs a hard-coded research example. Use `app.py` for the interactive application.

## License

See [LICENSE](LICENSE).
