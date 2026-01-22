# AI-Powered PowerPoint Generator

Transform bulk text, markdown, or prose into fully formatted PowerPoint presentations that match your chosen template's look and feel.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **Intelligent Text Parsing**: Automatically breaks down input text into logical slides with titles and bullet points
- **Template Style Preservation**: Extracts and applies colors, fonts, and layouts from your uploaded template
- **Image Reuse**: Intelligently reuses images from templates (logos, backgrounds, decorative elements)
- **Speaker Notes**: Auto-generates helpful speaker notes for each slide
- **Multi-LLM Support**: Works with OpenAI (GPT), Anthropic (Claude), and Google (Gemini)
- **Secure**: API keys are never stored or logged
- **Customizable Tone**: Choose from presets or provide custom guidance

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 16+
- An API key from OpenAI, Anthropic, or Google

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ppt-generator.git
   cd ppt-generator
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --port 8001
   ```

3. **Frontend Setup** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the app**
   - Open your browser to `http://localhost:5173`

## 📖 Usage

1. **Paste Your Content**: Enter the text you want to convert (minimum 50 words recommended)
2. **Choose a Tone**: Select from presets like "Investor Pitch" or "Technical Overview"
3. **Enter API Key**: Provide your OpenAI (`sk-...`), Anthropic (`sk-ant-...`), or Gemini (`AIza...`) API key
4. **Upload Template**: Upload a `.pptx` file that has your desired style, colors, and images
5. **Generate**: Click "Generate Presentation" and download your custom PowerPoint!

## 🔬 Technical Overview

### How Text is Parsed and Mapped to Slides

The application uses a multi-stage LLM-powered pipeline to transform unstructured text into structured presentations. When you submit content, the system first constructs a detailed prompt that instructs the AI to analyze the text and identify logical breakpoints, key themes, and supporting details. The LLM returns a JSON schema containing slide titles, bullet points (limited to 15 words each for clarity), and speaker notes. This structured plan is validated using Pydantic models to ensure consistency and completeness. The system intelligently determines the number of slides based on content volume and complexity—not a fixed count—ensuring each slide has a focused message. The result is a presentation that flows naturally from introduction to conclusion, with each slide serving a clear purpose.

### How Visual Style and Assets are Applied

Template style application happens through a comprehensive extraction and reuse process. When you upload a PowerPoint template, the system performs deep analysis using the `python-pptx` library. It extracts layout structures, placeholder positions, theme colors (by sampling fill colors from shapes), and font families used throughout the template. Critically, the system also catalogs all images in the template, categorizing them as logos (small corner images), backgrounds (large covering images), or content images based on size and position heuristics. During presentation generation, each new slide is cloned from the template's layouts using a modulo-based rotation to maintain visual variety. The cloning process preserves all formatting, colors, and fonts. Images are then intelligently reused: logos are consistently placed on slides to maintain branding, while backgrounds are selectively applied to avoid clutter. This approach ensures the generated presentation looks professionally designed and maintains complete visual consistency with your brand or template style.

## 🏗️ Architecture

```
ppt-generator/
├── backend/          # FastAPI server
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── services/ # Business logic
│   │   │   ├── llm/  # LLM clients (OpenAI, Gemini, Anthropic)
│   │   │   └── ppt/  # PPT generation & image extraction
│   │   └── main.py
│   └── requirements.txt
└── frontend/         # React + Vite
    ├── src/
    │   ├── components/
    │   └── services/
    └── package.json
```

## 🔑 Supported LLM Providers

| Provider | API Key Format | Model Used |
|----------|---------------|------------|
| OpenAI | `sk-...` | GPT-3.5-turbo |
| Anthropic | `sk-ant-...` | Claude 3 Haiku |
| Google | `AIza...` | Gemini 1.5 Flash |

## 🛡️ Security & Privacy

- **No Storage**: API keys are passed directly to LLM providers and never stored
- **No Logging**: Sensitive data is not logged to files or databases
- **Client-Side**: API keys are entered in the browser and sent only to the backend for immediate use

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

## 🚢 Deployment

### Backend Deployment (e.g., Render, Railway)

1. Set environment variables if needed
2. Deploy with: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (e.g., Vercel, Netlify)

1. Build: `npm run build`
2. Deploy the `dist/` folder
3. Update API endpoint in `src/services/api.js`

---

**Made with ❤️ using FastAPI, React, and AI**
