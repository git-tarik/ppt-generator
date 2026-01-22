import json
import logging
from app.services.llm.openai import OpenAIClient
from app.services.prompt_builder import build_planning_prompt
from app.services.validators import SlidePlan

logger = logging.getLogger("SlidePlanner")
logger.setLevel(logging.INFO)

if not logger.handlers:
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("[%(name)s] %(levelname)s: %(message)s"))
    logger.addHandler(sh)
logger.propagate = False

# Instantiate client once (or dependency inject)
llm_client = OpenAIClient()

async def generate_slide_plan(text_input: str, guidance: str | None, api_key: str) -> dict:
    prompt = build_planning_prompt(text_input, guidance)
    
    max_retries = 2
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            logger.info(f"Generating plan (Attempt {attempt + 1}/{max_retries + 1})...")
            raw_response = await llm_client.generate(prompt, api_key)
            
            cleaned_response = raw_response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            try:
                data = json.loads(cleaned_response)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON output from LLM")
            
            plan = SlidePlan(**data)
            
            logger.info(f"Plan validation successful. {len(plan.slides)} slides generated.")
            return plan.model_dump()
            
        except ValueError as e:
            logger.warning(f"Validation failed: {e}")
            last_error = e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            last_error = e
            
    logger.error("All generation attempts failed.")
    raise ValueError(f"Failed to generate valid plan after retries: {last_error}")
