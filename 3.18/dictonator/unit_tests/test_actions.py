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

from unittest import TestCase

from dictonator.statesacts import DictonatorActions


class TestDictonatorActions(TestCase):
    def setUp(self):
        self.da = DictonatorActions()
        return True

    def run(self, result=None):
        self.test_decide_action()
        self.test_get_number()

    def test_decide_action(self):
        self.assertEqual(self.da.decide_action("hello"), ('continue_dictation', 1, ''))
        self.assertEqual(self.da.decide_action("what's up"), ('continue_dictation', 1, ''))
        self.assertEqual(self.da.decide_action("put 8 digit five times"), ('put', 5, 'eight_digit'))
        self.assertEqual(self.da.decide_action("put eight digit five times"), ('put', 5, 'eight_digit'))
        self.assertEqual(self.da.decide_action("delete word eight times"), ('delete_word', 8, ''))
        self.assertEqual(self.da.decide_action("go to line 58"), ('goto_line', 58, ''))
        self.assertEqual(self.da.decide_action("delete sentence 5 times"), ('delete_sentence', 5, ''))
        self.assertEqual(self.da.decide_action("close document"), ('close_document', 1, ''))
        self.assertEqual(self.da.decide_action("put apostrophe"), ('put', 1, 'apostrophe'))
        print("Decide actions working correctly")

    def test_get_number(self):
        self.assertEqual(self.da.get_number('seven'), 7)
        self.assertEqual(self.da.get_number('seventy two'), 72)
        self.assertEqual(self.da.get_number('5'), 5)
        self.assertEqual(self.da.get_number('put 5 digit'), 5)
        self.assertEqual(self.da.get_number("what's up"), 1)
        self.assertEqual(self.da.get_number('delete word eight times'), 8)
        self.assertEqual(self.da.get_number('delete sentence 7 times'), 7)
        print("Get number working correctly")
