# Backend - PPT Generator

## Phase 1: Foundation (Dummy Mode)

This is the backend scaffold for the PPT Generator. It simulates the generation process without making real LLM calls.

## Tech Stack
- Python 3.10+
- FastAPI
- Uvicorn
- python-pptx

## Setup & Run

1.  Navigate to the `backend` directory.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```
    The server will start at `http://127.0.0.1:8000`.

## Implemented Features
- `POST /generate`: Accepts text, guidance, api_key, and a file. Returns a dummy `.pptx` file.
- **Mocked**: No actual AI generation; returns hardcoded slides using `python-pptx`.
- **Ignored**: Content of the uploaded file is strictly ignored in this phase.
