# FeverCoach Blog Extraction Pipeline

Fetches a live FeverCoach blog post, extracts article sections, and prepares content for video script generation.

## File Structure
```
work/
├── extract.py          # Fetches and parses blog post
├── generate_script.py  # Generates avatar script via Claude API
├── README.md           # This file
├── .gitignore          # Ignores .venv, __pycache__, .env
└── .venv/              # Python virtual environment (not tracked)
```

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4 anthropic
export ANTHROPIC_API_KEY=your_key_here
```

## Run
```bash
python3 extract.py
python3 generate_script.py
```

## Input

A hardcoded FeverCoach blog post URL:
```
https://www.fevercoach.us/ko/post/q-5개월-아기가-자꾸-자기-얼굴을-때려요-왜-그런-걸까요
```

## Output
```python
{
  "title":         str,  # Article headline
  "disclaimer":    str,  # Medical disclaimer text
  "question":      str,  # Parent's question
  "answer":        str,  # Doctor's full answer
  "doctor_needed": str,  # When to see a doctor
  "cta":           str   # Call to action / closing
}
```

## Code Explanation

| File | What it does | Input | Output |
|---|---|---|---|
| `extract.py` | Fetches live HTML, parses plain text, splits content using Korean text markers | Hardcoded blog post URL | Python dict with 6 keys: `title`, `disclaimer`, `question`, `answer`, `doctor_needed`, `cta` |
| `generate_script.py` | Sends extracted sections to Claude API and generates a spoken Korean avatar script | Dict output from `extract.py` | Spoken Korean script printed to terminal, ready to paste into HeyGen / DropshotAI |
| `.gitignore` | Tells git which files to ignore | N/A | N/A |
| `README.md` | Project documentation | N/A | N/A |