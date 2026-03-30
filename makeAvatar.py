import requests
import time
import os

from generateScript import script

HEYGEN_API_KEY = os.environ.get("HEYGEN_API_KEY")
AVATAR_IMAGE_PATH = "assets/Dropshot.jpg"
OUTPUT_FILE = "output_avatar.mp4"
VOICE_ID = "ko-KR-SunHiNeural"  # Korean female voice

HEADERS = {
    "X-Api-Key": HEYGEN_API_KEY,
    "Content-Type": "application/json"
}

# ── Step 1: Upload avatar image ──────────────────────────────────────────────

def upload_avatar_image(image_path):
    print("Uploading avatar image...")
    with open(image_path, "rb") as f:
        response = requests.post(
            "https://upload.heygen.com/v1/talking_photo",
            headers={"X-Api-Key": HEYGEN_API_KEY},
            files={"file": (os.path.basename(image_path), f, "image/jpeg")}
        )
    response.raise_for_status()
    talking_photo_id = response.json()["data"]["talking_photo_id"]
    print(f"Avatar uploaded: {talking_photo_id}")
    return talking_photo_id

# ── Step 2: Submit video generation job ─────────────────────────────────────

def generate_video(talking_photo_id, script_text):
    print("Submitting video generation job...")
    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "talking_photo",
                    "talking_photo_id": talking_photo_id
                },
                "voice": {
                    "type": "text",
                    "input_text": script_text,
                    "voice_id": VOICE_ID
                }
            }
        ],
        "dimension": {
            "width": 1920,
            "height": 1080
        }
    }
    response = requests.post(
        "https://api.heygen.com/v2/video/generate",
        headers=HEADERS,
        json=payload
    )
    response.raise_for_status()
    video_id = response.json()["data"]["video_id"]
    print(f"Job submitted. Video ID: {video_id}")
    return video_id

# ── Step 3: Poll until ready ─────────────────────────────────────────────────

def poll_video(video_id, interval=10, max_wait=600):
    print("Waiting for video to render...")
    elapsed = 0
    while elapsed < max_wait:
        response = requests.get(
            f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
            headers=HEADERS
        )
        response.raise_for_status()
        data = response.json()["data"]
        status = data["status"]
        print(f"  Status: {status} ({elapsed}s elapsed)")

        if status == "completed":
            return data["video_url"]
        elif status == "failed":
            raise RuntimeError(f"Video generation failed: {data.get('error')}")

        time.sleep(interval)
        elapsed += interval

    raise TimeoutError("Video generation timed out.")

# ── Step 4: Download MP4 ─────────────────────────────────────────────────────

def download_video(video_url, output_path):
    print(f"Downloading video to {output_path}...")
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Saved: {output_path}")

# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    talking_photo_id = upload_avatar_image(AVATAR_IMAGE_PATH)
    video_id = generate_video(talking_photo_id, script)
    video_url = poll_video(video_id)
    download_video(video_url, OUTPUT_FILE)
    print("Done.")
