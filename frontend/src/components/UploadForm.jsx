import React, { useState } from 'react';
import { generatePPT } from '../services/api';
import './UploadForm.css';

const UploadForm = () => {
    const [textInput, setTextInput] = useState('');
    const [guidance, setGuidance] = useState('');
    const [apiKey, setApiKey] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
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
            setError(err.message);
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
                        placeholder="Enter the main topic or content..."
                        rows={5}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="guidance">Guidance (Optional):</label>
                    <input
                        type="text"
                        id="guidance"
                        value={guidance}
                        onChange={(e) => setGuidance(e.target.value)}
                        placeholder="e.g., Target audience"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="apiKey">API Key:</label>
                    <input
                        type="password"
                        id="apiKey"
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        required
                        placeholder="Enter your dummy API key"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="file">Upload Reference File (.pptx):</label>
                    <input
                        type="file"
                        id="file"
                        accept=".pptx"
                        onChange={handleFileChange}
                        required
                    />
                </div>

                <button type="submit" disabled={loading} className="submit-btn">
                    {loading ? 'Generating...' : 'Generate PPT'}
                </button>
            </form>

            {message && <div className="success-message">{message}</div>}
            {error && <div className="error-message">{error}</div>}
        </div>
    );
};

export default UploadForm;
