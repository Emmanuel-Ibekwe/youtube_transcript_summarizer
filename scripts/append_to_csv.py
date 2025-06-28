import os
import csv
import re
import requests
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("ACCESS_TOKEN")


# Define the CSV file path
CSV_FILE_PATH = "../data/youtube_transcripts_with_summaries.csv"
LOG_FILE_PATH = '../data/processed_video_ids.log'
API_ENDPOINT = "https://transcript-summarizer-1.onrender.com/api/v1/transcripts"

# Define field names
FIELDNAMES = ['url', 'title', 'news_channel', 'video_id', 'transcript', 'summary']

def init_csv():
    """Create CSV with header if it doesn't exist."""
    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, 'w', newline="", encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def load_logged_ids():
    """Load videoIds from the log file."""
    if not os.path.exists(LOG_FILE_PATH):
        return set()
    with open(LOG_FILE_PATH, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())


def log_video_id(video_id):
    """Append a video_id to the log file."""
    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
        f.write(video_id + '\n')


def camel_to_snake_case(name):
    """Convert camelCase or PascalCase to snake_case."""
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def normalize_element(element):
    """convert keys to snake_case and extract only needed fields."""
    # Convert all keys to snake_case
    snake_case_element = {
        camel_to_snake_case(key): value 
        for key, value in element.items()
    }

    # Filter only desired fields (in snake case)
    return {key: snake_case_element.get(key, '') for key in FIELDNAMES}


def append_to_csv(element):
    """Append normalized (filtered and snake_cased) data to CSV."""
    normalized = normalize_element(element)
    with open(CSV_FILE_PATH, 'a', newline="", encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(normalized)


headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

def fetch_transcripts():
    response = requests.get(f"{API_ENDPOINT}?page=1&limit={441}", headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['transcripts']

def main():
    init_csv()
    logged_ids = load_logged_ids()

    
    try:
        transcripts = fetch_transcripts()
        num = len(transcripts)
        for index, transcript in enumerate(transcripts):
            transcript_id = transcript.get("_id")
            if not transcript_id:
                print(f"[{index}] Skipped: No videoId found.")
                continue

            if transcript_id in logged_ids:
                print(f"[{index}] Skipped: Already processed {transcript_id}")
                continue

            append_to_csv(transcript)
            log_video_id(transcript_id)
            logged_ids.add(transcript_id)
            print(f"[{index}] processed: {transcript_id}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        

if __name__ == '__main__':
    main()
    


