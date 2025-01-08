from .base_models import Experience, Education, OtherSkills
from pydantic import BaseModel, Field
from typing import List


class JobRequirements(BaseModel):
    """Job requirements specification"""

    required_skills: List[str] = Field(
        description="List of technical skills required for the position"
    )
    required_experience: Experience = Field(
        description="Details about required work experience"
    )
    required_education: Education = Field(
        description="Educational and certification requirements"
    )
    other_requirements: OtherSkills = Field(
        description="Additional requirements including soft skills and logistics"
    )
