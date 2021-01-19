import librosa
import os
import numpy as np
import soundfile as sf

def split(audio, sr, threshold=20, max_length=10):
    res = librosa.effects.split(audio, top_db=threshold)
    out = []
    length = 0
    cur = []
    for sp in res:
        _length = length + sp[1] - sp[0] 
        if _length > (sr*max_length) and cur:
            if length <= (sr*max_length):
                out.append(cur)
                cur = []
            length = 0
            _length = length + sp[1] - sp[0] 
        if sp[1] - sp[0] <= (sr*max_length):
            cur.append(sp)
            length = _length
    if cur:
        out.append(cur)
    return out
        
def make_audio(audio, parts, sr, pause=0.2):
    res = audio[parts[0][0]:parts[0][1]]
    for i in range(1,len(parts)):
        s,e = parts[i]
        _pause = int(min((pause*sr),s-parts[i-1][1]))
        res = np.concatenate((res,audio[s-_pause:e]))
    return res

def save_clips(audio, splits, sr, output_path, input_path):
    name = input_path.split('/')[-1].replace('.wav','')
    os.makedirs(output_path, exist_ok=True)
    for i,sp in enumerate(splits):
        a = make_audio(audio, sp, sr, pause=0.2)
        sf.write(os.path.join(output_path,'%s_%04d.wav' % (name,i)), a, sr)

def main(input, output, db_thresh=20, max_length=10):
    audio, sr = librosa.load(input)
    splits = split(audio, sr, threshold=db_thresh, max_length=max_length)
    save_clips(audio, splits, sr, output, input)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input", "-i", 
                        help="Path to the input audio", 
                        required=True)
    parser.add_argument("--output", "-o", 
                        help="Path to where you want to save the output audios.",
                        required=True)
    parser.add_argument("--db-thresh", "-t", 
                        help="DB threshold for splitting.", 
                        type=float,
                        default=20) 
    parser.add_argument("--max_length", "-l", 
                        help="Max clip length in seconds.", 
                        type=float,
                        default=10) 

    args = parser.parse_args()

    main(args.input, args.output, db_thresh=args.db_thresh, max_length=args.max_length)