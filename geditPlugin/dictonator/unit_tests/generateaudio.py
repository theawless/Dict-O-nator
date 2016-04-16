# Dict'O'nator - A dictation plugin for gedit.
# Copyright (C) <2016>  <Abhinav Singh>
#
# This file is part of Dict'O'nator.
#
# Dict'O'nator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dict'O'nator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dict'O'nator.  If not, see <http://www.gnu.org/licenses/>.

import os

import speech_recognition as sr
TEST_PATH = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(TEST_PATH + '/test_audio'):
    os.makedirs(TEST_PATH + '/test_audio')
AUDIO_PATH = TEST_PATH + "/test_audio/"

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
