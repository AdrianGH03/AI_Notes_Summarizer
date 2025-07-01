from transformers import pipeline
from typing import List, Dict
import re


# Initialize Hugging Face pipelines
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
keyword_extractor = pipeline("feature-extraction", model="distilbert-base-uncased")

#Only look for common requirements in job ads
REQUIREMENTS_LIST = [
    # Languages
    "python", "java", "javascript", "typescript", "c#", "c++", "go", "ruby", "php", "swift", "kotlin",
    # Frameworks/Libraries
    "react", "next.js", "angular", "vue", "django", "flask", "express", "spring", "fastapi", "node.js",
    # Databases
    "mongodb", "postgresql", "mysql", "sqlite", "redis", "oracle", "mariadb", "dynamodb",
    # DevOps/Tools
    "ci/cd", "docker", "kubernetes", "aws", "azure", "gcp", "jenkins", "git", "github", "gitlab",
    # Methodologies
    "agile", "scrum", "kanban", "waterfall", "xp", "tdd", "bdd",
    # Other
    "rest", "graphql", "microservices", "serverless",
    "api", "web services", "cloud computing", "machine learning", "data analysis", "big data",
    "artificial intelligence", "cybersecurity", "networking", "mobile development",
    "ui/ux design", "responsive design", "cross-platform development", "performance optimization",
    "version control", "testing", "debugging", "documentation", "code review",
    "problem solving", "communication", "teamwork", "time management", "adaptability", "attention to detail"
]

#Clean the text of any unnecessary characters and whitespace
def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def summarize_text(text: str) -> str:
    cleaned = clean_text(text)
    if not cleaned or len(cleaned.split()) < 10:
        raise ValueError("Text too short for summarization.")
    if len(cleaned.split()) > 1024:
        raise ValueError("Text too long for summarization.")
    result = summarizer(cleaned, max_length=100, min_length=30, do_sample=False)
    return result[0]['summary_text']

def extract_keywords(text: str, top_k: int = 10) -> List[str]:
    cleaned = clean_text(text).lower()
    words = cleaned.split()
    #Stop common words in sentences from being counted as keywords
    stopwords = set([
        "the", "and", "is", "in", "to", "of", "a", "for", "on", "with", "as", "by", "an", "at", "from", "or", "that", "it"
    ])
    filtered_words = [word for word in words if word not in stopwords and len(word) > 2]
    freq = {}
    for word in filtered_words:
        freq[word] = freq.get(word, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, count in sorted_words[:top_k]]
    return keywords

#Find requirements in job ad text
def extract_requirements(text: str) -> str:
    text_lower = text.lower()
    found = []
    for req in REQUIREMENTS_LIST:
        if re.search(r'\b' + re.escape(req) + r'\b', text_lower):
            found.append(req)
    return ", ".join(sorted(set(found)))

#Call everything here to summarize
def summarize_and_keywords(text: str) -> Dict[str, object]:
    summary = summarize_text(text)
    keywords = extract_keywords(summary)
    requirements = extract_requirements(text)
    return {
        "summary": summary,
        "keywords": keywords,
        "requirements": requirements
    }