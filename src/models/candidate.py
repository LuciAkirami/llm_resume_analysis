from .base_models import Experience, Education, OtherSkills
from pydantic import BaseModel, Field
from typing import List


class CandidateProfile(BaseModel):
    """Candidate Profile"""

    name: str = Field(description="Name of the Candidate")
    skills: List[str] = Field(
        description="List of technical skills acquired by the candidate"
    )
    experience: Experience = Field(
        description="Details about work experience of the candidate"
    )
    education: Education = Field(
        description="Educational and certification of the candidate"
    )
    other_skills: OtherSkills = Field(
        description="Additional skills including soft skills and logistics"
    )
    brief_description: str = Field(
        description="A brief summary of the resume covering all aspects"
    )
