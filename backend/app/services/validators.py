from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class Slide(BaseModel):
    title: str = Field(..., min_length=1)
    bullets: List[str] = Field(..., min_length=1)
    notes: Optional[str] = None

    @field_validator('bullets')
    def bullets_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Bullets list cannot be empty')
        # Check specific constraints like word count if needed, but keeping it flexible for now
        return v

class SlidePlanMeta(BaseModel):
    estimated_duration_minutes: float
    slide_count: int
    tone: str

class SlidePlan(BaseModel):
    slides: List[Slide]
    meta: SlidePlanMeta

    @field_validator('slides')
    def validate_slide_count(cls, v):
        if len(v) < 3:
            raise ValueError('Plan must have at least 3 slides')
        return v
