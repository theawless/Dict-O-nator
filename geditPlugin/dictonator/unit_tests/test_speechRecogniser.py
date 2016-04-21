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
from unittest import TestCase

import speech_recognition as sr

from dictonator.configurablesettings import PluginSettings
from dictonator.recogspeechbg import SpeechRecogniser
from dictonator.statesmod import DictonatorStates

TEST_PATH = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = TEST_PATH + "/test_audio/"


class TestSpeechRecogniser(TestCase):
    def setUp(self):
        PluginSettings()
        # Only test sphinx
        PluginSettings.settings['Main']['recogniser'] = 'Sphinx'
        self.recogniser = SpeechRecogniser(f_action_handler=self.action_handler_fake)
        self.audio_count = 0
        try:
            with sr.AudioFile(AUDIO_PATH + 'hello' + '.wav') as source:
                self.audio0 = sr.Recognizer().record(source)  # read the entire audio file
            with sr.AudioFile(AUDIO_PATH + 'whats_up' + '.wav') as source:
                self.audio1 = sr.Recognizer().record(source)  # read the entire audio file
            with sr.AudioFile(AUDIO_PATH + 'this_is_amazing' + '.wav') as source:
                self.audio2 = sr.Recognizer().record(source)  # read the entire audio file
            with sr.AudioFile(AUDIO_PATH + 'book_on_table' + '.wav') as source:
                self.audio3 = sr.Recognizer().record(source)  # read the entire audio file
            return True
        except FileNotFoundError:
            print("Audio files not found, skipping this test")
            return False

    def run(self, result=None):
        self.test_start_recognising()
        self.test_recog_callback()

    def test_start_recognising(self):
        # Not implemented yet
        pass

    def test_recog_callback(self):
        self.recogniser.recog_callback(self.recogniser.re, audio=self.audio0, testing=True)
        self.recogniser.recog_callback(self.recogniser.re, audio=self.audio1, testing=True)
        self.recogniser.recog_callback(self.recogniser.re, audio=self.audio2, testing=True)
        self.recogniser.recog_callback(self.recogniser.re, audio=self.audio3, testing=True)

    def action_handler_fake(self, recognized_text, state, msg):
        # print(recognized_text + " audio_count= " + self.audio_count)
        if state == DictonatorStates.recognised:
            if self.audio_count == 0:
                self.assertEqual(recognized_text, "hello")
                print("Audio" + str(self.audio_count) + "was recognized properly")
            if self.audio_count == 1:
                self.assertEqual(recognized_text, "what's up")
                print("Audio" + str(self.audio_count) + "was recognized properly")
            if self.audio_count == 2:
                self.assertEqual(recognized_text, "this is amazing")
                print("Audio" + str(self.audio_count) + "was recognized properly")
            if self.audio_count == 3:
                self.assertEqual(recognized_text, "book on table")
                print("Audio" + str(self.audio_count) + "was recognized properly")

        elif state == DictonatorStates.error:
            self.fail("Could not understand above audio")
        elif state == DictonatorStates.fatal_error:
            self.fail("Fatal error.")

        self.audio_count += 1
