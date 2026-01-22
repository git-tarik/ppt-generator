import httpx
import logging
import json
from .base import LLMClient

logger = logging.getLogger("LLMClient")

class GeminiClient(LLMClient):
    async def generate(self, prompt: str, api_key: str) -> str:
        # Use Gemini 1.5 Flash for speed and efficiency
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Construct payload with JSON mode forced
        data = {
            "contents": [{
                "parts": [{"text": "You are a helpful assistant that outputs JSON.\n" + prompt}]
            }],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.3
            }
        }

        timeout = httpx.Timeout(30.0, connect=5.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()
                result = response.json()
                
                # Extract text from Gemini response structure
                try:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    return content
                except (KeyError, IndexError) as e:
                    logger.error(f"Gemini Response Parse Error: {result}")
                    raise ValueError("Unexpected response format from Gemini")
                    
            except httpx.HTTPStatusError as e:
                logger.error(f"Gemini API Error: {e.response.status_code} - {e.response.text}")
                raise ValueError(f"Provider Error: {e.response.status_code}")
            except Exception as e:
                logger.error(f"Network/Client Error: {str(e)}")
                raise ValueError("LLM Connection Failed")
