import pandas as pd
import requests
import os

# input_file = "../data/youtube_links_with_transcripts.csv"

# df = pd.read_csv(input_file)

#  === Configuration ===
CSV_FILE_PATH = "../data/youtube_links_with_transcripts.csv"
API_ENDPOINT= "https://transcript-summarizer-1.onrender.com/api/v1/add-transcript"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2ODRhYTdhMDNlYTBkMzJiM2Y1OTY3M2UiLCJlbWFpbCI6ImliZWt3ZWVtbWFudWVsMDA3QGdtYWlsLmNvbSIsImlhdCI6MTc0OTgwMDgxNSwiZXhwIjoxNzQ5ODg3MjE1fQ.Q41uqn-JTcXd5hmOj0G4P9J0tV_buXYI8BBwgcrH4Qw"
LOG_FILE = "../data/sent.log"

# === Auth Headers ===
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# === Load sent IDs ===
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r') as f:
        sent_ids = set(line.strip() for line in f if line.strip())
else:
    sent_ids = set()
    


#  === Load CSV ===
df = pd.read_csv(CSV_FILE_PATH)

# === Send Unsynced Rows ===
for index, row in df.iterrows():
    video_id = str(row['video_id'])
    
    if video_id in sent_ids:
        continue # Skip already sent
    
    # videoId, transcript, url, title, newsChannel
    data = {
        "videoId": video_id,
        "transcript": row["transcript"],
        "url": row["url"],
        "title": row["title"],
        "newsChannel": row["news channel"]
    }
    
    try:
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        print(f"[{index}] Sent: {video_id}")
        
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(video_id + '\n')
            
    except requests.exceptions.RequestException as e:
        print(f"[{index}] Failed to send {video_id}: {e}")
        break
        
    
