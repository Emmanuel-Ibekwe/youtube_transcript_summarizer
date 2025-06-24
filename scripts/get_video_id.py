from urllib.parse import urlparse, parse_qs
import pandas as pd


def get_video_id(url):
    try:
        parsed = urlparse(url)
        if parsed.netloc == "youtu.be":
            return parsed.path.lstrip("/")
        elif parsed.netloc in ["www.youtube.com", "youtube.com"]:
            query = parse_qs(parsed.query)
            return query.get("v", [None])[0]
        else:
            return None
    except Exception as e:
        return None
    
# Load Excel file 
df = pd.read_excel('youtube urls.xlsx')

# Extract video IDs
df['video_id'] = df['url'].apply(get_video_id)

# Save to a new Excel file
df.to_excel('youtube_links_with_video_ids.xlsx', index=False)

print('Video IDs extracted and saved to "youtube_links_with_video_ids.xlsx"')