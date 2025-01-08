from typing import Optional, List, Tuple, Dict
from pydantic import BaseModel, Field


class ExperiencePerRole(BaseModel):
    role: str = Field(description="Role")
    years: str = Field(description="Years of experience")


class Experience(BaseModel):
    years_per_role: List[ExperiencePerRole] = Field(
        description="Years of experience for each role"
    )
    domains: List[str] = Field(
        description="List of specific domains or areas of expertise the candidate worked in"
    )
    levels: List[str] = Field(
        description="List of experience levels (e.g., Junior, Senior, Lead)"
    )


class Education(BaseModel):
    degrees: List[str] = Field(description="List of required educational degrees")
    certifications: List[str] = Field(
        description="List of required professional certifications"
    )


class OtherSkills(BaseModel):
    soft_skills: List[str] = Field(
        description="List of required soft skills and interpersonal abilities"
    )
    languages: List[str] = Field(description="List of languages")
    location: str = Field(
        description="Location requirements or work arrangement (e.g., Remote, Hybrid, On-site)"
    )
