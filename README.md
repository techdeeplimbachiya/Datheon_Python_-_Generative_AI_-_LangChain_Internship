# Python, Generative AI & LangChain Internship

Projects developed during the Datheon Python, Generative AI,
and LangChain internship.

## Projects

### Task 1: Structured LLM Prompt Pipeline & JSON Extractor

A Python application that extracts invoice information from
unstructured text using Gemini and validates the output with Pydantic.

Features:
- Parameterized prompts and few-shot examples.
- Structured JSON output.
- Nested invoice line items.
- Date and monetary-value validation.
- Missing-field and warning reporting.

[View Task 1](./task-1/)

### Task 3: Multi-Tool Autonomous AI Agent

A LangChain console agent with tools for:
- DuckDuckGo web search.
- Restricted arithmetic calculations.
- Reading local UTF-8 text files.

Displays tool actions, observations, and final answers.

Current validation status:
The API key successfully listed models, but minimal generation requests
returned Gemini 503 UNAVAILABLE errors during testing. Successful
end-to-end autonomous execution has not yet been demonstrated.

[View Task 3](./task-3/)

## Setup

Each task has its own README and requirements.txt.
Follow the instructions inside the relevant task folder.

## Security

API keys, .env files, virtual environments, and Python cache files
must not be committed.

## Author

Deep Limbachiya
