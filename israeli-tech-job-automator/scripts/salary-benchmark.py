#!/usr/bin/env python3
"""
Israeli Tech Salary Benchmark
Quick salary range lookup by role and experience level for the Israeli
tech market.

Usage:
    python salary-benchmark.py --role "full-stack" --experience 5
    python salary-benchmark.py --role "devops" --experience 3 --format json
    python salary-benchmark.py --list-roles
    python salary-benchmark.py --role "backend" --experience 7 --benefits
"""

import argparse
import json
import sys
from typing import Any


# ---------------------------------------------------------------------------
# Israeli tech salary data (2026, gross monthly NIS)
# ---------------------------------------------------------------------------
SALARY_DATA: dict[str, dict[str, Any]] = {
    "full-stack": {
        "title_en": "Full Stack Developer",
        "title_he": "מפתח/ת Full Stack",
        "ranges": {
            "junior": {"min": 18000, "max": 25000, "years": "0-2"},
            "mid": {"min": 25000, "max": 35000, "years": "2-5"},
            "senior": {"min": 35000, "max": 50000, "years": "5-8"},
            "lead": {"min": 50000, "max": 70000, "years": "8+"},
        },
    },
    "backend": {
        "title_en": "Backend Developer",
        "title_he": "מפתח/ת Backend",
        "ranges": {
            "junior": {"min": 18000, "max": 25000, "years": "0-2"},
            "mid": {"min": 25000, "max": 38000, "years": "2-5"},
            "senior": {"min": 38000, "max": 55000, "years": "5-8"},
            "lead": {"min": 55000, "max": 75000, "years": "8+"},
        },
    },
    "frontend": {
        "title_en": "Frontend Developer",
        "title_he": "מפתח/ת Frontend",
        "ranges": {
            "junior": {"min": 17000, "max": 24000, "years": "0-2"},
            "mid": {"min": 24000, "max": 34000, "years": "2-5"},
            "senior": {"min": 34000, "max": 48000, "years": "5-8"},
            "lead": {"min": 48000, "max": 65000, "years": "8+"},
        },
    },
    "mobile": {
        "title_en": "Mobile Developer",
        "title_he": "מפתח/ת מובייל",
        "ranges": {
            "junior": {"min": 18000, "max": 26000, "years": "0-2"},
            "mid": {"min": 26000, "max": 38000, "years": "2-5"},
            "senior": {"min": 38000, "max": 55000, "years": "5-8"},
            "lead": {"min": 55000, "max": 70000, "years": "8+"},
        },
    },
    "embedded": {
        "title_en": "Embedded Developer",
        "title_he": "מפתח/ת Embedded",
        "ranges": {
            "junior": {"min": 20000, "max": 28000, "years": "0-2"},
            "mid": {"min": 28000, "max": 40000, "years": "2-5"},
            "senior": {"min": 40000, "max": 55000, "years": "5-8"},
            "lead": {"min": 55000, "max": 75000, "years": "8+"},
        },
    },
    "devops": {
        "title_en": "DevOps Engineer",
        "title_he": "מהנדס/ת DevOps",
        "ranges": {
            "junior": {"min": 20000, "max": 28000, "years": "0-2"},
            "mid": {"min": 28000, "max": 42000, "years": "2-5"},
            "senior": {"min": 42000, "max": 60000, "years": "5-8"},
            "lead": {"min": 60000, "max": 80000, "years": "8+"},
        },
    },
    "sre": {
        "title_en": "Site Reliability Engineer",
        "title_he": "מהנדס/ת SRE",
        "ranges": {
            "junior": {"min": 22000, "max": 30000, "years": "0-2"},
            "mid": {"min": 30000, "max": 45000, "years": "2-5"},
            "senior": {"min": 45000, "max": 65000, "years": "5-8"},
            "lead": {"min": 65000, "max": 85000, "years": "8+"},
        },
    },
    "cloud": {
        "title_en": "Cloud Engineer",
        "title_he": "מהנדס/ת ענן",
        "ranges": {
            "junior": {"min": 20000, "max": 28000, "years": "0-2"},
            "mid": {"min": 28000, "max": 42000, "years": "2-5"},
            "senior": {"min": 42000, "max": 58000, "years": "5-8"},
            "lead": {"min": 58000, "max": 75000, "years": "8+"},
        },
    },
    "data-engineer": {
        "title_en": "Data Engineer",
        "title_he": "מהנדס/ת דאטה",
        "ranges": {
            "junior": {"min": 20000, "max": 28000, "years": "0-2"},
            "mid": {"min": 28000, "max": 42000, "years": "2-5"},
            "senior": {"min": 42000, "max": 60000, "years": "5-8"},
            "lead": {"min": 60000, "max": 80000, "years": "8+"},
        },
    },
    "data-scientist": {
        "title_en": "Data Scientist",
        "title_he": "מדען/ית נתונים",
        "ranges": {
            "junior": {"min": 22000, "max": 30000, "years": "0-2"},
            "mid": {"min": 30000, "max": 45000, "years": "2-5"},
            "senior": {"min": 45000, "max": 65000, "years": "5-8"},
            "lead": {"min": 65000, "max": 85000, "years": "8+"},
        },
    },
    "ml-engineer": {
        "title_en": "ML Engineer",
        "title_he": "מהנדס/ת ML",
        "ranges": {
            "junior": {"min": 22000, "max": 32000, "years": "0-2"},
            "mid": {"min": 32000, "max": 48000, "years": "2-5"},
            "senior": {"min": 48000, "max": 70000, "years": "5-8"},
            "lead": {"min": 70000, "max": 90000, "years": "8+"},
        },
    },
    "ai-engineer": {
        "title_en": "AI/LLM Engineer",
        "title_he": "מהנדס/ת AI/LLM",
        "ranges": {
            "junior": {"min": 25000, "max": 35000, "years": "0-2"},
            "mid": {"min": 35000, "max": 55000, "years": "2-5"},
            "senior": {"min": 55000, "max": 80000, "years": "5-8"},
            "lead": {"min": 80000, "max": 100000, "years": "8+"},
        },
    },
    "security-engineer": {
        "title_en": "Security Engineer",
        "title_he": "מהנדס/ת אבטחה",
        "ranges": {
            "junior": {"min": 20000, "max": 28000, "years": "0-2"},
            "mid": {"min": 28000, "max": 42000, "years": "2-5"},
            "senior": {"min": 42000, "max": 60000, "years": "5-8"},
            "lead": {"min": 60000, "max": 80000, "years": "8+"},
        },
    },
    "security-researcher": {
        "title_en": "Security Researcher",
        "title_he": "חוקר/ת אבטחה",
        "ranges": {
            "junior": {"min": 22000, "max": 32000, "years": "0-2"},
            "mid": {"min": 32000, "max": 48000, "years": "2-5"},
            "senior": {"min": 48000, "max": 68000, "years": "5-8"},
            "lead": {"min": 68000, "max": 90000, "years": "8+"},
        },
    },
    "team-lead": {
        "title_en": "Team Lead",
        "title_he": "ראש/ת צוות",
        "ranges": {
            "junior": {"min": 40000, "max": 55000, "years": "0-2 mgmt"},
            "mid": {"min": 55000, "max": 70000, "years": "2-5 mgmt"},
            "senior": {"min": 70000, "max": 85000, "years": "5+ mgmt"},
        },
    },
    "engineering-manager": {
        "title_en": "Engineering Manager",
        "title_he": "מנהל/ת פיתוח",
        "ranges": {
            "junior": {"min": 50000, "max": 65000, "years": "0-2 mgmt"},
            "mid": {"min": 65000, "max": 80000, "years": "2-5 mgmt"},
            "senior": {"min": 80000, "max": 100000, "years": "5+ mgmt"},
        },
    },
    "vp-engineering": {
        "title_en": "VP Engineering",
        "title_he": "סמנכ\"ל/ית פיתוח",
        "ranges": {
            "mid": {"min": 70000, "max": 90000, "years": "2-5 mgmt"},
            "senior": {"min": 90000, "max": 130000, "years": "5+ mgmt"},
        },
    },
    "cto": {
        "title_en": "CTO (Startup)",
        "title_he": "CTO (סטארטאפ)",
        "ranges": {
            "mid": {"min": 60000, "max": 85000, "years": "2-5 mgmt"},
            "senior": {"min": 80000, "max": 120000, "years": "5+ mgmt"},
        },
    },
    "qa": {
        "title_en": "QA Engineer",
        "title_he": "מהנדס/ת QA",
        "ranges": {
            "junior": {"min": 15000, "max": 22000, "years": "0-2"},
            "mid": {"min": 22000, "max": 32000, "years": "2-5"},
            "senior": {"min": 32000, "max": 45000, "years": "5-8"},
            "lead": {"min": 45000, "max": 60000, "years": "8+"},
        },
    },
    "qa-automation": {
        "title_en": "QA Automation Engineer",
        "title_he": "מהנדס/ת אוטומציה",
        "ranges": {
            "junior": {"min": 17000, "max": 25000, "years": "0-2"},
            "mid": {"min": 25000, "max": 36000, "years": "2-5"},
            "senior": {"min": 36000, "max": 50000, "years": "5-8"},
            "lead": {"min": 50000, "max": 65000, "years": "8+"},
        },
    },
    "product-manager": {
        "title_en": "Product Manager",
        "title_he": "מנהל/ת מוצר",
        "ranges": {
            "junior": {"min": 20000, "max": 30000, "years": "0-2"},
            "mid": {"min": 30000, "max": 45000, "years": "2-5"},
            "senior": {"min": 45000, "max": 65000, "years": "5-8"},
            "lead": {"min": 65000, "max": 85000, "years": "8+"},
        },
    },
}

# ---------------------------------------------------------------------------
# Benefits calculation
# ---------------------------------------------------------------------------
BENEFITS = {
    "pension_employer": 0.065,       # 6.5% employer contribution
    "pension_employee": 0.06,        # 6% employee contribution
    "severance": 0.0833,             # 8.33% severance (Section 14)
    "keren_hishtalmut_employer": 0.075,  # 7.5% employer
    "keren_hishtalmut_employee": 0.025,  # 2.5% employee
    "convalescence_days": 9,         # Average days per year
    "convalescence_rate": 418,       # NIS per day (2026 estimate)
}


def get_experience_level(years: float) -> str:
    """Map years of experience to level."""
    if years < 2:
        return "junior"
    elif years < 5:
        return "mid"
    elif years < 8:
        return "senior"
    else:
        return "lead"


def calculate_benefits_value(monthly_salary: int) -> dict[str, Any]:
    """Calculate the monetary value of standard Israeli tech benefits."""
    annual_salary = monthly_salary * 12

    pension_employer = annual_salary * BENEFITS["pension_employer"]
    severance = annual_salary * BENEFITS["severance"]
    keren_employer = annual_salary * BENEFITS["keren_hishtalmut_employer"]
    convalescence = BENEFITS["convalescence_days"] * BENEFITS["convalescence_rate"]

    total_employer_cost = (
        annual_salary + pension_employer + severance +
        keren_employer + convalescence
    )

    return {
        "monthly_gross": monthly_salary,
        "annual_gross": annual_salary,
        "pension_employer_annual": round(pension_employer),
        "severance_annual": round(severance),
        "keren_hishtalmut_employer_annual": round(keren_employer),
        "convalescence_annual": round(convalescence),
        "total_employer_cost_annual": round(total_employer_cost),
        "total_employer_cost_monthly": round(total_employer_cost / 12),
        "benefits_value_percent": round(
            (total_employer_cost - annual_salary) / annual_salary * 100, 1
        ),
    }


def format_salary(amount: int) -> str:
    """Format salary with thousand separators."""
    return f"{amount:,}"


def lookup_salary(
    role: str, experience: float, fmt: str = "text",
    show_benefits: bool = False,
) -> str:
    """Look up salary range for a given role and experience level."""
    role_key = role.lower().strip()

    # Try direct match
    if role_key not in SALARY_DATA:
        # Try partial match
        matches = [
            k for k in SALARY_DATA
            if role_key in k or k in role_key
        ]
        if len(matches) == 1:
            role_key = matches[0]
        elif len(matches) > 1:
            if fmt == "json":
                return json.dumps({
                    "error": f"Ambiguous role '{role}'. Did you mean: {', '.join(matches)}?"
                })
            return (
                f"Ambiguous role '{role}'. Did you mean one of: "
                f"{', '.join(matches)}?"
            )
        else:
            if fmt == "json":
                return json.dumps({
                    "error": f"Role '{role}' not found.",
                    "available_roles": list(SALARY_DATA.keys()),
                })
            return (
                f"Role '{role}' not found.\n\n"
                f"Available roles:\n"
                + "\n".join(f"  - {k}" for k in sorted(SALARY_DATA.keys()))
            )

    data = SALARY_DATA[role_key]
    level = get_experience_level(experience)

    # Handle management roles that may not have junior/lead levels
    if level not in data["ranges"]:
        available_levels = list(data["ranges"].keys())
        level = available_levels[-1]  # Use highest available

    range_data = data["ranges"][level]
    midpoint = (range_data["min"] + range_data["max"]) // 2

    if fmt == "json":
        result: dict[str, Any] = {
            "role": role_key,
            "title_en": data["title_en"],
            "title_he": data["title_he"],
            "experience_years": experience,
            "level": level,
            "salary_range": {
                "min": range_data["min"],
                "max": range_data["max"],
                "midpoint": midpoint,
                "currency": "NIS",
                "period": "monthly_gross",
            },
            "all_levels": {
                lvl: {
                    "min": r["min"],
                    "max": r["max"],
                    "years": r["years"],
                }
                for lvl, r in data["ranges"].items()
            },
        }
        if show_benefits:
            result["benefits_at_midpoint"] = calculate_benefits_value(midpoint)
        return json.dumps(result, indent=2, ensure_ascii=False)

    # Plain text
    lines: list[str] = []
    lines.append("=" * 55)
    lines.append(f"  {data['title_en']} ({data['title_he']})")
    lines.append(f"  Experience: {experience} years (Level: {level})")
    lines.append("=" * 55)
    lines.append("")
    lines.append(f"  Salary Range: {format_salary(range_data['min'])} - "
                 f"{format_salary(range_data['max'])} NIS/month (gross)")
    lines.append(f"  Midpoint:     {format_salary(midpoint)} NIS/month")
    lines.append(f"  Annual Range: {format_salary(range_data['min'] * 12)} - "
                 f"{format_salary(range_data['max'] * 12)} NIS/year")
    lines.append("")

    # Show all levels for context
    lines.append("  All Levels:")
    for lvl, r in data["ranges"].items():
        marker = " <-- you" if lvl == level else ""
        lines.append(
            f"    {lvl.capitalize():10s} ({r['years']:>10s}): "
            f"{format_salary(r['min']):>7s} - {format_salary(r['max']):>7s}"
            f"{marker}"
        )
    lines.append("")

    if show_benefits:
        benefits = calculate_benefits_value(midpoint)
        lines.append("  Benefits Value (at midpoint salary):")
        lines.append(f"    Pension (employer 6.5%):       {format_salary(benefits['pension_employer_annual']):>8s} NIS/year")
        lines.append(f"    Severance (8.33%):             {format_salary(benefits['severance_annual']):>8s} NIS/year")
        lines.append(f"    Keren Hishtalmut (7.5%):       {format_salary(benefits['keren_hishtalmut_employer_annual']):>8s} NIS/year")
        lines.append(f"    Convalescence pay:             {format_salary(benefits['convalescence_annual']):>8s} NIS/year")
        lines.append(f"    Total employer cost:            {format_salary(benefits['total_employer_cost_monthly']):>8s} NIS/month")
        lines.append(f"    Benefits add ~{benefits['benefits_value_percent']}% to base salary")
        lines.append("")

    lines.append("  Note: Ranges are based on public survey data (Ethosia,")
    lines.append("  Hever Group) and may vary by company size, location,")
    lines.append("  and industry segment.")
    lines.append("=" * 55)

    return "\n".join(lines)


def list_roles(fmt: str = "text") -> str:
    """List all available roles."""
    if fmt == "json":
        roles = {
            k: {"title_en": v["title_en"], "title_he": v["title_he"]}
            for k, v in SALARY_DATA.items()
        }
        return json.dumps(roles, indent=2, ensure_ascii=False)

    lines = ["Available roles:", ""]
    for key, data in sorted(SALARY_DATA.items()):
        lines.append(f"  {key:25s} {data['title_en']} ({data['title_he']})")
    lines.append("")
    lines.append(f"  Total: {len(SALARY_DATA)} roles")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Israeli Tech Salary Benchmark"
    )
    parser.add_argument(
        "--role",
        help="Role to look up (e.g., 'full-stack', 'devops', 'backend')",
    )
    parser.add_argument(
        "--experience",
        type=float,
        default=3,
        help="Years of experience (default: 3)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--list-roles",
        action="store_true",
        help="List all available roles",
    )
    parser.add_argument(
        "--benefits",
        action="store_true",
        help="Show benefits value calculation",
    )
    args = parser.parse_args()

    if args.list_roles:
        print(list_roles(args.format))
        return

    if not args.role:
        print("Error: --role is required (or use --list-roles).", file=sys.stderr)
        sys.exit(1)

    result = lookup_salary(
        args.role, args.experience, args.format, args.benefits
    )
    print(result)


if __name__ == "__main__":
    main()
