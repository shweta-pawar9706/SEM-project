import json
import os

def match_job_roles(data):
    resume_skills = [s.lower() for s in data.get("resume_skills", [])]

    if not resume_skills:
        return {"error": "No skills found in resume"}

    # Load job roles from JSON
    json_path = os.path.join(os.path.dirname(__file__), "data", "job_roles.json")
    with open(json_path, "r") as f:
        job_roles = json.load(f)

    results = []

    for role_name, role_data in job_roles.items():
        required_skills = [s.lower() for s in role_data["skills"]]

        # Calculate matched and missing skills
        matched  = [s for s in required_skills if s in resume_skills]
        missing  = [s for s in required_skills if s not in resume_skills]
        total    = len(required_skills)
        match_pct = round((len(matched) / max(total, 1)) * 100)

        results.append({
            "role":           role_name,
            "icon":           role_data["icon"],
            "color":          role_data["color"],
            "description":    role_data["description"],
            "match_percent":  match_pct,
            "matched_skills": matched,
            "missing_skills": missing,
            "total_skills":   total
        })

    # Sort by match percentage
    results.sort(key=lambda x: x["match_percent"], reverse=True)

    # Top 5 matches
    top_matches = results[:5]

    return {
        "top_matches":  top_matches,
        "all_matches":  results,
        "best_role":    results[0]["role"] if results else "None",
        "best_percent": results[0]["match_percent"] if results else 0
    }