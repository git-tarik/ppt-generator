# Frontend - PPT Generator

## Phase 1: Foundation

This is the React frontend for the PPT Generator.

## Tech Stack
- React
- Vite
- Plain CSS

## Setup & Run

1.  Navigate to the `frontend` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    The app will be available at `http://localhost:5173`.

## Implemented Features
- **Upload Form**: Collects inputs (Text, Guidance, API Key, File).
- **Submission**: Sends `multipart/form-data` to backend.
- **Auto-Download**: Automatically downloads the generated `.pptx` on success.
- **Error Handling**: Displays error messages if generation fails.
