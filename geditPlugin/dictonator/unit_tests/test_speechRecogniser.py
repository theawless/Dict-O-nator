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

from ..configurablesettings import PluginSettings
from ..recogspeechbg import SpeechRecogniser

AUDIO_PATH = os.path.dirname(os.path.abspath(__file__)) + "/test_audio/"


class TestSpeechRecogniser(TestCase):
    def setUp(self):
        PluginSettings()
        # Only test sphinx
        PluginSettings.settings['Main']['recogniser'] = 'Sphinx'
        self.recogniser = SpeechRecogniser(f_action_handler=self.action_handler_fake,
                                           f_bottom_bar_changer=self.bottom_bar_changer_fake)

        self.audio_count = 0
        with sr.AudioFile(AUDIO_PATH + 'hello' + '.wav') as source:
            self.audio0 = sr.Recognizer().record(source)  # read the entire audio file
        with sr.AudioFile(AUDIO_PATH + 'whats_up' + '.wav') as source:
            self.audio1 = sr.Recognizer().record(source)  # read the entire audio file
        with sr.AudioFile(AUDIO_PATH + 'this_is_amazing' + '.wav') as source:
            self.audio2 = sr.Recognizer().record(source)  # read the entire audio file
        with sr.AudioFile(AUDIO_PATH + 'book_on_table' + '.wav') as source:
            self.audio3 = sr.Recognizer().record(source)  # read the entire audio file

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

    def action_handler_fake(self, recognized_text):
        print(recognized_text + " audio_count= " + self.audio_count)
        if self.audio_count == 0:
            self.assertEqual(recognized_text, "hello")
        if self.audio_count == 1:
            self.assertEqual(recognized_text, "whats up")
        if self.audio_count == 2:
            self.assertEqual(recognized_text, "this is amazing")
        if self.audio_count == 3:
            self.assertEqual(recognized_text, "book on table")

        self.audio_count += 1

    def bottom_bar_changer_fake(self, txt):
        # Nothing to be tested
        pass
