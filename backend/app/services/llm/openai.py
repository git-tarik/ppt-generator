import httpx
import logging
from .base import LLMClient

logger = logging.getLogger("LLMClient")

class OpenAIClient(LLMClient):
    async def generate(self, prompt: str, api_key: str) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1500
        }

        timeout = httpx.Timeout(20.0, connect=5.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()
                result = response.json()
                content = result['choices'][0]['message']['content']
                return content
            except httpx.HTTPStatusError as e:
                logger.error(f"OpenAI API Error: {e.response.status_code} - {e.response.text}")
                raise ValueError(f"Provider Error: {e.response.status_code}")
            except Exception as e:
                logger.error(f"Network/Client Error: {str(e)}")
                raise ValueError("LLM Connection Failed")
