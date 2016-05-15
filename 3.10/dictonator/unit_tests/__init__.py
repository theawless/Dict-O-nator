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

from dictonator.unit_tests.test_actionhandler import TestDictonatorActionHandler
from dictonator.unit_tests.test_settings import TestDictonatorSettings
from dictonator.unit_tests.test_actions import TestDictonatorActions


class AllTestSuite:
    def __init__(self):
        super().__init__()
        self.test_settings = TestDictonatorSettings()
        self.test_acts_handler = TestDictonatorActionHandler()
        self.test_acts_mod = TestDictonatorActions()

    def run_all_tests(self):
        if self.test_settings.setUp():
            self.test_settings.run()
        print("Setting tests finished")
        if self.test_acts_handler.setUp():
            self.test_acts_handler.run()
        print("Document actions handler tests finished")
        if self.test_acts_mod.setUp():
            self.test_acts_mod.run()
        print("Document actions tests finished")

        print("\nAll tests finished Successfully\n")


def start_tests():
    ats = AllTestSuite()
    ats.run_all_tests()
