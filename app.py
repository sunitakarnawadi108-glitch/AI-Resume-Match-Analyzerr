from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

SKILLS = [
    "python", "java", "c", "c++", "javascript",
    "typescript", "html", "css", "sql", "mysql",
    "mongodb", "flask", "django", "react",
    "node.js", "express.js", "git", "github",
    "rest api", "api", "machine learning",
    "data science", "pandas", "numpy",
    "power bi", "figma", "firebase", "bootstrap"
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files["resume"]
    job_description = request.form["job_description"]

    if not resume.filename.lower().endswith(".pdf"):
        return "Please upload a PDF resume."

    file_path = os.path.join(
        UPLOAD_FOLDER,
        resume.filename
    )

    resume.save(file_path)

    reader = PdfReader(file_path)

    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or ""

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    resume_skills = []
    job_skills = []

    for skill in SKILLS:

        if skill in resume_text:
            resume_skills.append(skill)

        if skill in job_description:
            job_skills.append(skill)

    matched_skills = list(
        set(resume_skills) & set(job_skills)
    )

    missing_skills = list(
        set(job_skills) - set(resume_skills)
    )

    if len(job_skills) > 0:

        match_score = round(
            len(matched_skills)
            / len(job_skills)
            * 100
        )

    else:

        match_score = 0

    if match_score >= 80:

        summary = (
            "Excellent Match! 🎉 "
            "Your resume matches most of the "
            "important skills required for this job."
        )

    elif match_score >= 60:

        summary = (
            "Good Match! 👍 "
            "Your resume has several relevant skills, "
            "but there are some areas you can improve."
        )

    elif match_score >= 40:

        summary = (
            "Moderate Match. 📚 "
            "You have some relevant skills, but "
            "learning the missing skills could improve "
            "your chances."
        )

    else:

        summary = (
            "Needs Improvement. 🚀 "
            "Your resume currently has a low skill match "
            "with this job description."
        )

    suggestions = []

    for skill in missing_skills:

        suggestions.append(
            "Consider learning or improving "
            + skill
            + "."
        )

    return render_template(
        "result.html",
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        match_score=match_score,
        suggestions=suggestions,
        summary=summary
    )


if __name__ == "__main__":
    app.run(debug=True)