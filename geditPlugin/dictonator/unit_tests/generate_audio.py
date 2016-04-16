#!/usr/bin/env python3
import speech_recognition as sr
import os

AUDIO_PATH = os.path.dirname(os.path.abspath(__file__)) + "/test_audio/"

file_name = input("Input Filename(without extension): ")
# obtain audio from the microphone
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Wait for two seconds")
    r.adjust_for_ambient_noise(source, 2)
    print("Say something!")
    audio = r.listen(source)
# write audio to a WAV file
with open(AUDIO_PATH + file_name + ".wav", "wb+") as f:
    f.write(audio.get_wav_data())
