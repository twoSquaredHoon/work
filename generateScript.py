import anthropic
from extract import result as blog

client = anthropic.Anthropic()

system_prompt = """
You are a script writer for a Korean-language pediatric health video channel called FeverCoach.
Your job is to convert blog post content into a tight spoken script for an AI avatar presenter.

Rules:
- Write in natural, warm, conversational Korean
- Target duration: under 60 seconds of speech (~250 syllables total)
- Tone: calm, professional, reassuring — like a trusted pediatric doctor
- Do NOT include stage directions, timestamps, or section headers in the output
- Output only the spoken words, nothing else
- Structure must follow this order exactly:
  1. Disclaimer (one short sentence)
  2. Question hook (restate the question naturally)
  3. Answer (core content, concise)
  4. Doctor-needed cases (when to visit, + brief disclaimer reminder)
- Keep sentences short and easy to follow when spoken aloud
""".strip()

user_prompt = f"""
Here is the blog post content. Generate the avatar script.

TITLE: {blog['title']}

DISCLAIMER: {blog['disclaimer']}

QUESTION: {blog['question']}

ANSWER: {blog['answer']}

DOCTOR-NEEDED: {blog['doctor_needed']}
""".strip()

response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": user_prompt}
    ],
    system=system_prompt
)

script = response.content[0].text

print("=" * 60)
print("AVATAR SCRIPT")
print("=" * 60)
print(script)
print("=" * 60)