# Backend - AI PowerPoint Generator

FastAPI backend service for the AI-powered PowerPoint generator.

## Features

- **Template Analysis**: Extracts layouts, colors, fonts, and images from uploaded PPTX files
- **LLM Integration**: Supports OpenAI, Anthropic Claude, and Google Gemini
- **Image Extraction**: Catalogs and categorizes images from templates for reuse
- **Slide Generation**: Creates presentations with intelligent content mapping
- **Speaker Notes**: Auto-generates speaker notes for each slide
- **Error Handling**: Robust validation and error messages

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- python-pptx
- httpx (for LLM API calls)
- Pydantic (validation)
- Pillow (image processing)

## Setup & Run

1. Navigate to the `backend` directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn app.main:app --port 8001 --log-level debug
   ```
   The server will start at `http://127.0.0.1:8001`

## API Endpoints

### `POST /generate`

Generates a PowerPoint presentation from text input.

**Request (multipart/form-data):**
- `text_input` (string, required): The content to convert into slides
- `guidance` (string, optional): Tone/style guidance (e.g., "Investor Pitch")
- `api_key` (string, required): LLM API key (OpenAI, Anthropic, or Gemini)
- `file` (file, required): PowerPoint template file (.pptx)

**Response:**
- Content-Type: `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- Binary PPTX file download

**Error Codes:**
- `400`: Invalid input (bad API key, invalid template)
- `500`: Server error (LLM failure, generation error)

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── generate.py          # Main API endpoint
│   ├── services/
│   │   ├── llm/
│   │   │   ├── openai.py        # OpenAI client
│   │   │   ├── gemini.py        # Gemini client
│   │   │   └── anthropic.py     # Anthropic client
│   │   ├── ppt/
│   │   │   ├── ppt_exporter.py  # PPT generation
│   │   │   ├── slide_builder.py # Slide content & images
│   │   │   ├── slide_cloner.py  # Template cloning
│   │   │   ├── layout_mapper.py # Layout selection
│   │   │   └── image_extractor.py # Image extraction
│   │   ├── template_parser.py   # Template analysis
│   │   ├── slide_planner.py     # LLM orchestration
│   │   ├── prompt_builder.py    # LLM prompts
│   │   └── validators.py        # Pydantic models
│   └── main.py                  # FastAPI app
└── requirements.txt
```

## Environment Variables

No environment variables required. API keys are provided per-request by users.

## Development

- **Logging**: Set to DEBUG level for detailed logs
- **CORS**: Configured to allow all origins (adjust for production)
- **Port**: Default 8001 (to avoid Windows conflicts)

## Supported LLM Providers

The backend automatically detects the LLM provider based on API key format:

- **OpenAI**: Keys starting with `sk-` (excluding `sk-ant-`)
- **Anthropic**: Keys starting with `sk-ant-`
- **Gemini**: All other keys (typically starting with `AIza`)

## Security Notes

- API keys are **never stored** or logged
- Keys are passed directly to LLM providers
- Template files are processed in-memory only
- No persistent storage of user data
