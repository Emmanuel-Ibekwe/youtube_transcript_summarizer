from youtube_transcript_api import YouTubeTranscriptApi

# https://youtu.be/1Zm-1qKSjXo?si=WZeHKqeWFrkyjF_f
video_id = "1Zm-1qKSjXo"

transcript = YouTubeTranscriptApi.get_transcript(video_id)

# for entry in transcript:
#     print(entry['text'])

full_transcript = " ".join([entry['text'] for entry in transcript])
print(full_transcript)