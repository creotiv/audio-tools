# audio-tools
Tools for creating audio datasets

## Use

pip3 install -r requirements.txt

python3 youtubedl.py https://www.youtube.com/watch?v=PpW6UmaF3c0 ./path

ffmpeg -i ./path/audio.m4a -ar 22050 -acodec pcm_u8 ./path/audio.wav

python3 splitter.py -i ./path/audio.wav -o ./path/clips --max_length 10 --db-thresh 20

export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google/auth.json

python3 transcribe.py ./path/clips
