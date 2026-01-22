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
            setFile(e.target.files[0]);
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
            setError("Please upload a file");
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
            setTimeout(() => setLoadingText("Planning slides..."), 2000);
            setTimeout(() => setLoadingText("Generating presentation..."), 5000);

            const blob = await generatePPT(formData);

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "generated_presentation.pptx";
            document.body.appendChild(a);
            a.click();
            a.remove();

            setMessage("Presentation generated and downloaded!");
        } catch (err) {
            // Friendly error messages
            let safeError = "Something went wrong. Please check your API key and try again.";
            if (err.message.includes("400")) safeError = "Invalid input. Please check your text and API key.";
            if (err.message.includes("401")) safeError = "Authentication failed. Invalid API Key.";
            if (err.message.includes("500")) safeError = "Server hiccup. Please try again with shorter text.";

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
                    <label htmlFor="apiKey">API Key (OpenAI or Gemini):</label>
                    <input
                        type="password"
                        id="apiKey"
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        required
                        placeholder="sk-... or AIza..."
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
