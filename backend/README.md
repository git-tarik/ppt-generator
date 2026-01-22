# Backend - PPT Generator

## Phase 1: Foundation (Dummy Mode)
## Phase 2: Template Parsing

This is the backend scaffold for the PPT Generator.

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
3.  Run the server (Note: Port 8001 to avoid Windows conflicts):
    ```bash
    uvicorn app.main:app --port 8001 --log-level debug
    ```
    The server will start at `http://127.0.0.1:8001`.

## Implemented Features
- `POST /generate`: Accepts text, guidance, api_key, and a file.
    - **Phase 2 Implementation**: Parses uploaded PPTX, extracts layouts/placeholders, and logs metadata to console.
    - Returns a dummy `.pptx` file (Phase 1 behavior preserved).
