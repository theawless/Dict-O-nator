import os
from unittest import TestCase

from gi.repository import Gedit

from dictonator.pluginactions import DictonatorPluginActions
from dictonator.statesmod import DictonatorStates

TEST_PATH = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(TEST_PATH + '/.logs'):
    os.makedirs(TEST_PATH + '/.logs')

TEXT_PATH = TEST_PATH + "/test_text/"


class TestDictonatorPluginActions(TestCase):
    def setUp(self):
        self.plugin_actions = DictonatorPluginActions(f_bottom_bar_changer=self.bottom_bar_changer_fake,
                                                      f_bottom_bar_adder=self.bottom_bar_adder_fake)
        try:
            with open(TEXT_PATH + 'original' + '.txt') as file:
                self.org = file.read()  # read the entire text file
            with open(TEXT_PATH + 'deleted_line' + '.txt') as file:
                self.dl = file.read()  # read the entire text file
            with open(TEXT_PATH + 'deleted_sentence' + '.txt') as file:
                self.ds = file.read()  # read the entire text file
            with open(TEXT_PATH + 'deleted_word' + '.txt') as file:
                self.dw = file.read()  # read the entire text file
            with open(TEXT_PATH + 'inserted_text' + '.txt') as file:
                self.ti = file.read()  # read the entire text file
            self.cd = ""
            self.plugin_actions.document = Gedit.Document()
            self.plugin_actions.document.set_text(self.org)
            self.plugin_actions.recogniser.is_listening = True
            return True
        except FileNotFoundError:
            print("Texts files not found, skipping this test")
            return False

    def run(self, result=None):
        self.test_get_cursor_position()
        self.test_inserttext()
        self.test_action_handler()

    def place_cursor_at(self, line, offset):
        i = self.plugin_actions.document.get_iter_at_line_offset(line, offset)
        self.plugin_actions.document.place_cursor(i)

    def test_get_cursor_position(self):
        i = self.plugin_actions.document.get_iter_at_line_offset(2, 5)
        self.place_cursor_at(2, 5)
        j = self.plugin_actions.get_cursor_position(self.plugin_actions.document)
        if i.compare(j) == 0:
            print("Get cursor position tested")
        else:
            self.fail("Got incorrect cursor position")

    def get_doc_text(self):
        return self.plugin_actions.document.get_text(self.plugin_actions.document.get_start_iter(),
                                                     self.plugin_actions.document.get_end_iter(), False)

    def test_inserttext(self):
        self.place_cursor_at(2, 5)
        self.plugin_actions.inserttext(" dictonator is the best", True)
        self.assertEqual(self.get_doc_text(), self.ti, "Insert text failed")
        print("Insert text tested")

    def test_action_handler(self):

        self.plugin_actions.action_handler("clear document", DictonatorStates.recognised, "")
        self.assertEqual(self.get_doc_text(), self.cd, "Clear document failed")
        print("Clear document tested")

        self.plugin_actions.document.set_text(self.org)
        self.place_cursor_at(2, 6)
        self.plugin_actions.action_handler("delete line", DictonatorStates.recognised, "")
        self.assertEqual(self.get_doc_text(), self.dl, "Delete line failed")
        print("Delete line tested")

        self.plugin_actions.document.set_text(self.org)
        self.place_cursor_at(2, 105)
        self.plugin_actions.action_handler("delete sentence", DictonatorStates.recognised, "")
        self.assertEqual(self.get_doc_text(), self.ds, "Delete sentence failed")
        print("Delete sentence tested")

        self.plugin_actions.document.set_text(self.org)
        self.place_cursor_at(2, 19)
        self.plugin_actions.action_handler("delete word", DictonatorStates.recognised, "")
        self.assertEqual(self.get_doc_text(), self.dw, "Delete word failed")
        print("Delete word tested")

    def bottom_bar_changer_fake(self, a):
        pass

    def bottom_bar_adder_fake(self, a, b, c):
        pass

    # Not implemented
    def test_on_setup_activate(self):
        pass

    def test_on_listen_activate(self):
        pass

    def test_on_stop_activate(self):
        pass
