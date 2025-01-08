from langchain_core.prompts import ChatPromptTemplate

resume_user_template = """
Analyze the following resume and extract key components.

- List of skills
- Work experience (with duration)
- Education and certifications
- Other relevant information (languages, location, soft skills)

Current Date:
{current_date} (Useful for calculating experience as of current date)

Candidate Resume:
{resume_text}
"""
resume_extract_prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are a skilled HR analyst who extracts structured requirements from candidate resumes.",
        ),
        ("user", resume_user_template),
    ]
)


jd_user_template = """
Analyze this job description and extract key requirements.

- Required skills
- Required experience level and type
- Required education and certifications
- Other requirements (location, languages, etc.)

Job Description:
{jd_text}
"""
jd_extract_prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are a skilled HR analyst who extracts structured requirements from job descriptions.",
        ),
        (
            "user",
            jd_user_template,
        ),
    ]
)


skills_user_template = """
Compare these skill sets and rate the match from 0-100:
1. **Exact Matches**:
- Identify skills that appear directly in both the resume and the job description. Exact matches should be given the highest weight.

2. **Related/Similar Skills**:
- Consider skills that are not exact matches but are related or similar in function. For example, "Python" vs. "Data Science Programming" or "Machine Learning" vs. "AI."

3. **Industry-standard Alternatives**:
- Take into account industry-standard terms or synonymous skills. For instance, "Cloud Computing" might appear as "AWS" in the resume or job description.

- **Resume Skills**:
{resume_skills}

- **Required Skills**:
{required_skills}

Provide a score from 0 to 100 reflecting the overall match. If the candidate is only missing a few specific but crucial skills or has alternative terms, rate it higher within the range. If there are significant mismatches or missing essential skills, rate it lower.
"""
skills_score_prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are tasked with comparing two sets of skills: one from a resume and one from a job's requirements. \
    Your goal is to evaluate how closely they match on a scale from 0 to 100. Along with that, you even provide the list of matching and missing skills.",
        ),
        (
            "user",
            skills_user_template,
        ),
    ]
)


experience_user_template = """
Compare the experience and rate the match from 0-100:

1. **Years of Experience**:
- Compare the number of years listed in both the resume and the job description. If the candidate has a few months less experience than required, consider how relevant and impactful the shorter experience is.
- The experience must also be relevant. If the candidate has 6 years of FrontEnd and 2 Years of Data Engineer YOE and the job needs a Data Scientist with 3 YOE, then this person is not relevant and score is penalized

2. **Domains**:
- Evaluate how closely the domains in the resume align with those listed in the job description. If the candidate has experience in similar or advanced domains (e.g., Data Science vs. Product Analytics), consider the relevance and transferability of those skills to the job requirements.

3. **Levels**:
- Consider the role level in the resume (e.g., Full-time) and compare it to the job's level requirement (e.g., Mid-level). If the candidate has relevant experience at a similar level, even if not explicitly stated, adjust the match accordingly.

- **Resume Information**:
{resume_exp}

- **Job Description**:
{required_exp}

Provide a score from 0 to 100 reflecting the overall match. If the experience is close but not quite matching the requirements (e.g., a few months short or some domain differences), rate it higher within the range. If there are notable discrepancies (e.g., large differences in experience or completely mismatched domains), rate it lower.
"""
experience_score_prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are tasked with comparing two sets of experience: one from a resume and one from a job's requirements. \
    Your goal is to evaluate how closely they match on a scale from 0 to 100.",
        ),
        (
            "user",
            experience_user_template,
        ),
    ]
)


education_user_template = """
Compare education and certifications and rate the match from 0-100:
1. **Degree Level Match**:
- Compare the highest level of education listed in both the resume and the job description. If the candidate is just short of the required level (e.g., a Bachelor's instead of a Master's), consider how relevant and applicable their experience is in place of the missing degree.

2. **Field of Study Relevance**:
- Evaluate how closely the field of study in the resume aligns with the field required for the job. If the fields are similar but not exact (e.g., "Computer Science" vs. "Software Engineering"), give the candidate some credit for transferable knowledge.

3. **Required Certifications Present**:
- Check if the resume includes the specific certifications that are mandatory for the job. If they are missing, but the candidate has relevant alternative certifications, consider their applicability.

4. **Additional Relevant Certifications**:
- Consider any additional certifications listed in the resume that, while not required, could be highly relevant or beneficial for the job.

- **Resume Education and Certifications**:
{resume_edu}

- **Required Education and Certifications**:
{required_edu}

Provide a score from 0 to 100 reflecting the overall match. If the candidate has a degree close to the required level or a similar field of study, or if alternative certifications are highly relevant, adjust the score upwards. If there are major discrepancies, rate it lower.
"""
education_score_prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are tasked with comparing two sets of educational qualifications: one from a resume and one from a job's requirements. \
    Your goal is to evaluate how closely they match on a scale from 0 to 100.",
        ),
        (
            "user",
            education_user_template,
        ),
    ]
)


others_user_template = """
Compare other factors and rate the match from 0-100:
1. **Location Match**:
- Assess how closely the location listed in the resume aligns with the location requirement for the job. If the candidate is in a similar region or open to relocation, this should be considered a positive factor.

2. **Language Requirements**:
- Evaluate whether the resume meets the language requirements specified in the job description. If the candidate speaks a similar or equivalent language (e.g., fluent in French vs. proficient in a similar Romance language), this can be considered.

3. **Soft Skills Alignment**:
- Consider the alignment of soft skills (e.g., communication, teamwork, problem-solving) between the resume and the job requirements. If soft skills are not explicitly listed, evaluate the experience for signs of those skills (e.g., leadership roles, teamwork, or customer-facing work).

4. **Any Other Specified Requirements**:
- Take into account any additional factors mentioned in the resume or job description, such as willingness to travel, remote work preferences, or specific tools/technologies that could impact the candidate's fit for the role.

- **Resume Other Factors**:
{resume_other}

- **Required Other Factors**:
{required_other}

Provide a score from 0 to 100 reflecting the overall match. If the candidate meets or is close to meeting the location, language, or soft skill requirements, rate the match higher. If there are clear mismatches or missing key factors, rate it lower.
"""
other_score_prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are tasked with comparing other relevant factors: one from a resume and one from a job's requirements. \
    Your goal is to evaluate how closely they match on a scale from 0 to 100.",
        ),
        (
            "user",
            others_user_template,
        ),
    ]
)


recommendations_user_template = """
Given the following job description, along with the candidate's skill and experience scores, please generate a detailed list of recommendations for the candidate to improve upon in order to match the job requirements more closely. The recommendations should focus on closing gaps in both skills and experience, and should suggest actionable steps for improvement. 
Provide specific suggestions for acquiring missing skills or gaining relevant experience.

Job Description:
{jd_text}

Skills:
- Matching Skills: {matching_skills}
- Missing Skills: {missing_skills}

Experience:
- Candidate Experience: 
{candidate_experience}

- Required Experience: 
{required_experience}

Please include:
- Specific skills the candidate should focus on acquiring.
- Recommended courses, certifications, or resources for learning missing skills.
- Suggestions for gaining relevant experience or improving current experience.
- If applicable, suggestions for projects or practical activities the candidate can take on to build experience.
- STRICTLY USE MARKDOWN FORMAT

Your response should be actionable, clear, and tailored to the gaps identified in the provided scores.
Provide the response in Markdown format. 

DO NOT USE MAIN HEADING LIKE #, ##, ###
"""
recommendations_prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are a career advisor. Based on the provided job description, SkillS, and Experience, \
    generate actionable recommendations for the candidate to improve on missing skills and experience gaps. You only \
        respond in MARKDOWN FORMAT. DO NOT USE MAIN HEADING LIKE #, ##, ###",
        ),
        (
            "user",
            recommendations_user_template,
        ),
    ]
)
