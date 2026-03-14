def analyze_skill_gap(data):
    resume_skills = [s.lower() for s in data.get("resume_skills", [])]
    job_description = data.get("job_description", "").lower()

    if not job_description:
        return {"error": "Job description is missing"}

    # ─────────────────────────────────────────
    # SKILLS DATABASE (same as resume_parser)
    # ─────────────────────────────────────────
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
        "ui", "ux", "ui design", "ux design", "rest api", "api",
        "wordpress", "responsive web design"
    ]

    # ─────────────────────────────────────────
    # STEP 1 — Extract skills from JD
    # ─────────────────────────────────────────
    jd_skills = []
    for skill in SKILLS_DB:
        if skill.lower() in job_description:
            jd_skills.append(skill.lower())

    if not jd_skills:
        return {"error": "No recognizable skills found in job description"}

    # ─────────────────────────────────────────
    # STEP 2 — Compare resume skills vs JD skills
    # ─────────────────────────────────────────
    matched_skills = []
    missing_skills = []

    for skill in jd_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # ─────────────────────────────────────────
    # STEP 3 — Calculate percentages
    # ─────────────────────────────────────────
    total         = len(jd_skills)
    matched_count = len(matched_skills)
    missing_count = len(missing_skills)
    match_percent = round((matched_count / max(total, 1)) * 100)
    gap_percent   = 100 - match_percent

    # ─────────────────────────────────────────
    # STEP 4 — Generate recommendations
    # ─────────────────────────────────────────
    recommendations = []
    if match_percent >= 80:
        recommendations.append("Great match! You have most of the required skills.")
    elif match_percent >= 50:
        recommendations.append("Good match! Focus on learning the missing skills.")
    else:
        recommendations.append("Significant skill gap found. Start learning missing skills immediately.")

    if missing_count > 0:
        recommendations.append(f"You are missing {missing_count} skills required for this role.")
        recommendations.append("Check the Course Recommendations page to learn missing skills.")

    return {
        "jd_skills":       jd_skills,
        "matched_skills":  matched_skills,
        "missing_skills":  missing_skills,
        "total_skills":    total,
        "matched_count":   matched_count,
        "missing_count":   missing_count,
        "match_percent":   match_percent,
        "gap_percent":     gap_percent,
        "recommendations": recommendations
    }