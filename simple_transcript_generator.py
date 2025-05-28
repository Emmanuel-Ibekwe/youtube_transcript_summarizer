from youtube_transcript_api import YouTubeTranscriptApi

# https://youtu.be/JFTMs6fl-2I?si=es54bba7_OPYqkWg
video_id = "JFTMs6fl-2I"

transcript = YouTubeTranscriptApi.get_transcript(video_id)

# for entry in transcript:
#     print(entry['text'])

full_transcript = " ".join([entry['text'] for entry in transcript])
print(full_transcript)