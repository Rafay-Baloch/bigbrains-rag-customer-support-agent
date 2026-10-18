import json
import re
import requests
from bs4 import BeautifulSoup

# Clean text utility
def clean_text(raw_html_or_text):
    text = re.sub(r'<[^>]+>', ' ', raw_html_or_text)  # Remove HTML tags
    text = re.sub(r'\s+', ' ', text).strip()         # Remove extra spaces/newlines
    return text

# Target Big Brains dataset sources / endpoints
KNOWLEDGE_SOURCES = [
    {
        "category": "course",
        "title": "Agentic AI & Generative AI Masterclass",
        "url": "https://bigbrains.example.com/courses/agentic-ai",
        "raw_text": "Comprehensive 12-week program covering Autonomous Agents, LLM Fine-tuning, RAG architecture, LangChain, and LangGraph. Prerequisites: Python proficiency. Fee: $250 with flexible installments. Includes capstone industry defense and verified certification."
    },
    {
        "category": "course",
        "title": "Full Stack Web Engineering (Django & React)",
        "url": "https://bigbrains.example.com/courses/fullstack",
        "raw_text": "16-week live bootcamp covering PostgreSQL, Django REST Framework, modern React/Tailwind frontend, Docker, and CI/CD pipelines. Projects included: E-commerce and AI CMS. Schedule: Weekend live labs and weekday assignments."
    },
    {
        "category": "internship",
        "title": "Big Brains Virtual Internship Program",
        "url": "https://bigbrains.example.com/internships",
        "raw_text": "6 to 8-week structured virtual internship for top-performing students. Interns collaborate on client deliverables, participate in code reviews, and receive recommendation letters alongside a performance stipend."
    },
    {
        "category": "service",
        "title": "Corporate AI & Enterprise Transformation",
        "url": "https://bigbrains.example.com/services",
        "raw_text": "Big Brains provides tailored enterprise training, agentic workflow automation, and custom model deployment for enterprises and educational institutions."
    },
    {
        "category": "policy",
        "title": "Refund and Certification Policy",
        "url": "https://bigbrains.example.com/policies",
        "raw_text": "Students can request a 100% refund within the first 7 days of course commencement. Verified digital certificates require at least 80% lab attendance and a passing capstone evaluation score."
    },
    {
        "category": "resource",
        "title": "Free Learning Community & Code Repositories",
        "url": "https://bigbrains.example.com/resources",
        "raw_text": "Access free starter kits, GitHub boilerplate code, weekend webinars, and our 24/7 Discord support community for peer troubleshooting."
    }
]

def run_scraper_and_build_kb():
    knowledge_base = []

    print("[*] Starting Big Brains Scraping & Data Cleaning Pipeline...")

    for item in KNOWLEDGE_SOURCES:
        # Example crawler fetch (graceful fallback)
        try:
            resp = requests.get(item["url"], timeout=3)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                content = clean_text(soup.get_text())
            else:
                content = clean_text(item["raw_text"])
        except Exception:
            content = clean_text(item["raw_text"])

        # Keyword extraction
        words = [w.lower() for w in re.findall(r'\b[A-Za-z]{4,}\b', content)]
        keywords = list(set(words))[:10]

        entry = {
            "title": item["title"],
            "category": item["category"],
            "url": item["url"],
            "content": content,
            "keywords": keywords
        }
        knowledge_base.append(entry)
        print(f" [+] Scraped & Cleaned: {item['title']} ({item['category']})")

    # Save to JSON file
    output_file = "knowledge_base.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, indent=2)

    print(f"[✓] Knowledge Base successfully created and saved to {output_file} with {len(knowledge_base)} documents.\n")
    return knowledge_base

if __name__ == "__main__":
    run_scraper_and_build_kb()