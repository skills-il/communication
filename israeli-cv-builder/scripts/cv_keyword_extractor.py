#!/usr/bin/env python3
"""CV keyword extractor for Israeli job postings.

Extracts ATS-relevant keywords from a pasted job description so the CV can be
tailored to match. Works in Hebrew and English. Uses simple frequency +
stop-word filtering, no external dependencies.

Usage:
    python cv_keyword_extractor.py < job_description.txt
    python cv_keyword_extractor.py --example
    echo "We're hiring a senior Go engineer..." | python cv_keyword_extractor.py

Output:
    Top 15 keywords ranked by a combined score of frequency and
    tech-relevance. Technology names are boosted.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

EN_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "have",
    "in", "is", "it", "of", "on", "or", "that", "the", "to", "was", "were", "will",
    "with", "you", "your", "our", "we", "they", "this", "these", "their", "i",
    "am", "us", "if", "so", "but", "not", "no", "can", "do", "does", "did", "would",
    "should", "could", "may", "might", "must", "shall", "about", "into", "than",
    "then", "also", "what", "which", "who", "whom", "whose", "when", "where", "why",
    "how", "all", "any", "each", "every", "some", "such", "more", "most", "other",
    "new", "one", "two", "three", "first", "last", "next", "good", "great", "best",
    "job", "jobs", "role", "roles", "position", "positions", "candidate", "team",
    "company", "work", "working", "looking", "seeking", "join", "hiring", "apply",
    "opportunity", "opportunities", "based", "like", "well", "make", "making",
    "get", "use", "using", "build", "building", "develop", "developing", "create",
    "creating", "help", "helping", "ensure", "ensuring", "deliver", "delivering",
    "years", "year", "experience", "knowledge", "understanding", "strong", "solid",
    "proven", "excellent", "deep", "advanced", "senior", "junior", "mid", "level",
    "office", "remote", "hybrid", "full", "time", "part", "israel", "israeli",
    "tel", "aviv", "herzliya",
}

HE_STOPWORDS = {
    "של", "את", "על", "עם", "זה", "זו", "אלה", "אלו", "היא", "הוא", "הם", "הן",
    "אני", "אתה", "את", "אנחנו", "אתם", "אתן", "לא", "כן", "אם", "אז", "גם",
    "רק", "כמו", "יש", "אין", "היה", "היו", "להיות", "לעבוד", "עובד", "עובדים",
    "חברה", "צוות", "תפקיד", "משרה", "ניסיון", "שנים", "שנה", "אנשים", "אדם",
    "כל", "כלל", "בכל", "בתוך", "בין", "לפי", "אחרי", "לפני", "מתוך", "בעיקר",
    "מאוד", "יותר", "פחות", "הכי", "חייב", "צריך", "רצוי", "נדרש", "יכולת",
    "יכולות", "הבנה", "ידע", "כישורים", "תל", "אביב", "הרצליה", "ישראל",
    "אנו", "הכרת", "התפקיד", "ממך", "שלך", "שלנו", "חזק", "רב",
}

TECH_BOOST = {
    "python", "go", "golang", "typescript", "javascript", "rust", "java", "kotlin",
    "swift", "c", "c++", "c#", "ruby", "php", "scala", "elixir", "clojure",
    "react", "vue", "angular", "next.js", "nextjs", "svelte", "nuxt", "remix",
    "node.js", "nodejs", "django", "flask", "fastapi", "nestjs", "express", "rails",
    "spring", "laravel", "postgres", "postgresql", "mysql", "mongodb", "redis",
    "kafka", "rabbitmq", "elasticsearch", "clickhouse", "snowflake", "bigquery",
    "aws", "gcp", "azure", "kubernetes", "k8s", "docker", "terraform", "ansible",
    "jenkins", "circleci", "githubactions", "datadog", "sentry", "prometheus",
    "grafana", "kafka", "spark", "airflow", "dbt", "looker", "tableau",
    "ml", "llm", "rag", "pytorch", "tensorflow", "transformers", "huggingface",
    "openai", "anthropic", "claude", "gpt", "embeddings", "vector",
    "graphql", "rest", "grpc", "protobuf", "microservices", "serverless",
    "linux", "bash", "git", "ci/cd", "cicd", "oauth", "jwt", "saml", "sso",
    "stripe", "tranzila", "pepper", "priority", "monday.com",
}


def tokenize(text: str) -> list[str]:
    """Split text into tokens while preserving dotted tech names (node.js, next.js)."""
    text = text.lower()
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.\-/]*|[\u0590-\u05FF]+", text)
    return [t.strip(".-/") for t in tokens if len(t.strip(".-/")) > 1]


def score_tokens(tokens: list[str]) -> Counter:
    """Score tokens by frequency, with a boost for known tech terms."""
    filtered = [
        t for t in tokens
        if t not in EN_STOPWORDS and t not in HE_STOPWORDS and len(t) > 2
    ]
    counts = Counter(filtered)
    scored = Counter()
    for token, freq in counts.items():
        boost = 3 if token.lower() in TECH_BOOST else 1
        scored[token] = freq * boost
    return scored


def extract_keywords(text: str, top_n: int = 15) -> list[tuple[str, int]]:
    tokens = tokenize(text)
    scored = score_tokens(tokens)
    return scored.most_common(top_n)


EXAMPLE_JD = """We are hiring a Senior Backend Engineer to join our Platform team in Tel Aviv.

You will build and maintain high-throughput payment systems using Go and
PostgreSQL. The role involves designing microservices, owning deployment
pipelines on AWS (ECS, Lambda, RDS), and collaborating with Frontend engineers
using TypeScript and React.

Requirements:
- 5+ years of backend experience, ideally in fintech or payments
- Strong Go or similar (Rust, Java) background
- Experience with Kafka, Redis, and distributed systems
- Comfortable with Terraform and Kubernetes
- Familiarity with Stripe and/or Tranzila integrations is a plus

Nice to have: experience with Datadog, GraphQL, or Israeli payment providers."""


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract ATS keywords from an Israeli job description")
    parser.add_argument("--top", type=int, default=15, help="Number of keywords to return (default 15)")
    parser.add_argument("--example", action="store_true", help="Run on a bundled example job description")
    args = parser.parse_args()

    if args.example:
        text = EXAMPLE_JD
        print("=== EXAMPLE JOB DESCRIPTION ===\n")
        print(text)
        print("\n=== EXTRACTED KEYWORDS ===\n")
    else:
        if sys.stdin.isatty():
            print("Paste the job description and press Ctrl+D when done:", file=sys.stderr)
        text = sys.stdin.read()
        if not text.strip():
            print("Error: no input provided. Use --example for a demo.", file=sys.stderr)
            return 1

    keywords = extract_keywords(text, top_n=args.top)
    if not keywords:
        print("No keywords extracted. Input may be too short.", file=sys.stderr)
        return 1

    max_score = keywords[0][1]
    for rank, (keyword, score) in enumerate(keywords, start=1):
        bar = "#" * max(1, int((score / max_score) * 20))
        print(f"{rank:2}. {keyword:20} {bar} ({score})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
