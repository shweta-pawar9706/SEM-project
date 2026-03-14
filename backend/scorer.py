def score_resume(parsed_data):
    score = 0
    breakdown = {}
    tips = []

    # ── 1. Skills (30 points) ──
    skills = parsed_data.get("skills", [])
    skill_score = min(len(skills) * 3, 30)
    score += skill_score
    breakdown["Skills"] = skill_score
    if skill_score < 15:
        tips.append("Add more technical skills to your resume.")

    # ── 2. Experience (25 points) ──
    experience = parsed_data.get("experience", [])
    if experience and experience[0] != "No experience found":
        exp_score = min(len(experience) * 8, 25)
    else:
        exp_score = 0
        tips.append("Add work experience or internships.")
    score += exp_score
    breakdown["Experience"] = exp_score

    # ── 3. Education (20 points) ──
    education = parsed_data.get("education", [])
    if education and education[0] != "Not found":
        edu_score = min(len(education) * 10, 20)
    else:
        edu_score = 0
        tips.append("Add your educational qualifications.")
    score += edu_score
    breakdown["Education"] = edu_score

    # ── 4. Contact Info (15 points) ──
    contact_score = 0
    if parsed_data.get("email") != "Not found":
        contact_score += 8
    else:
        tips.append("Add your email address.")
    if parsed_data.get("phone") != "Not found":
        contact_score += 7
    else:
        tips.append("Add your phone number.")
    score += contact_score
    breakdown["Contact Info"] = contact_score

    # ── 5. Name Found (10 points) ──
    if parsed_data.get("name") != "Not found":
        score += 10
        breakdown["Name"] = 10
    else:
        breakdown["Name"] = 0
        tips.append("Make sure your name is clearly at the top.")

    # ── Final Result ──
    return {
        "total_score": score,
        "breakdown": breakdown,
        "tips": tips,
        "grade": get_grade(score)
    }


def get_grade(score):
    if score >= 80:
        return {"label": "Excellent", "color": "success"}
    elif score >= 60:
        return {"label": "Good", "color": "primary"}
    elif score >= 40:
        return {"label": "Average", "color": "warning"}
    else:
        return {"label": "Needs Work", "color": "danger"}