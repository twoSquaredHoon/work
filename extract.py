import requests
from bs4 import BeautifulSoup

url = "https://www.fevercoach.us/ko/post/q-5%EA%B0%9C%EC%9B%94-%EC%95%84%EA%B8%B0%EA%B0%80-%EC%9E%90%EA%BE%B8-%EC%9E%90%EA%B8%B0-%EC%96%BC%EA%B5%B4%EC%9D%84-%EB%95%8C%EB%A0%A4%EC%9A%94-%EC%99%9C-%EA%B7%B8%EB%9F%B0-%EA%B1%B8%EA%B9%8C%EC%9A%94"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(url, headers=headers, timeout=20).text
soup = BeautifulSoup(html, "html.parser")

text = soup.get_text("\n", strip=True)

# Keep only the article area
start_marker = "Q: 5개월 아기가 자꾸 자기 얼굴을 때려요. 왜 그런 걸까요?"
end_marker = "최근 게시물"

start = text.find(start_marker)
end = text.find(end_marker)

article = text[start:end].strip()

title = start_marker
disclaimer = article.split("질문:")[0].split("2분 분량")[-1].strip()
question = article.split("질문:")[1].split("답변:")[0].strip()
answer = article.split("답변:")[1].split("병원 진료가 필요한 경우")[0].strip()
doctor_needed = article.split("병원 진료가 필요한 경우")[1].split("지금도 충분히 잘하고 계시니")[0].strip()
cta = article.split("지금도 충분히 잘하고 계시니")[1].strip()

result = {
    "title": title,
    "disclaimer": disclaimer,
    "question": question,
    "answer": answer,
    "doctor_needed": doctor_needed,
    "cta": cta
}

print(result)