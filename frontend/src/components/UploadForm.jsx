import React, { useState } from 'react';
import { generatePPT } from '../services/api';
import './UploadForm.css';

const UploadForm = () => {
    const [textInput, setTextInput] = useState('');
    const [guidance, setGuidance] = useState('');
    const [apiKey, setApiKey] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [loadingText, setLoadingText] = useState('Processing...');
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);

    // Slide Estimation Logic
    const estimatedSlides = textInput ? Math.max(3, Math.min(15, Math.ceil(textInput.split(/\s+/).length / 120))) : 0;

    const [selectedPreset, setSelectedPreset] = useState(null);

    const handleFileChange = (e) => {
        if (e.target.files) {
            const selectedFile = e.target.files[0];

            // File size validation (10MB limit)
            const maxSize = 10 * 1024 * 1024; // 10MB in bytes
            if (selectedFile.size > maxSize) {
                setError("File size exceeds 10MB limit. Please upload a smaller template.");
                setFile(null);
                return;
            }

            setFile(selectedFile);
            setError(null); // Clear any previous errors
        }
    };

    const handlePreset = (presetText) => {
        setSelectedPreset(presetText);
        // Append instead of overwrite, avoid duplicates
        if (!guidance.includes(presetText)) {
            setGuidance(prev => prev ? `${prev}, ${presetText}` : presetText);
        }
    };

    const presets = [
        "🎯 Investor Pitch",
        "📊 Research Summary",
        "🧠 Technical Overview",
        "📢 Sales Deck",
        "🧑‍🏫 Educational Slides"
    ];

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setLoadingText("Analyzing text...");
        setMessage(null);
        setError(null);

        if (!file) {
            setError("Please upload a PowerPoint template file");
            setLoading(false);
            return;
        }

        if (!textInput || textInput.trim().length < 20) {
            setError("Please enter at least 20 characters of content");
            setLoading(false);
            return;
        }

        const formData = new FormData();
        formData.append('text_input', textInput);
        if (guidance) formData.append('guidance', guidance);
        formData.append('api_key', apiKey);
        formData.append('file', file);

        try {
            // Simulate progress stages
            setTimeout(() => setLoadingText("Extracting template style..."), 1500);
            setTimeout(() => setLoadingText("Planning slides with AI..."), 3500);
            setTimeout(() => setLoadingText("Generating presentation..."), 6000);

            const blob = await generatePPT(formData);

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "generated_presentation.pptx";
            document.body.appendChild(a);
            a.click();
            a.remove();

            setMessage("✅ Presentation generated and downloaded successfully!");
        } catch (err) {
            // Enhanced error messages
            let safeError = "Something went wrong. Please check your inputs and try again.";

            const errMsg = err.message || "";

            if (errMsg.includes("400") || errMsg.includes("Bad Request")) {
                safeError = "Invalid input. Please check your API key and template file.";
            } else if (errMsg.includes("401") || errMsg.includes("Unauthorized")) {
                safeError = "Authentication failed. Your API key is invalid or expired.";
            } else if (errMsg.includes("403") || errMsg.includes("Forbidden")) {
                safeError = "Access denied. Please check your API key permissions.";
            } else if (errMsg.includes("500") || errMsg.includes("Server")) {
                safeError = "Server error. Please try again with shorter text or a simpler template.";
            } else if (errMsg.includes("timeout") || errMsg.includes("Timeout")) {
                safeError = "Request timed out. The AI service might be slow. Please try again.";
            } else if (errMsg.includes("network") || errMsg.includes("Network")) {
                safeError = "Network error. Please check your internet connection.";
            }

            setError(safeError);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-form-container">
            <h2>Create Presentation</h2>
            <form onSubmit={handleSubmit} className="upload-form">
                <div className="form-group">
                    <label htmlFor="textInput">Content/Topic:</label>
                    <textarea
                        id="textInput"
                        value={textInput}
                        onChange={(e) => setTextInput(e.target.value)}
                        required
                        placeholder="Enter the main topic or content (min 50 words recommended)..."
                        rows={6}
                    />
                    {textInput.length > 20 && (
                        <small className="estimation-text">
                            Estimated slides: <strong>{estimatedSlides} - {estimatedSlides + 2}</strong>
                        </small>
                    )}
                </div>

                <div className="form-group">
                    <label htmlFor="guidance">Tone & Style (Guidance):</label>
                    <div className="presets-container">
                        {presets.map((preset) => (
                            <button
                                key={preset}
                                type="button"
                                className={`preset-btn ${selectedPreset === preset ? 'selected' : ''}`}
                                onClick={() => handlePreset(preset)}
                            >
                                {preset}
                            </button>
                        ))}
                    </div>
                    <input
                        type="text"
                        id="guidance"
                        value={guidance}
                        onChange={(e) => setGuidance(e.target.value)}
                        placeholder="e.g., Professional, for engineers..."
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="apiKey">API Key (OpenAI, Anthropic, or Gemini):</label>
                    <input
                        type="password"
                        id="apiKey"
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        required
                        placeholder="sk-... or sk-ant-... or AIza..."
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="file">Upload Reference Template (.pptx):</label>
                    <input
                        type="file"
                        id="file"
                        accept=".pptx"
                        onChange={handleFileChange}
                        required
                    />
                </div>

                <button type="submit" disabled={loading} className={`submit-btn ${loading ? 'loading' : ''}`}>
                    {loading ? (
                        <span className="loading-content">
                            <span className="spinner"></span> {loadingText}
                        </span>
                    ) : 'Generate Presentation'}
                </button>
            </form>

            {message && <div className="success-message">{message}</div>}
            {error && <div className="error-message">{error}</div>}
        </div>
    );
};

export default UploadForm;
