import PyPDF2
import re
from typing import List, Dict
from difflib import SequenceMatcher

#Read the user's resume from a PDF file and extract the text
def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def normalize(text):
    return re.sub(r'[\W_]+', '', text.lower())


#Uses the SequenceMatcher to compare the resume text with job ad keywords and requirements
def suggest_resume_improvements(resume_text: str, job_keywords: List[str], job_requirements: str) -> Dict:
    resume_words = set(normalize(word) for word in re.findall(r'\w+', resume_text))
    keyword_suggestions = []

    for keyword in job_keywords:
        if normalize(keyword) not in resume_words:
            keyword_suggestions.append(keyword)

    # Split requirements by comma and newline
    import itertools
    requirement_lines = list(itertools.chain.from_iterable(
        [req.strip() for req in line.split(",")] for line in job_requirements.split("\n") if line.strip()
    ))
    requirement_lines = [req for req in requirement_lines if req]

    improvement_suggestions = []

    resume_lines = [normalize(line) for line in resume_text.splitlines() if line.strip()]

    for req in requirement_lines:
        req_norm = normalize(req)
        match_found = False

        for line in resume_lines:
            if req_norm in line:
                match_found = True
                break
            similarity = SequenceMatcher(None, req_norm, line).ratio()
            if similarity > 0.8:
                match_found = True
                break

        if not match_found:
            improvement_suggestions.append(req)

    return {
        "missing_keywords": keyword_suggestions,
        "unmet_requirements": improvement_suggestions
    }

