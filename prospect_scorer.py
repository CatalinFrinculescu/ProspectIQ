"""
ProspectIQ - ICP Scorer
A tool for BDRs/SDRs to score prospects based on their company homepage.
Analyzes the homepage and returns a 1-10 ICP score + outreach suggestions.
"""

import requests
from bs4 import BeautifulSoup
from rake_nltk import Rake
from transformers import pipeline
import spacy
import re


# ─────────────────────────────────────────────
# STEP 1: Define ICP
# ─────────────────────────────────────────────

def get_icp_from_user():
    """Ask the user to define their Ideal Customer Profile (ICP)."""
    print("\n" + "=" * 50)
    print("   📋  Define your Ideal Customer Profile (ICP)")
    print("=" * 50)
    print("Tip: separate multiple values with a comma.\n")

    target_industry = input("🏭  Target industry keywords (e.g. software, SaaS, fintech): ")
    positive_signals = input("✅  Growth signals to look for (e.g. hiring, expanding, AI, Series): ")
    negative_signals = input("❌  Red-flag keywords to avoid (e.g. nonprofit, government, education): ")

    icp = {
        "industry": [kw.strip().lower() for kw in target_industry.split(",") if kw.strip()],
        "positive_signals": [kw.strip().lower() for kw in positive_signals.split(",") if kw.strip()],
        "negative_signals": [kw.strip().lower() for kw in negative_signals.split(",") if kw.strip()],
    }
    return icp


# ─────────────────────────────────────────────
# STEP 2: Scrape Homepage
# ─────────────────────────────────────────────

def scrape_homepage(url):
    """Download and clean the text content from a company homepage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ProspectIQ/1.0)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove non-content tags
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r'\s+', ' ', text).strip()

        # Limit to first 5000 characters to keep processing fast
        return text[:5000]

    except requests.exceptions.RequestException as e:
        print(f"\n⚠️  Error fetching the page: {e}")
        return None


# ─────────────────────────────────────────────
# STEP 3: NLP Analysis
# ─────────────────────────────────────────────

def extract_keywords(text):
    """Extract the most relevant keywords using the RAKE algorithm."""
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()[:10]


def analyze_sentiment(text):
    """Run sentiment analysis using a Hugging Face Transformers pipeline."""
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        truncation=True,
        max_length=512
    )
    result = sentiment_pipeline(text[:512])
    return result[0]


def extract_entities(text):
    """Extract named entities (organizations, locations, etc.) using spaCy."""
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("⚠️  spaCy model not found. Run: python -m spacy download en_core_web_sm")
        return []

    doc = nlp(text[:2000])
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


# ─────────────────────────────────────────────
# STEP 4: ICP Scoring
# ─────────────────────────────────────────────

def score_prospect(text, icp):
    """
    Score the prospect from 1 to 10 based on ICP match.
    
    Scoring logic:
    - Base score: 5
    - +1.5 per industry keyword found (max +3)
    - +0.75 per positive signal found (max +2)
    - -1.5 per negative signal found (max -4)
    """
    text_lower = text.lower()
    score = 5.0  # neutral base

    # Industry match
    industry_matches = sum(1 for kw in icp["industry"] if kw in text_lower)
    score += min(industry_matches * 1.5, 3.0)

    # Positive signals
    positive_matches = sum(1 for kw in icp["positive_signals"] if kw in text_lower)
    score += min(positive_matches * 0.75, 2.0)

    # Negative signals (red flags)
    negative_matches = sum(1 for kw in icp["negative_signals"] if kw in text_lower)
    score -= min(negative_matches * 1.5, 4.0)

    # Clamp between 1 and 10
    score = max(1.0, min(10.0, score))
    return round(score, 1)


# ─────────────────────────────────────────────
# STEP 5: Outreach Suggestion
# ─────────────────────────────────────────────

def generate_outreach_suggestion(score, keywords, sentiment, entities, icp):
    """Generate a personalised outreach suggestion based on the analysis."""
    print("\n" + "=" * 50)
    print("   💌  Outreach Personalisation Suggestion")
    print("=" * 50)

    top_keyword = keywords[0] if keywords else "their core offering"

    # Priority tier
    if score >= 7:
        print("🟢  Priority: HIGH — This company fits your ICP well.")
        print(f"\n📧  Opening hook:")
        print(f'    "I came across {top_keyword} on your homepage and immediately thought')
        print(f'    of how [your solution] helps teams like yours [key benefit]."')
    elif score >= 4:
        print("🟡  Priority: MEDIUM — Partial ICP fit. Worth a soft outreach.")
        print(f"\n📧  Opening hook:")
        print(f'    "I noticed you\'re focused on {top_keyword} — curious if your team')
        print(f'    also deals with [pain point your product solves]?"')
    else:
        print("🔴  Priority: LOW — Weak ICP fit. Add to a low-priority nurture sequence.")
        print(f"\n📧  Opening hook:")
        print(f'    Consider skipping or sending a very generic, low-effort message.')

    # Tone tip based on sentiment
    print(f"\n🎯  Tone Tip:")
    if sentiment["label"] == "POSITIVE":
        print("    The homepage has a positive, energetic tone.")
        print("    → Match it: be upbeat, forward-looking, and vision-oriented.")
    else:
        print("    The homepage has a neutral or cautious tone.")
        print("    → Be formal, data-driven, and ROI-focused.")

    # Entity tip
    orgs = [e[0] for e in entities if e[1] == "ORG"]
    if orgs:
        print(f"\n🏢  Named organisations detected: {', '.join(orgs[:3])}")
        print("    → Mentioning a partner/technology they use can add credibility.")

    print()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print("\n" + "=" * 50)
    print("   🔍  ProspectIQ — BDR/SDR ICP Scorer")
    print("=" * 50)
    print("Paste a company homepage URL and get an ICP score")
    print("plus a personalised outreach suggestion.\n")

    # Step 1 — ICP setup
    icp = get_icp_from_user()

    # Step 2 — URL input
    print()
    url = input("🌐  Enter company homepage URL: ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    print("\n⏳  Scraping and analysing the homepage...")

    # Step 3 — Scrape
    text = scrape_homepage(url)
    if not text:
        print("❌  Could not retrieve the page. Please check the URL and try again.")
        return

    print("✅  Page retrieved successfully.\n")

    # Step 4 — NLP
    print("🔬  Running NLP analysis...")
    keywords = extract_keywords(text)
    sentiment = analyze_sentiment(text)
    entities = extract_entities(text)

    # Step 5 — Score
    score = score_prospect(text, icp)

    # Step 6 — Output
    print("\n" + "=" * 50)
    print("   📊  Analysis Results")
    print("=" * 50)
    print(f"\n🏆  ICP Score:    {score} / 10")
    print(f"😊  Sentiment:    {sentiment['label']} ({round(sentiment['score'] * 100, 1)}% confidence)")
    print(f"\n🔑  Top Keywords: {', '.join(keywords[:5]) if keywords else 'N/A'}")

    orgs = [e[0] for e in entities if e[1] == "ORG"]
    if orgs:
        print(f"🏢  Organisations: {', '.join(orgs[:4])}")

    # Step 7 — Outreach suggestion
    generate_outreach_suggestion(score, keywords, sentiment, entities, icp)


if __name__ == "__main__":
    main()
