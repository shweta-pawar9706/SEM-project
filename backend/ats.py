def check_ats(data):
    resume_text = data.get("resume_text", "").lower()
    job_description = data.get("job_description", "").lower()

    if not resume_text or not job_description:
        return {"error": "Resume text or job description missing"}

    score = 0
    breakdown = {}
    tips = []
    matched_keywords = []
    missing_keywords = []

    # ─────────────────────────────────────────
    # CHECK 1 — Keyword Match (40 points)
    # ─────────────────────────────────────────
    import re
    # Extract meaningful words from JD (length > 3)
    jd_words = set(re.findall(r'\b[a-z]{4,}\b', job_description))
    # Remove common words
    stop_words = {
        "with", "that", "this", "have", "will", "from", "they",
        "been", "were", "your", "into", "more", "also", "about",
        "able", "when", "what", "some", "than", "then", "them",
        "these", "those", "such", "each", "must", "should", "would",
        "could", "their", "there", "where", "which", "while"
    }
    jd_keywords = jd_words - stop_words

    matched = []
    missing = []
    for word in jd_keywords:
        if word in resume_text:
            matched.append(word)
        else:
            missing.append(word)

    matched_keywords = matched[:20]   # Show top 20
    missing_keywords = missing[:20]   # Show top 20

    keyword_score = min(int((len(matched) / max(len(jd_keywords), 1)) * 40), 40)
    score += keyword_score
    breakdown["Keyword Match"] = keyword_score
    if keyword_score < 20:
        tips.append("Add more keywords from the job description to your resume.")

    # ─────────────────────────────────────────
    # CHECK 2 — Contact Info (15 points)
    # ─────────────────────────────────────────
    contact_score = 0
    if "@" in resume_text:
        contact_score += 8
    else:
        tips.append("Add your email address to your resume.")

    if any(char.isdigit() for char in resume_text):
        contact_score += 7
    else:
        tips.append("Add your phone number to your resume.")

    score += contact_score
    breakdown["Contact Info"] = contact_score

    # ─────────────────────────────────────────
    # CHECK 3 — Important Sections (20 points)
    # ─────────────────────────────────────────
    section_score = 0
    sections = {
        "education":   5,
        "experience":  5,
        "skills":      5,
        "project":     5
    }
    for section, points in sections.items():
        if section in resume_text:
            section_score += points
        else:
            tips.append(f"Add a '{section.title()}' section to your resume.")

    score += section_score
    breakdown["Resume Sections"] = section_score

    # ─────────────────────────────────────────
    # CHECK 4 — Resume Length (15 points)
    # ─────────────────────────────────────────
    word_count = len(resume_text.split())
    if word_count >= 300:
        length_score = 15
    elif word_count >= 150:
        length_score = 8
        tips.append("Your resume is too short. Add more details about your experience and skills.")
    else:
        length_score = 0
        tips.append("Your resume is very short. Aim for at least 300 words.")

    score += length_score
    breakdown["Resume Length"] = length_score

    # ─────────────────────────────────────────
    # CHECK 5 — Action Verbs (10 points)
    # ─────────────────────────────────────────
    action_verbs = [
        "developed", "designed", "built", "created", "managed",
        "led", "implemented", "improved", "achieved", "delivered",
        "launched", "automated", "analyzed", "collaborated", "optimized"
    ]
    found_verbs = [v for v in action_verbs if v in resume_text]
    verb_score = min(len(found_verbs) * 2, 10)
    score += verb_score
    breakdown["Action Verbs"] = verb_score
    if verb_score < 5:
        tips.append("Use more action verbs like 'developed', 'designed', 'built' in your resume.")

    # ─────────────────────────────────────────
    # Final Result
    # ─────────────────────────────────────────
    return {
        "ats_score":        score,
        "breakdown":        breakdown,
        "tips":             tips,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "grade":            get_grade(score)
    }


def get_grade(score):
    if score >= 80:
        return {"label": "Excellent", "color": "success"}
    elif score >= 60:
        return {"label": "Good",      "color": "primary"}
    elif score >= 40:
        return {"label": "Average",   "color": "warning"}
    else:
        return {"label": "Needs Work","color": "danger"}