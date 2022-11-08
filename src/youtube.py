# Download from youtube

# install pytube before using it
import pytube
try:
    video = pytube.YouTube('https://www.youtube.com/watch?v=dQw4w9WgXcQ').streams.first()
    video.download('./Downloads')
    print("File downloaded.")
except Exception as E:
    print(f"Error: {str(E)}")
