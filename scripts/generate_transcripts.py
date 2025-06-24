import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable


def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        raise
    except Exception as e:
        raise
    
    
# def fetch_with_index(row):
#     index = row.name
#     video_id = row['video_id']
#     transcript = fetch_transcript(video_id)
#     print(f"Index {index} processed")
#     return transcript
    
    
# Load file

# df["transcript"] = df.apply(fetch_with_index, axis=1)

# df.to_csv("youtube_links_with_transcripts.csv", index=False)

# print("Transcripts added and saved to 'videos_with_transcripts.csv'")

input_file = "../data/filtered_youtube_links_with_video_ids.xlsx"
output_file = "../data/youtube_links_with_transcripts.csv"

try:
    df_out = pd.read_csv(output_file)
    df_in = pd.read_excel(input_file)
    df_in["transcript"] = ""
except FileNotFoundError:
    df_in = pd.read_excel(input_file)
    df_in["transcript"] = ""
    df_out = None
    
increase_index = True

  
# Start processing
for index, row in df_in.iterrows():
    if df_out is not None and df_out.shape[0] != 0:
        if index <= df_out.shape[0] - 1:
            df_in.at[index, "transcript"] = df_out.at[index, "transcript"]
            continue
        if index == df_out.shape[0]:    
            print("df_out transcripts copied to df_in")
    
    try:
        transcript = fetch_transcript(row["video_id"])
        df_in.at[index, "transcript"] = transcript
        print(f"Index {index} processed successfully")
    except Exception as e:
        print(f"Error occurred at index {index}: {e}")
        df_out = df_in.iloc[:index]
        increase_index = False
        break
    
# Final save if loop finishes without error
if increase_index == True:
    df_out = df_in.iloc[:index + 1]
    df_out.to_csv(output_file, index=False) # Save progress
    print("All transcripts processed and saved.")  
else:
    df_out = df_in.iloc[:index]
    df_out.to_csv(output_file, index=False)
    print("Progress saved. Stop execution.")
    
# possible error: 
# Error occurred at index {index}: no element found: line 1, column 0
# 441 transcripts processed.