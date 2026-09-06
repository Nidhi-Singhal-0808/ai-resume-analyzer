import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def analyze_resume_with_gemini(resume_text, job_description):
    """
    Sends resume text and job description to Gemini and returns structured JSON analysis.
    """
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from environment variables.")
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert HR recruiter and ATS (Applicant Tracking System) specialist. 
    Analyze the provided resume against the given Job Description objectively. 
    Do not invent or assume experience that is not explicitly mentioned in the resume.
    
    JOB DESCRIPTION:
    {job_description}
    
    RESUME TEXT:
    {resume_text}
    
    Provide your analysis strictly in valid JSON format with the following exact keys:
    - "overall_score": integer between 0 and 100 representing general fit
    - "ats_score": integer between 0 and 100 representing keyword and format matching
    - "matching_skills": list of strings (skills found in both resume and JD)
    - "missing_skills": list of strings (important skills in JD missing from resume)
    - "strengths": list of strings (key strengths of the resume for this role)
    - "weaknesses": list of strings (areas of concern or gaps)
    - "missing_keywords": list of strings (important keywords absent from resume)
    - "improvement_suggestions": list of strings (actionable recommendations)
    
    Return ONLY valid JSON. No markdown code blocks, no introductory text, no conversational filler.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    # Clean response text in case model wraps output in markdown blocks
    raw_text = response.text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    raw_text = raw_text.strip()
    
    try:
        parsed_data = json.loads(raw_text)
        return parsed_data
    except json.JSONDecodeError:
        raise ValueError("The AI model returned an invalid structure. Please try again.")