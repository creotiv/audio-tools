from google.cloud import speech
import io
import os

def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        sample_rate_hertz=22050,
        language_code="ru-RU",
    )

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    out = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        out.append(result.alternatives[0].transcript)
    return out

def main(path):
    out = open(os.path.join(path,'..','text.csv'),'w')
    files = os.listdir(path)
    for f in files:
        fpath = os.path.join(path,f)
        res = transcribe_file(fpath)
        out.write(f"{fpath.split('/')[-1]},{res[0]}\n")
        break

# add GOOGLE_APPLICATION_CREDENTIALS=/home/creotiv/.google/auth.json

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument('input_dir', type=str, 
                        help="Path to the audio dir")

    args = parser.parse_args()

    main(args.input_dir)