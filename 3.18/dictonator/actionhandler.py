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

import sys
import time

from gi.repository import GLib, Gedit

from dictonator.recogspeech import SpeechRecogniser
from dictonator.saveasdialog import FileSaveAsDialog
from dictonator.settings import DictonatorSettings
from dictonator.statesacts import DictonatorActions, DictonatorStates


class DictonatorActionHandler:
    """Contains recogniser, threader and actions.

         Active window updated from the UI class.
         Handles all actions.
    """

    def __init__(self, f_bottom_bar_changer: callable, f_bottom_bar_adder: callable):
        """ Constructor.

        :param f_bottom_bar_changer: change the bottom bar main text.
        :param f_bottom_bar_adder: add to the actions list in bottom bar.
        """
        # will be set from UI class
        self.window = None
        self.document = None
        self.view = None
        self.tab = None
        # initialize the settings class
        DictonatorSettings()
        # Using like a global function
        self.bottom_bar_text_set = f_bottom_bar_changer
        self.bottom_bar_add = f_bottom_bar_adder
        GLib.threads_init()
        self.recogniser = SpeechRecogniser(self.action_handler)

    def on_setup_activate(self, action):
        """Demands noise fix from recogniser."""

        self.bottom_bar_add(time.strftime("%H:%M:%S"), "None", "setup_dictation")
        self.recogniser.setup_recogniser()

    def on_listen_activate(self, action):
        """Calls to start listening."""
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "None", "start_dictation")
        self.recogniser.start_recognising()

    def on_stop_activate(self, action):
        """Calls to stop listening."""
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "None", "stop_dictation")
        self.recogniser.stop_recognising()

    def inserttext(self, text: str, words=False):
        """Inserts the text in the document at cursor position."""
        doc = self.document
        if not doc:
            return
        doc.begin_user_action()
        ei = self.get_cursor_position(doc)
        if words:
            if not ei.ends_sentence():
                # need to capitalize the new sentence, after sentence ends

                text = text.capitalize()
                doc.insert_at_cursor(text)
            else:
                doc.insert_at_cursor(" " + text)
        else:
            doc.insert_at_cursor(text)
        doc.end_user_action()

    @staticmethod
    def get_cursor_position(doc: Gedit.Document):
        """Gets the current cursor position from the doc given, Gtk+ 2.1 has this inbuilt as property."""
        c_mark = doc.get_insert()
        i = doc.get_iter_at_mark(c_mark)
        return i

    def on_logit_activate(self, action):
        """A test function."""
        self.action_handler('save as document', DictonatorStates.recognised, '')
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "", "log_it")

    def action_handler(self, text: str, state: DictonatorStates, msg: str):
        """ Handle what to do with the state/msg that we get.
        Based on output by the decide_action we choose action."""

        if state is not DictonatorStates.fatal_error and state is not DictonatorStates.recognised:
            # simple msg
            self.bottom_bar_text_set(msg)
        if state is DictonatorStates.fatal_error:
            # fatal error, we will stop listening
            self.on_stop_activate(None)
            self.bottom_bar_text_set(msg)
        if state == DictonatorStates.recognised:
            if not self.recogniser.is_listening:
                # if by chance user stops before the results come
                return
            self.bottom_bar_text_set("Speak!")
            if text == "":
                return
            curr_action, num, special = DictonatorActions.decide_action(text)
            self.bottom_bar_add(time.strftime("%H:%M:%S"), text, curr_action)
            if curr_action == "continue_dictation":
                self.inserttext(text, True)
            elif curr_action == "start_dictation":
                self.on_listen_activate(None)
            elif curr_action == "stop_dictation":
                self.on_stop_activate(None)
            elif curr_action == "hold_dictation":
                pass
            elif curr_action == "put":
                if special != "":
                    for _ in range(num):
                        if 'digit' in special:
                            # using the format how digits are saved
                            self.inserttext(DictonatorActions.digits[special][0])
                        else:
                            # sure that the special is not a digit, again using the format how specials are saved
                            self.inserttext(DictonatorActions.special_chars[special][0])
                    self.inserttext(' ')
            elif curr_action == "scroll_to_cursor":
                vi = self.view
                if not vi:
                    return
                vi.scroll_to_cursor()
            elif curr_action == "goto_line":
                self.document.goto_line(num)
            elif curr_action == "undo":
                doc = self.document
                if not doc:
                    return
                for _ in range(num):
                    if doc.can_undo():
                        doc.undo()
            elif curr_action == "redo":
                doc = self.document
                if not doc:
                    return
                for _ in range(num):
                    if doc.can_redo():
                        doc.redo()
            elif curr_action == "cut_clipboard":
                vi = self.view
                if not vi:
                    return
                vi.cut_clipboard()
            elif curr_action == "copy_clipboard":
                vi = self.view
                if not vi:
                    return
                vi.copy_clipboard()
            elif curr_action == "paste_clipboard":
                vi = self.view
                if not vi:
                    return
                vi.paste_clipboard()
            elif curr_action == "delete_selection":
                vi = self.view
                if not vi:
                    return
                vi.delete_selection()
            elif curr_action == "select_all":
                vi = self.view
                if not vi:
                    return
                vi.select_all()
            elif curr_action == "sentence_end":
                self.inserttext('. ')
            elif curr_action == "line_end":
                self.inserttext('\n')
            elif curr_action == "delete_line":
                doc = self.document
                if not doc:
                    return
                for _ in range(num):
                    doc.begin_user_action()
                    ei = self.get_cursor_position(doc)
                    si = self.get_cursor_position(doc)
                    si.set_line(ei.get_line())
                    ei.forward_to_line_end()
                    doc.delete(si, ei)
                    doc.end_user_action()
            elif curr_action == "delete_sentence":
                doc = self.document
                if not doc:
                    return
                for _ in range(num):
                    doc.begin_user_action()
                    ei = self.get_cursor_position(doc)
                    si = self.get_cursor_position(doc)
                    if not si.starts_sentence():
                        si.backward_sentence_start()
                    si.backward_char()
                    ei.forward_sentence_end()
                    doc.delete(si, ei)
                    doc.end_user_action()
            elif curr_action == "delete_word":
                doc = self.document
                if not doc:
                    return
                for _ in range(num):
                    doc.begin_user_action()
                    ei = self.get_cursor_position(doc)
                    si = self.get_cursor_position(doc)
                    si.backward_word_start()
                    si.backward_char()
                    ei.forward_word_end()
                    doc.delete(si, ei)
                    doc.end_user_action()
            elif curr_action == "clear_document":
                doc = self.document
                if not doc:
                    return
                doc.begin_user_action()
                doc.set_text('')
                doc.end_user_action()
            elif curr_action == "new_document":
                self.window.create_tab(True)
            elif curr_action == "save_document":
                doc = self.document
                if not doc:
                    return
                Gedit.commands_save_document(self.window, doc)
            elif curr_action == "save_as_document":
                # get complete text from current document
                doc = self.document
                txt = doc.get_text(doc.get_start_iter(), doc.get_end_iter(), False)
                gfile_path = FileSaveAsDialog(self.window).file_dialog_handler(txt)
                if gfile_path is not None:
                    # the file has been created by above function and we load it
                    Gedit.commands_load_location(self.window, gfile_path, None, 0, 0)
            elif curr_action == "close_document":
                doc = self.document
                if not doc:
                    return
                tab = self.tab
                if not tab:
                    return
                u_docs = self.window.get_unsaved_documents()
                if self.document not in u_docs:
                    self.window.close_tab(tab)
                else:
                    # to prevent data loss
                    self.bottom_bar_text_set("You might want to save this document before closing it.")
            elif curr_action == "force_close_document":
                tab = self.tab
                if not tab:
                    return
                self.window.close_tab(tab)
            elif curr_action == "exit":
                u_docs = self.window.get_unsaved_documents()
                if len(u_docs) == 0:
                    sys.exit()
                else:
                    self.bottom_bar_text_set("You might want to save all documents before quitting.")
            else:
                self.bottom_bar_text_set("WEIRD STATE! How did you reach this state? O_O")
        return

    def stop(self):
        """Stop Actions class."""
        del self.window
        del self.bottom_bar_text_set
