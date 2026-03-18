# ProspectIQ — BDR/SDR ICP Scorer

A Python tool for Sales Development Representatives (BDRs/SDRs) that analyses a company's homepage and returns an **ICP match score (1–10)** plus a **personalised outreach suggestion**.

---

## 🧠 What it does

1. The user defines their **Ideal Customer Profile (ICP)** — target industry, growth signals, red flags
2. The user pastes a **company homepage URL**
3. The program **scrapes and analyses** the page using NLP techniques
4. It returns:
   - An **ICP Score** from 1 to 10
   - The **top keywords** found on the page
   - A **sentiment analysis** of the company's tone
   - A **personalised outreach suggestion** (opening hook + tone tip)

---

## 🛠️ Technologies Used

| Library | Purpose |
|---|---|
| `requests` + `beautifulsoup4` | Web scraping (homepage text extraction) |
| `rake_nltk` | Keyword extraction (RAKE algorithm) |
| `transformers` (Hugging Face) | Sentiment analysis |
| `spacy` | Named Entity Recognition (NER) |

---

## ⚙️ Getting Started

### Prerequisites

Make sure you have **Python 3.8+** and **Anaconda** installed.

### 1. Create a new Anaconda environment

```bash
conda create -n prospectiq python=3.11
conda activate prospectiq
```

### 2. Install required libraries

```bash
pip install requests beautifulsoup4 rake-nltk transformers torch spacy
python -m spacy download en_core_web_sm
```

### 3. Clone the repository

```bash
git clone https://github.com/your-username/ProspectIQ.git
cd ProspectIQ
```

### 4. Run the program

```bash
python prospect_scorer.py
```

---

## 🚀 Example Usage

```
🔍  ProspectIQ — BDR/SDR ICP Scorer

📋  Define your Ideal Customer Profile (ICP)
🏭  Target industry keywords: SaaS, software, cloud
✅  Growth signals to look for: hiring, expanding, Series, AI
❌  Red-flag keywords to avoid: nonprofit, government

🌐  Enter company homepage URL: https://example-company.com

⏳  Scraping and analysing the homepage...

📊  ICP Score:    8.0 / 10
😊  Sentiment:    POSITIVE (94.3% confidence)
🔑  Top Keywords: cloud infrastructure, AI platform, enterprise solutions
🏢  Organisations: AWS, Salesforce

💌  Outreach Personalisation Suggestion
🟢  Priority: HIGH — This company fits your ICP well.
📧  Opening hook:
    "I came across cloud infrastructure on your homepage and immediately thought
    of how [your solution] helps teams like yours [key benefit]."
🎯  Tone Tip: Be upbeat, forward-looking, and vision-oriented.
```

---

## 📁 Project Structure

```
ProspectIQ/
│
├── prospect_scorer.py      # Main program
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
└── acknowledgment.md       # Credits and contributions
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
