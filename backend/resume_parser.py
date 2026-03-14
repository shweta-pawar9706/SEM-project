import fitz
from docx import Document
import re

SKILLS_DB = [
    "python", "java", "javascript", "c++", "c#", "c", "r", "swift",
    "kotlin", "typescript", "php", "ruby", "go", "rust", "scala",
    "html", "css", "react", "angular", "vue", "nodejs", "express",
    "bootstrap", "tailwind", "jquery", "nextjs", "flask", "django",
    "machine learning", "deep learning", "data analysis", "nlp",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas",
    "numpy", "matplotlib", "seaborn", "opencv",
    "sql", "mysql", "postgresql", "mongodb", "firebase", "redis",
    "sqlite", "oracle",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github",
    "linux", "jenkins", "ci/cd",
    "excel", "powerpoint", "tableau", "power bi", "figma", "jira",
    "postman", "vs code", "android studio",
    "communication", "teamwork", "leadership", "problem solving",
    "time management", "critical thinking", "project management",
    "ui", "ux", "ui design", "ux design", "ui and ux",
    "wordpress", "responsive web design", "rest api", "api"
]


def extract_text(filepath):
    text = ""
    try:
        if filepath.endswith(".pdf"):
            doc = fitz.open(filepath)
            for page in doc:
                # Try normal text extraction first
                page_text = page.get_text("text")
                if page_text.strip():
                    text += page_text
                else:
                    # Fallback — extract text in reading order with blocks
                    blocks = page.get_text("blocks")
                    for block in blocks:
                        if block[6] == 0:  # Text block
                            text += block[4] + "\n"

        elif filepath.endswith(".docx"):
            doc = Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"

    except Exception as e:
        print("Error extracting text:", e)

    print("Extracted text preview:", text[:500])  # Debug log
    return text


def extract_email(text):
    # Handle emails split across lines like "pawarshweta697@gmail.co\nm"
    text_clean = text.replace("\n", " ")
    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    match = re.findall(pattern, text_clean)
    return match[0] if match else "Not found"


def extract_phone(text):
    pattern = r'(\+?\d[\d\s\-]{8,13}\d)'
    match = re.findall(pattern, text)
    return match[0].strip() if match else "Not found"


def extract_name(text):
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    for line in lines:
        # Name is usually short, all letters and spaces, near top
        if (len(line) > 3 and len(line) < 40
                and "@" not in line
                and not any(char.isdigit() for char in line)
                and line.replace(" ", "").isalpha()):
            return line.title()
    return lines[0] if lines else "Not found"


def extract_skills(text):
    text_lower = text.lower()
    found_skills = []
    for skill in SKILLS_DB:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))


def extract_education(text):
    education = []
    keywords = [
        "b.e", "b.tech", "m.tech", "bsc", "msc", "bca", "mca",
        "bachelor", "master", "phd", "diploma", "hsc", "ssc",
        "12th", "10th", "engineering", "computer science",
        "information technology", "mba", "ioit", "institute",
        "university", "college", "school", "2024", "2025",
        "2026", "2027", "2028"
    ]
    lines = text.lower().split("\n")
    for line in lines:
        for keyword in keywords:
            if keyword in line:
                clean_line = line.strip()
                if clean_line and len(clean_line) > 3 and clean_line not in education:
                    education.append(clean_line.title())
                break
    return education if education else ["Not found"]


def extract_experience(text):
    experience = []
    keywords = [
        "experience", "worked at", "working at", "internship",
        "intern at", "developer at", "engineer at", "analyst at",
        "trainee", "project at", "employed", "website developer",
        "web developer", "developed", "designed", "built", "created"
    ]
    lines = text.lower().split("\n")
    for line in lines:
        for keyword in keywords:
            if keyword in line:
                clean_line = line.strip()
                if clean_line and len(clean_line) > 5 and clean_line not in experience:
                    experience.append(clean_line.title())
                break
    return experience if experience else ["No experience found"]


def parse_resume(filepath):
    text = extract_text(filepath)

    if not text.strip():
        return {
            "name": "Not found",
            "email": "Not found",
            "phone": "Not found",
            "skills": [],
            "education": ["Not found"],
            "experience": ["No experience found"],
            "raw_text": "",
            "error": "Could not extract text — resume may be image based"
        }

    parsed = {
        "name":       extract_name(text),
        "email":      extract_email(text),
        "phone":      extract_phone(text),
        "skills":     extract_skills(text),
        "education":  extract_education(text),
        "experience": extract_experience(text),
        "raw_text":   text
    }

    return parsed