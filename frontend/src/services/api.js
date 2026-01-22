const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export async function generatePPT(formData) {
    const response = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Generation failed');
    }

    return response.blob();
}
