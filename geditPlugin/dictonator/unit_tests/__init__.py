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

from dictonator.unit_tests.test_dictonatorPluginActions import TestDictonatorPluginActions
from dictonator.unit_tests.test_pluginSettings import TestPluginSettings
from dictonator.unit_tests.test_speechRecogniser import TestSpeechRecogniser


class AllTestSuite:
    def __init__(self):
        super().__init__()
        self.test_settings = TestPluginSettings()
        self.test_stt = TestSpeechRecogniser()
        self.test_acts = TestDictonatorPluginActions()

    def run_all_tests(self):
        if self.test_settings.setUp():
            self.test_settings.run()
        print("Setting tests finished")
        if self.test_stt.setUp():
            self.test_stt.run()
        print("Speech Recognition tests finished")
        if self.test_acts.setUp():
            self.test_acts.run()
        print("Document actions tests finished")

        print("\nAll tests finished Successfully\n")


def start_tests():
    ats = AllTestSuite()
    ats.run_all_tests()
