import httpx
import logging
from .base import LLMClient

logger = logging.getLogger("LLMClient")

class AnthropicClient(LLMClient):
    async def generate(self, prompt: str, api_key: str) -> str:
        """
        Anthropic Claude API client.
        Supports Claude 3 models (Haiku, Sonnet, Opus).
        """
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        
        # Use Claude 3 Haiku for speed and cost-effectiveness
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 2000,
            "temperature": 0.3,
            "messages": [
                {
                    "role": "user",
                    "content": f"You are a helpful assistant that outputs JSON.\n\n{prompt}"
                }
            ]
        }

        timeout = httpx.Timeout(30.0, connect=5.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()
                result = response.json()
                
                # Extract text from Anthropic response structure
                try:
                    # Anthropic returns content as an array of content blocks
                    content = result['content'][0]['text']
                    return content
                except (KeyError, IndexError) as e:
                    logger.error(f"Anthropic Response Parse Error: {result}")
                    raise ValueError("Unexpected response format from Anthropic")
                    
            except httpx.HTTPStatusError as e:
                logger.error(f"Anthropic API Error: {e.response.status_code} - {e.response.text}")
                raise ValueError(f"Provider Error: {e.response.status_code}")
            except Exception as e:
                logger.error(f"Network/Client Error: {str(e)}")
                raise ValueError("LLM Connection Failed")
