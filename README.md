# FeverCoach Blog Extraction Pipeline

Fetches a live FeverCoach blog post, extracts article sections, and prepares content for video script generation.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4
```

## Run
```bash
python3 extract.py
```

## Output Sections

- `title` — Article title
- `disclaimer` — Medical disclaimer
- `question` — Parent's question
- `answer` — Doctor's answer
- `doctor_needed` — When to see a doctor
- `cta` — Call to action
