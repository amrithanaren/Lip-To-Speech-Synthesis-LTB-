import torch
import librosa
import os
import numpy as np
import soundfile as sf
from moviepy.editor import * 
from gtts import gTTS
from scipy.io import wavfile
from IPython.display import Audio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer


def readLip(filename):
    language = 'en'
    transcription = "did you say somethin?" 
    UPLOAD_FOLDER = './uploads/'
    my_clip = VideoFileClip(UPLOAD_FOLDER+filename) #mp.
    audioFile = filename[:-4] + ".wav"
    my_clip.audio.write_audiofile(audioFile)

    tokenizer = Wav2Vec2Tokenizer.from_pretrained('./preTrainedWeithts' ) # use_auth_token=True
    model = Wav2Vec2ForCTC.from_pretrained("./preTrainedWeithts")

    print("\n\n", audioFile, "\n\n")

    data = wavfile.read(audioFile)
    framerate = data[0]
    sounddata = data[1]
    time = np.arange(0,len(sounddata))/framerate
    input_audio, _ = librosa.load(audioFile, sr=16000)
    input_values = tokenizer(input_audio, return_tensors="pt").input_values
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]
    print(transcription, "\n")

    audioObj = gTTS(text=transcription, lang=language, slow=False)
    audioObj.save(audioFile)


    print("\n\naudio file created.\n\n")

    clip = VideoFileClip(UPLOAD_FOLDER+filename)
    # getting only first 5 seconds
    # clip = clip.subclip(0, 5)
    
    # loading audio file
    audioclip = AudioFileClip(audioFile)
    
    # adding audio to the video clip
    videoclip = clip.set_audio(audioclip)

    print("video file created")

    # clip.write_videofile(filename)
    videoclip.ipython_display()


    print("video file saved")

    return transcription

# readLip("VID20220106145619.mp4")