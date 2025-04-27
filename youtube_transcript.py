
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Extract video ID from the URL
video_url = 'https://www.youtube.com/watch?v=9vqlZneYq7w'
video_id = video_url.split("v=")[-1]

# Fetch transcript
try:
    transcript = YouTubeTranscriptApi().fetch(video_id=video_id,languages=['hi'])

    # Format the transcript
    formatter = TextFormatter()
    formatted_transcript = formatter.format_transcript(transcript)
    print(formatted_transcript)  # This will print the transcript text
except Exception as e:
    print("Error fetching transcript:", e)
