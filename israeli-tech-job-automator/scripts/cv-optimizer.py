#!/usr/bin/env python3
"""
Israeli Tech CV Optimizer
Analyzes CV text and suggests improvements for the Israeli tech market.

Usage:
    python cv-optimizer.py --cv /path/to/cv.txt --role "Senior Backend Developer"
    python cv-optimizer.py --cv /path/to/cv.txt --role "Full Stack" --format json
    python cv-optimizer.py --cv /path/to/cv.txt --language he
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Israeli tech keywords by category
# ---------------------------------------------------------------------------
TECH_KEYWORDS = {
    "languages": [
        "Python", "JavaScript", "TypeScript", "Java", "Go", "Golang", "C#",
        "C++", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala",
    ],
    "frontend": [
        "React", "Next.js", "Vue.js", "Angular", "Svelte", "HTML5", "CSS3",
        "Tailwind CSS", "SASS", "LESS", "Webpack", "Vite", "Redux",
        "MobX", "Zustand",
    ],
    "backend": [
        "Node.js", "Express", "NestJS", "Django", "FastAPI", "Flask",
        "Spring Boot", "ASP.NET", "Gin", "Fiber", "Rails",
    ],
    "mobile": [
        "React Native", "Flutter", "iOS", "Android", "SwiftUI",
        "Jetpack Compose", "Xamarin",
    ],
    "databases": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
        "DynamoDB", "Cassandra", "SQLite", "Supabase", "Firebase",
    ],
    "cloud": [
        "AWS", "GCP", "Azure", "Docker", "Kubernetes", "K8s",
        "Terraform", "CloudFormation", "Pulumi", "Serverless",
    ],
    "devops": [
        "CI/CD", "Jenkins", "GitHub Actions", "GitLab CI", "ArgoCD",
        "Prometheus", "Grafana", "Datadog", "ELK", "Ansible",
    ],
    "data": [
        "Kafka", "RabbitMQ", "Spark", "Airflow", "dbt", "Snowflake",
        "BigQuery", "Redshift", "ETL", "Data Pipeline",
    ],
    "ai_ml": [
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
        "TensorFlow", "PyTorch", "LLM", "GPT", "Transformers",
        "MLOps", "Hugging Face", "LangChain",
    ],
    "security": [
        "OWASP", "Penetration Testing", "SOC2", "ISO 27001",
        "Encryption", "IAM", "Zero Trust", "SAST", "DAST",
    ],
}

# Israeli-specific keywords that strengthen a CV
ISRAELI_KEYWORDS = [
    "8200", "Unit 8200", "Mamram", "C4I", "IDF",
    "startup", "scale-up", "exit", "Series A", "Series B",
    "Hebrew", "bilingual", "RTL",
    "Tel Aviv", "Herzliya", "Ra'anana", "Haifa", "Be'er Sheva",
]

# ---------------------------------------------------------------------------
# CV section patterns
# ---------------------------------------------------------------------------
SECTION_PATTERNS = {
    "contact": re.compile(
        r"(?i)(contact|email|phone|linkedin|github|portfolio|"
        r"פרטי קשר|אימייל|טלפון)",
        re.UNICODE,
    ),
    "summary": re.compile(
        r"(?i)(summary|objective|about|profile|introduction|"
        r"תקציר|אודות|פרופיל מקצועי)",
        re.UNICODE,
    ),
    "experience": re.compile(
        r"(?i)(experience|employment|work history|"
        r"ניסיון תעסוקתי|ניסיון מקצועי|ניסיון)",
        re.UNICODE,
    ),
    "education": re.compile(
        r"(?i)(education|academic|degree|university|"
        r"השכלה|תואר|אקדמי)",
        re.UNICODE,
    ),
    "skills": re.compile(
        r"(?i)(skills|technologies|technical|tools|"
        r"כישורים|טכנולוגיות|כלים)",
        re.UNICODE,
    ),
    "military": re.compile(
        r"(?i)(military|army|idf|service|"
        r"שירות צבאי|צבא|צה\"ל)",
        re.UNICODE,
    ),
    "languages": re.compile(
        r"(?i)(languages|שפות)",
        re.UNICODE,
    ),
    "certifications": re.compile(
        r"(?i)(certifications?|courses?|licenses?|"
        r"הסמכות|קורסים|רישיונות)",
        re.UNICODE,
    ),
}

# ---------------------------------------------------------------------------
# Anti-patterns (things to flag)
# ---------------------------------------------------------------------------
ANTI_PATTERNS = {
    "photo_reference": re.compile(
        r"(?i)(photo|picture|headshot|תמונה)", re.UNICODE
    ),
    "marital_status": re.compile(
        r"(?i)(married|single|divorced|marital|spouse|children|"
        r"נשוי|רווק|גרוש|מצב משפחתי|ילדים)", re.UNICODE
    ),
    "date_of_birth": re.compile(
        r"(?i)(date of birth|born|age|dob|תאריך לידה|גיל)", re.UNICODE
    ),
    "em_dash": re.compile(r"\u2014"),
    "very_long_paragraph": re.compile(r"[^\n]{500,}"),
    "generic_objective": re.compile(
        r"(?i)(seeking a challenging|looking for an opportunity|"
        r"passionate about|results.driven professional)",
    ),
}


def read_cv(filepath: str) -> str:
    """Read CV text from file. Supports .txt and basic .pdf (text layer)."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)

    if path.suffix.lower() == ".pdf":
        try:
            # Try to extract text from PDF
            import subprocess
            result = subprocess.run(
                ["pdftotext", "-layout", str(path), "-"],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                return result.stdout
            else:
                print(
                    "Warning: pdftotext not available. "
                    "Install poppler-utils or provide a .txt file.",
                    file=sys.stderr,
                )
                sys.exit(1)
        except FileNotFoundError:
            print(
                "Warning: pdftotext not found. "
                "Install poppler-utils or provide a .txt file.",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        return path.read_text(encoding="utf-8", errors="ignore")


def detect_language(text: str) -> str:
    """Detect if CV is primarily Hebrew or English."""
    hebrew_chars = len(re.findall(r"[\u0590-\u05FF]", text))
    latin_chars = len(re.findall(r"[a-zA-Z]", text))
    return "he" if hebrew_chars > latin_chars * 0.3 else "en"


def detect_sections(text: str) -> dict[str, bool]:
    """Detect which standard sections are present in the CV."""
    found = {}
    for section, pattern in SECTION_PATTERNS.items():
        found[section] = bool(pattern.search(text))
    return found


def find_tech_keywords(text: str) -> dict[str, list[str]]:
    """Find technology keywords present in the CV."""
    found: dict[str, list[str]] = {}
    text_upper = text.upper()
    for category, keywords in TECH_KEYWORDS.items():
        matches = [kw for kw in keywords if kw.upper() in text_upper]
        if matches:
            found[category] = matches
    return found


def find_israeli_keywords(text: str) -> list[str]:
    """Find Israeli-specific keywords in the CV."""
    text_upper = text.upper()
    return [kw for kw in ISRAELI_KEYWORDS if kw.upper() in text_upper]


def check_anti_patterns(text: str) -> list[dict[str, str]]:
    """Check for anti-patterns that should be fixed."""
    issues: list[dict[str, str]] = []

    if ANTI_PATTERNS["marital_status"].search(text):
        issues.append({
            "severity": "HIGH",
            "issue": "Marital status detected",
            "recommendation": (
                "Remove marital status, number of children, and similar "
                "personal details. Israeli anti-discrimination law (2014) "
                "makes this unnecessary and potentially harmful."
            ),
        })

    if ANTI_PATTERNS["date_of_birth"].search(text):
        issues.append({
            "severity": "HIGH",
            "issue": "Date of birth or age detected",
            "recommendation": (
                "Remove date of birth and age. This information can lead "
                "to age discrimination and is not expected on Israeli tech CVs."
            ),
        })

    if ANTI_PATTERNS["em_dash"].search(text):
        issues.append({
            "severity": "LOW",
            "issue": "Em dashes detected",
            "recommendation": (
                "Replace em dashes with standard punctuation (commas, "
                "periods, parentheses). Some ATS systems may not "
                "handle em dashes correctly."
            ),
        })

    if ANTI_PATTERNS["very_long_paragraph"].search(text):
        issues.append({
            "severity": "MEDIUM",
            "issue": "Very long paragraphs detected",
            "recommendation": (
                "Break long paragraphs into bullet points. ATS systems "
                "and recruiters prefer concise, scannable content."
            ),
        })

    if ANTI_PATTERNS["generic_objective"].search(text):
        issues.append({
            "severity": "MEDIUM",
            "issue": "Generic objective statement detected",
            "recommendation": (
                "Replace generic phrases like 'seeking a challenging "
                "position' with a specific professional summary that "
                "highlights your unique value and target role."
            ),
        })

    # Check CV length (approximate by lines)
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) > 80:
        issues.append({
            "severity": "MEDIUM",
            "issue": "CV appears too long",
            "recommendation": (
                "Israeli tech CVs should be 1-2 pages. Consider "
                "trimming older experience and focusing on the most "
                "recent 5-7 years of relevant work."
            ),
        })
    elif len(lines) < 15:
        issues.append({
            "severity": "MEDIUM",
            "issue": "CV appears too short",
            "recommendation": (
                "The CV seems very brief. Ensure you have included "
                "enough detail about your experience, skills, and "
                "accomplishments."
            ),
        })

    return issues


def check_contact_info(text: str) -> list[dict[str, str]]:
    """Check for proper contact information."""
    issues: list[dict[str, str]] = []

    # Check for email
    if not re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text):
        issues.append({
            "severity": "HIGH",
            "issue": "No email address detected",
            "recommendation": "Add a professional email address to your CV.",
        })

    # Check for phone
    if not re.search(r"(\+972|05\d|07\d)\d{7,8}", text.replace("-", "").replace(" ", "")):
        issues.append({
            "severity": "MEDIUM",
            "issue": "No Israeli phone number detected",
            "recommendation": (
                "Add your phone number in +972 format or local format "
                "(05X-XXXXXXX). Israeli recruiters prefer to call."
            ),
        })

    # Check for LinkedIn
    if not re.search(r"(?i)linkedin\.com/in/", text):
        issues.append({
            "severity": "MEDIUM",
            "issue": "No LinkedIn profile link detected",
            "recommendation": (
                "Add your LinkedIn profile URL. LinkedIn is essential "
                "for Israeli tech job search."
            ),
        })

    # Check for GitHub (for developers)
    if not re.search(r"(?i)github\.com/", text):
        issues.append({
            "severity": "LOW",
            "issue": "No GitHub profile link detected",
            "recommendation": (
                "Consider adding your GitHub profile URL if you have "
                "public repositories or contributions."
            ),
        })

    return issues


def generate_suggestions(
    text: str,
    role: str,
    sections: dict[str, bool],
    tech_found: dict[str, list[str]],
    israeli_found: list[str],
) -> list[dict[str, str]]:
    """Generate improvement suggestions based on analysis."""
    suggestions: list[dict[str, str]] = []

    # Missing sections
    recommended_sections = [
        "contact", "summary", "experience", "skills", "education",
    ]
    for section in recommended_sections:
        if not sections.get(section, False):
            section_name = section.replace("_", " ").title()
            suggestions.append({
                "category": "structure",
                "suggestion": f"Add a '{section_name}' section to your CV.",
            })

    # Missing languages section
    if not sections.get("languages", False):
        suggestions.append({
            "category": "structure",
            "suggestion": (
                "Add a 'Languages' section listing Hebrew (native), "
                "English (fluent/professional), and any other languages."
            ),
        })

    # Role-specific keyword suggestions
    role_lower = role.lower()
    if "backend" in role_lower or "back-end" in role_lower:
        if "backend" not in tech_found:
            suggestions.append({
                "category": "keywords",
                "suggestion": (
                    "For a Backend role, ensure your CV mentions "
                    "backend frameworks (Node.js, Express, NestJS, "
                    "Django, FastAPI, Spring Boot, etc.)."
                ),
            })
    elif "frontend" in role_lower or "front-end" in role_lower:
        if "frontend" not in tech_found:
            suggestions.append({
                "category": "keywords",
                "suggestion": (
                    "For a Frontend role, ensure your CV mentions "
                    "frontend frameworks (React, Next.js, Vue.js, "
                    "Angular, etc.)."
                ),
            })
    elif "full" in role_lower and "stack" in role_lower:
        if "frontend" not in tech_found or "backend" not in tech_found:
            suggestions.append({
                "category": "keywords",
                "suggestion": (
                    "For a Full Stack role, ensure your CV covers both "
                    "frontend (React, Vue.js) and backend (Node.js, "
                    "Python) technologies."
                ),
            })
    elif "devops" in role_lower or "sre" in role_lower:
        if "cloud" not in tech_found or "devops" not in tech_found:
            suggestions.append({
                "category": "keywords",
                "suggestion": (
                    "For a DevOps/SRE role, ensure your CV mentions "
                    "cloud platforms (AWS, GCP, Azure), containerization "
                    "(Docker, Kubernetes), and CI/CD tools."
                ),
            })
    elif "data" in role_lower:
        if "data" not in tech_found and "databases" not in tech_found:
            suggestions.append({
                "category": "keywords",
                "suggestion": (
                    "For a Data role, ensure your CV mentions data "
                    "tools (Spark, Kafka, Airflow, dbt) and databases "
                    "(PostgreSQL, BigQuery, Snowflake)."
                ),
            })

    # Israeli-specific suggestions
    if not israeli_found:
        suggestions.append({
            "category": "israeli_market",
            "suggestion": (
                "Consider adding Israeli market-relevant keywords: "
                "startup experience, military tech background (if "
                "applicable), bilingual (Hebrew/English), etc."
            ),
        })

    # Check for quantifiable achievements
    if not re.search(r"\d+%|\d+x|\$\d+|improved|reduced|increased", text, re.IGNORECASE):
        suggestions.append({
            "category": "impact",
            "suggestion": (
                "Add quantifiable achievements. Instead of 'improved "
                "performance', say 'improved API response time by 40%' "
                "or 'reduced deployment time from 2 hours to 15 minutes'."
            ),
        })

    return suggestions


def analyze_cv(
    filepath: str, role: str, fmt: str = "text"
) -> str:
    """Run full CV analysis and return report."""
    text = read_cv(filepath)
    language = detect_language(text)
    sections = detect_sections(text)
    tech_found = find_tech_keywords(text)
    israeli_found = find_israeli_keywords(text)
    anti_pattern_issues = check_anti_patterns(text)
    contact_issues = check_contact_info(text)
    suggestions = generate_suggestions(
        text, role, sections, tech_found, israeli_found
    )

    all_issues = anti_pattern_issues + contact_issues

    if fmt == "json":
        result = {
            "language_detected": language,
            "target_role": role,
            "sections_found": sections,
            "tech_keywords": tech_found,
            "israeli_keywords": israeli_found,
            "issues": all_issues,
            "suggestions": suggestions,
            "score": calculate_score(
                sections, tech_found, israeli_found,
                all_issues, suggestions
            ),
        }
        return json.dumps(result, indent=2, ensure_ascii=False)

    # Plain text report
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("  Israeli Tech CV Optimizer Report")
    lines.append(f"  Target Role: {role}")
    lines.append(f"  Language Detected: {'Hebrew' if language == 'he' else 'English'}")
    lines.append("=" * 60)
    lines.append("")

    # Score
    score = calculate_score(
        sections, tech_found, israeli_found, all_issues, suggestions
    )
    lines.append(f"  Overall Score: {score}/100")
    lines.append("")

    # Sections
    lines.append("--- Sections Found ---")
    for section, found in sections.items():
        status = "OK" if found else "MISSING"
        icon = "+" if found else "-"
        lines.append(f"  [{icon}] {section.replace('_', ' ').title()}: {status}")
    lines.append("")

    # Tech keywords
    lines.append("--- Technology Keywords Found ---")
    if tech_found:
        for category, keywords in tech_found.items():
            lines.append(f"  {category.replace('_', ' ').title()}: {', '.join(keywords)}")
    else:
        lines.append("  No technology keywords detected. Add specific technology names.")
    lines.append("")

    # Israeli keywords
    lines.append("--- Israeli Market Keywords ---")
    if israeli_found:
        lines.append(f"  Found: {', '.join(israeli_found)}")
    else:
        lines.append("  No Israeli-specific keywords found.")
    lines.append("")

    # Issues
    if all_issues:
        lines.append("--- Issues to Fix ---")
        for issue in all_issues:
            lines.append(f"  [{issue['severity']}] {issue['issue']}")
            lines.append(f"    {issue['recommendation']}")
            lines.append("")

    # Suggestions
    if suggestions:
        lines.append("--- Improvement Suggestions ---")
        for suggestion in suggestions:
            lines.append(f"  [{suggestion['category']}] {suggestion['suggestion']}")
            lines.append("")

    lines.append("=" * 60)
    lines.append("  Review complete. Address issues by severity (HIGH first).")
    lines.append("=" * 60)

    return "\n".join(lines)


def calculate_score(
    sections: dict[str, bool],
    tech_found: dict[str, list[str]],
    israeli_found: list[str],
    issues: list[dict[str, str]],
    suggestions: list[dict[str, str]],
) -> int:
    """Calculate an overall CV quality score (0-100)."""
    score = 50  # Base score

    # Sections (up to +20)
    recommended = ["contact", "summary", "experience", "skills", "education"]
    section_score = sum(3 for s in recommended if sections.get(s, False))
    if sections.get("languages", False):
        section_score += 3
    if sections.get("military", False):
        section_score += 2
    score += min(section_score, 20)

    # Tech keywords (up to +15)
    total_keywords = sum(len(kws) for kws in tech_found.values())
    keyword_score = min(total_keywords * 2, 15)
    score += keyword_score

    # Israeli market fit (up to +10)
    israeli_score = min(len(israeli_found) * 3, 10)
    score += israeli_score

    # Issues penalty
    high_issues = sum(1 for i in issues if i["severity"] == "HIGH")
    medium_issues = sum(1 for i in issues if i["severity"] == "MEDIUM")
    score -= high_issues * 8
    score -= medium_issues * 3

    # Suggestions penalty (mild)
    score -= min(len(suggestions) * 2, 10)

    return max(0, min(100, score))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Israeli Tech CV Optimizer"
    )
    parser.add_argument(
        "--cv",
        required=True,
        help="Path to CV file (.txt or .pdf)",
    )
    parser.add_argument(
        "--role",
        default="Software Developer",
        help="Target role (e.g., 'Senior Backend Developer')",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--language",
        choices=["auto", "he", "en"],
        default="auto",
        help="CV language (default: auto-detect)",
    )
    args = parser.parse_args()

    report = analyze_cv(args.cv, args.role, args.format)
    print(report)


if __name__ == "__main__":
    main()
