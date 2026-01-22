import json

def build_planning_prompt(text_input: str, guidance: str | None) -> str:
    """
    Constructs the system verification prompt for the LLM.
    """
    
    guidance_section = f"Guidance/Tone: {guidance}" if guidance else "Tone: Professional and clear."

    prompt = f"""
You are an expert presentation designer.
Analyze the following text and return a structured slide plan as JSON.

OBJECTIVE:
Transform the input text into a slide deck plan.
- Break down the content into logical slides.
- Create a title for each slide.
- Extract key points as concise bullets (max 15 words per bullet).
- Add speaker notes if helpful.

CONSTRAINTS:
- Use JSON format ONLY.
- The JSON must match the schema provided below.
- Create at least 3 slides.
- Do NOT hallucinate facts not present in the input text.
- Do NOT use markdown code blocks (```json). Just raw JSON.

SCHEMA:
{{
  "slides": [
    {{
      "title": "string",
      "bullets": ["string", "string"],
      "notes": "string (optional)"
    }}
  ],
  "meta": {{
    "estimated_duration_minutes": number,
    "slide_count": number,
    "tone": "string"
  }}
}}

INPUT TEXT:
{text_input}

{guidance_section}
"""
    return prompt.strip()
