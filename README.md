# PPT Generator - Dummy Scaffold

## Phase 1: Foundation

This repository contains the foundation scaffold for a PPT Generator application.
The current implementation handles an end-to-end flow using **dummy data only**.

## Project Structure
- `backend/`: FastAPI application.
- `frontend/`: React (Vite) application.

## Scope of Phase 1
- **Goal**: Scaffold the repo and create a working pipeline.
- **Input**: User provides text, guidance, API key (dummy), and a reference file.
- **Output**: A dummy `.pptx` file is generated and downloaded.
- **Constraints**: 
    - No real LLM calls.
    - No real PPT parsing.
    - API Key is not stored or logged.

## How to Run

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

### Usage
1. Open the frontend URL (e.g., `http://localhost:5173`).
2. FIll in the form (Topic, Guidance, etc.).
3. Upload any valid `.pptx` file (content is ignored).
4. Click "Generate PPT".
5. Receive `generated_presentation.pptx` with 2 dummy slides.
