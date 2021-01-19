from youtube_dl import YoutubeDL
import sys

postprocessors = [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': "best",
    'preferredquality': 0,
    'nopostoverwrites': False,
}]

try:
    out = sys.argv[2]
except:
    out = '.'

options = {
    'postprocessors': postprocessors,
    'outtmpl': '%s/%%(title)s.%%(ext)s' % out,
    'format': 'bestaudio/best',
    'ignoreerrors': True
}

with YoutubeDL(options) as ydl:
    ydl.download(list([sys.argv[1]]))