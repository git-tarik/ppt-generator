from pydantic import BaseModel
from typing import Optional

class GenerateRequest(BaseModel):
    text_input: str
    guidance: Optional[str] = None
    api_key: str
