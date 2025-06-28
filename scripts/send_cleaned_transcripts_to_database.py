import pandas as pd
import requests 
import os
from dotenv import load_dotenv

CSV_FILE_PATH = "../data/youtube_links_with_recleaned_transcripts.csv"
API_ENDPOINT= "https://transcript-summarizer-1.onrender.com/api/v1"
LOG_FILE = "../data/edit_transcript_sent.log"

# Load variables from .env into environment
load_dotenv()


# Now you can access them like normal environment variables
access_token = os.getenv("ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# === Load sent IDs ===
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        sent_ids = set(line.strip() for line in f if line.strip())
else:
    sent_ids = set()


#  === Load CSV ===
df = pd.read_csv(CSV_FILE_PATH)

# === Send Unsynced Rows ===
for index, row in df.iterrows():
    video_id = str(row["video_id"])

    if video_id in sent_ids:
        continue # Skip already sent

    data = {
        "transcript": row["transcript"]
    }

    try:
        response = requests.patch(f"{API_ENDPOINT}/transcripts/{video_id}", json=data, headers=headers)
        response.raise_for_status()
        print(f"[{index}] Sent: {video_id}")

        with open(LOG_FILE, "a") as log_file:
            log_file.write(video_id + "\n")

    except requests.exceptions.RequestException as e:
        print(f"[{index}] Failed to send {video_id}: {e}")
        break





