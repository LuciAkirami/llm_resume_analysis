import json
from typing import Dict, List

from .models.candidate import CandidateProfile
from .models.job import JobRequirements
from .models.scores import (
    SkillScore,
    ExperienceScore,
    EducationScore,
    OtherScore,
    Recommendations,
)

from .prompts.templates import (
    resume_extract_prompt_template,
    jd_extract_prompt_template,
    skills_score_prompt_template,
    experience_score_prompt_template,
    education_score_prompt_template,
    other_score_prompt_template,
    recommendations_prompt_template,
)

from .utils.pdf_loader import get_current_date

from langchain_core.prompts import ChatPromptTemplate


class ResumeAnalysisSystem:

    def __init__(self, llm):
        """
        Initializes the ResumeAnalysisSystem with a Large Language Model (LLM) object.
        """
        self.llm = llm
        self.weights = {
            "skills": 0.4,
            "experience": 0.3,
            "education": 0.2,
            "other": 0.1,
        }
        self.results = []

    def get_structured_llm_chain(self, structured_class, prompt_template):
        """
        Creates a Runnable Chain.

        Args:
            structured_class: The Pydantic class representing the desired structured output.
            prompt_template: The template prompt for the LLM chain.

        Returns:
            A Langchain object representing the LLM prompt chain.
        """

        structured_llm = self.llm.with_structured_output(structured_class)
        chain = prompt_template | structured_llm
        return chain

    def extract_resume_components(self, resume_text: str) -> CandidateProfile:
        """
        Extracts components (skills, experience, education, etc.) from a resume text using the LLM chain.

        Args:
            resume_text: The text content of the resume.

        Returns:
            A CandidateProfile object containing extracted information.
        """
        chain = self.get_structured_llm_chain(
            CandidateProfile, resume_extract_prompt_template
        )
        return chain.invoke(
            {"resume_text": resume_text, "current_date": get_current_date()}
        )

    def analyze_job_description(self, jd_text: str) -> JobRequirements:
        """
        Extracts requirements (skills, experience, education, etc.) from a job description using the LLM chain.

        Args:
            jd_text: The text content of the job description.

        Returns:
            A JobRequirements object containing extracted requirements.
        """
        chain = self.get_structured_llm_chain(
            JobRequirements, jd_extract_prompt_template
        )
        return chain.invoke({"jd_text": jd_text})

    def calculate_skills_score(
        self, resume_skills: List[str], required_skills: List[str]
    ) -> SkillScore:
        """
        Calculates a skill score based on matching and missing skills between resume and job description.

        Args:
            resume_skills: List of skills extracted from the resume.
            required_skills: List of skills required by the job description.

        Returns:
            A SkillScore object containing the score and reason.
        """
        chain = self.get_structured_llm_chain(SkillScore, skills_score_prompt_template)
        response = chain.invoke(
            {"resume_skills": resume_skills, "required_skills": required_skills}
        )

        return response

    def calculate_experience_score(
        self, resume_exp: Dict, required_exp: Dict
    ) -> ExperienceScore:
        """
        Calculates an experience score based on the relevance of experience in the resume to the job description.

        Args:
            resume_exp: A dictionary representing experience details from the resume.
            required_exp: A dictionary representing experience requirements from the job description.

        Returns:
            An ExperienceScore object containing the score and reason.
        """
        chain = self.get_structured_llm_chain(
            ExperienceScore, experience_score_prompt_template
        )
        response = chain.invoke(
            {
                "resume_exp": json.dumps(resume_exp),
                "required_exp": json.dumps(required_exp),
            }
        )

        return response

    def calculate_education_score(
        self, resume_edu: Dict, required_edu: Dict
    ) -> EducationScore:
        """
        Calculates an education score based on the match between education in the resume and the job description.

        Args:
            resume_edu: A dictionary representing education details from the resume.
            required_edu: A dictionary representing education requirements from the job description.

        Returns:
            An EducationScore object containing the score and reason.
        """
        chain = self.get_structured_llm_chain(
            EducationScore, education_score_prompt_template
        )
        response = chain.invoke(
            {
                "resume_edu": json.dumps(resume_edu),
                "required_edu": json.dumps(required_edu),
            }
        )

        return response

    def calculate_other_score(
        self, resume_other: Dict, required_other: Dict
    ) -> OtherScore:
        """
        Calculates a score for other factors (soft skills, location, etc.) based on the resume and job description.

        Args:
            resume_other: A dictionary representing other factors from the resume.
            required_other: A dictionary representing other requirements from the job description.

        Returns:
            An OtherScore object containing the score and reason.
        """
        chain = self.get_structured_llm_chain(OtherScore, other_score_prompt_template)
        response = chain.invoke(
            {
                "resume_other": json.dumps(resume_other),
                "required_other": json.dumps(required_other),
            }
        )

        return response

    def provide_recommendations(
        self,
        resume_skills: Dict,
        resume_experience: Dict,
        jd_experience: Dict,
        jd_text: str,
    ) -> Recommendations:
        """
        Provides recommendations for the candidate based on the analysis.

        Args:
            resume_skills: A dictionary of skills from the resume including matching and missing skills.
            resume_experience: A dictionary representing experience details from the resume.
            jd_experience: A dictionary representing experience requirements from the job description.
            jd_text: The text content of the job description.

        Returns:
            A Recommendations object containing the recommendations in Markdown format.
        """
        chain = self.get_structured_llm_chain(
            Recommendations, recommendations_prompt_template
        )

        matching_skills = resume_skills["matching_skills"]
        missing_skills = resume_skills["missing_skills"]

        response = chain.invoke(
            {
                "jd_text": {jd_text},
                "matching_skills": {json.dumps(matching_skills)},
                "missing_skills": {json.dumps(missing_skills)},
                "candidate_experience": {json.dumps(resume_experience)},
                "required_experience": {json.dumps(jd_experience)},
            }
        )

        return response

    def analyze_resume(self, resume_text: str, job_description: str) -> Dict:
        """
        Analyzes a single resume against a job description and returns a comprehensive analysis result.

        Args:
            resume_text: The text content of the resume.
            job_description: The text content of the job description.

        Returns:
            A dictionary containing the analysis results, including scores, reasons, analysis summary, and recommendations.
        """

        # Extract components
        resume_components = self.extract_resume_components(resume_text)
        jd_components = self.analyze_job_description(job_description)

        # Calculate scores
        skills_response = self.calculate_skills_score(
            resume_components.skills, jd_components.required_skills
        )
        skills_score = skills_response.score * self.weights["skills"]

        experience_response = self.calculate_experience_score(
            resume_components.experience.model_dump(),
            jd_components.required_experience.model_dump(),
        )
        experience_score = experience_response.score * self.weights["experience"]

        education_response = self.calculate_education_score(
            resume_components.education.model_dump(),
            jd_components.required_education.model_dump(),
        )
        education_score = education_response.score * self.weights["education"]

        other_response = self.calculate_other_score(
            resume_components.other_skills.model_dump(),
            jd_components.other_requirements.model_dump(),
        )
        other_score = other_response.score * self.weights["other"]

        # Calculate total score
        total_score = skills_score + experience_score + education_score + other_score

        # Get recommendations
        recommendations = self.provide_recommendations(
            skills_response.model_dump(),
            resume_components.experience.model_dump(),
            jd_components.required_experience.model_dump(),
            job_description,
        )

        return {
            "name": resume_components.name,
            "total_score": total_score,
            "component_scores": {
                "skills": {"score": skills_score, "reason": skills_response.reason},
                "experience": {
                    "score": experience_score,
                    "reason": experience_response.reason,
                },
                "education": {
                    "score": education_score,
                    "reason": education_response.reason,
                },
                "other": {"score": other_score, "reason": other_response.reason},
            },
            "analysis": {
                "matching_skills": resume_components.skills,
                "experience_summary": resume_components.experience.model_dump(),
                "education_summary": resume_components.education.model_dump(),
                "other_factors": resume_components.other_skills.model_dump(),
            },
            "recommendations": recommendations.recommendations,
        }

    def analyze_multiple_resumes(
        self, resumes: List[str], job_description: str
    ) -> List[Dict]:
        """
        Analyzes multiple resumes against a job description.

        Args:
            resumes: A list of resume texts.
            job_description: The text content of the job description.

        Returns:
            A list of dictionaries, where each dictionary contains the analysis results for a single resume.
        """
        for resume in resumes:
            result = self.analyze_resume(resume, job_description)
            self.results.append(result)

        return self.results
