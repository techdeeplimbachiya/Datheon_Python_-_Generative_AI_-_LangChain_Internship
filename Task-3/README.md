# Multi-Tool Autonomous AI Agent

A Python console agent built with LangChain and Google Gemini that can
choose and invoke tools for research, arithmetic, and local document tasks.

Developed for Task 3: Multi-Tool Autonomous AI Agent.

## Features

- Gemini integration through `ChatGoogleGenerativeAI`.
- Autonomous tool selection using LangChain `create_agent`.
- DuckDuckGo web search with source URLs.
- Restricted arithmetic calculator using Python's AST module.
- UTF-8 local file reader restricted to the `documents` folder.
- Console display of tool actions, inputs, observations, and final answers.
- Environment-based API configuration.
- Diagnostic scripts for model discovery and basic API testing.

The console displays observable tool activity, not private internal
chain-of-thought.

## Project Structure

```text
Task-3/
├── agent.py
├── tools.py
├── check_gemini.py
├── list_models.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── documents/
    └── project_notes.txt
```

## Requirements

- Python 3.11 or newer.
- A Gemini API key.
- Access to a Gemini model that supports tool calling.
- An internet connection for Gemini and web search.

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies on Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Install dependencies on macOS/Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and replace the API-key placeholder.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Configuration:

```dotenv
GEMINI_API_KEY=your-real-api-key
GEMINI_MODEL=gemini-flash-latest
```

Use a model available to your project that supports tool calling.
Model aliases, access, and quotas may change.

Never commit `.env` or an actual API key.

## Run

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe agent.py
```

macOS/Linux:

```bash
.venv/bin/python agent.py
```

Type `exit` to quit. Each question starts a fresh task; conversation
history is not retained between questions.

## Available Tools

| Tool | Purpose |
| --- | --- |
| web_search | Retrieves DuckDuckGo search snippets and URLs |
| calculator | Evaluates restricted arithmetic expressions |
| read_local_file | Reads UTF-8 files within `documents` |

The calculator does not execute arbitrary Python code.
The file reader blocks paths outside the documents folder and limits
files to 200 KB.

## Example Prompts

### Calculator

```text
Calculate (12 * 19.95) + 15.
```

Expected mathematical result: 254.40.

### Local File

```text
Read project_notes.txt and summarize the purchasing plan.
```

### Web Search

```text
Search for official LangChain documentation about tool-calling agents.
Provide the URLs and summarize what the search results establish.
```

### Compound Task

```text
Read project_notes.txt. Calculate the total license cost including setup
and the remaining budget. Then search for official LangChain
documentation about tool-calling agents and provide the URLs.
```

The agent chooses which tools to call and in what order.
The exact tool sequence is not hard-coded.

## API Diagnostics

List available content-generation models:

```powershell
.\.venv\Scripts\python.exe list_models.py
```

Test a minimal Gemini request without LangChain:

```powershell
.\.venv\Scripts\python.exe check_gemini.py
```

These commands use the Windows virtual-environment path.
On macOS/Linux, replace it with `.venv/bin/python`.

## Current Validation Status

- The application reached the Gemini API during development.
- Model listing succeeded using the configured API key.
- Minimal generation requests returned `503 UNAVAILABLE` with a
  high-demand message.
- Successful end-to-end autonomous tool execution has not yet been
  demonstrated in the recorded tests.

A listed model does not guarantee that generation or tool calling is
currently available.

## Limitations

- Requires a working external model service.
- API availability and free-tier quotas vary.
- Search returns snippets rather than full verified web pages.
- DuckDuckGo searches may fail or be throttled.
- Calculator supports basic arithmetic, not arbitrary Python.
- Floating-point calculations may show rounding artifacts.
- Local file reading supports UTF-8 text, not PDF or OCR.
- No automated test suite is included.
- The agent is bounded by a recursion limit.

## Security

Use fictional or redacted documents.
Do not place sensitive files in the documents folder.
Do not commit API keys, `.env`, or virtual environments.

## Author

Deep Limbachiya