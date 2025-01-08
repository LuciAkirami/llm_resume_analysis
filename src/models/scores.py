from pydantic import BaseModel, Field
from typing import List


class SkillScore(BaseModel):
    score: int = Field(
        description="A score between 0 to 100 based on how close the job description skills are to the given candidate skills"
    )
    matching_skills: List[str] = Field(
        description="List of key matching skills from comparing the Job Description and Candidate Resume"
    )
    missing_skills: List[str] = Field(
        description="List of skills that the candidate is missing which the Job Description states"
    )
    reason: str = Field("Reasononing of why this particular score is assigned")


class ExperienceScore(BaseModel):
    score: int = Field(
        description="A score between 0 to 100 based on how close the job description experience are to the given relvant candidate experience"
    )
    reason: str = Field("Reasononing of why this particular score is assigned")


class EducationScore(BaseModel):
    score: int = Field(
        description="A score between 0 to 100 based on how close the job description education qualifications/certifications are to the given \
        candidate education qualifications / certifications"
    )
    reason: str = Field("Reasononing of why this particular score is assigned")


class OtherScore(BaseModel):
    score: int = Field(
        description="A score between 0 to 100 based on how close the other relevant skils are"
    )
    reason: str = Field("Reasononing of why this particular score is assigned")


class Recommendations(BaseModel):
    recommendations: str = Field(
        description="Recommendations for the candidate to improve in Markdown format"
    )
