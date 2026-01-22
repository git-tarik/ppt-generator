# Frontend - AI PowerPoint Generator

React frontend application for the AI-powered PowerPoint generator.

## Features

- **Intuitive Form**: Clean UI for text input, tone selection, and file upload
- **Tone Presets**: Quick-select buttons for common presentation types
- **Live Slide Estimation**: Real-time estimate of slide count based on content
- **Loading States**: Visual feedback during generation process
- **Error Handling**: User-friendly error messages with specific guidance
- **File Validation**: 10MB file size limit with validation
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- React 18
- Vite (build tool)
- Vanilla CSS (no framework dependencies)

## Setup & Run

1. Navigate to the `frontend` directory
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`

## Build for Production

```bash
npm run build
```

The production build will be in the `dist/` folder.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── UploadForm.jsx       # Main form component
│   │   └── UploadForm.css       # Form styles
│   ├── services/
│   │   └── api.js               # API client
│   ├── App.jsx                  # Root component
│   ├── App.css                  # App styles
│   ├── index.css                # Global styles
│   └── main.jsx                 # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## Configuration

### API Endpoint

The backend API URL is configured in `src/services/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
```

To change the backend URL:
- **Development**: Update `VITE_API_URL` in `.env`
- **Production**: Set environment variable during build

## Components

### UploadForm

Main form component that handles:
- Text input with character validation
- Tone/style preset selection
- API key input (password field)
- Template file upload with size validation
- Form submission and error handling
- Download trigger for generated presentations

## Deployment

### Vercel

```bash
npm run build
vercel --prod
```

### Netlify

```bash
npm run build
netlify deploy --prod --dir=dist
```

### Environment Variables

Set `VITE_API_URL` to your backend URL in production.

## Development Notes

- **Hot Reload**: Vite provides instant hot module replacement
- **CSS**: Uses vanilla CSS for maximum compatibility
- **No Build Dependencies**: Minimal dependencies for faster builds
- **Browser Support**: Modern browsers (ES6+)
