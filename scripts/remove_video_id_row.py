import pandas as pd

file_path = "../data/filtered_youtube_links_with_video_ids.xlsx"
df = pd.read_excel(file_path)

# Specify the video_id you want to remove
video_id_to_remove = "mm6FJMJcAlM" # Replace with the actual video_id value

# Filter the DataFrame to exclude the video id to be remove
df_filtered = df[df['video_id'] != video_id_to_remove]

# Save file
df_filtered.to_excel(file_path, index=False)

print("Row(s) with video_id", video_id_to_remove, "have been removed.")

# Bq1NjE2a6so
# AT2iL8vgRFo
# mm6FJMJcAlM