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

import threading
import time

from gi.repository import GLib, Gedit

from . import statesmod
from .configurablesettings import PluginSettings
from .recogspeechbg import SpeechRecogniser
from .saveasdialog import FileSaveAsDialog
from .setlog import logger


class DictonatorPluginActions:
    """Contains recogniser, threader and actions.

         Active window updated from the UI class.
         Handles all actions.
    """

    def __init__(self, f_bottom_bar_changer: callable, f_bottom_bar_adder: callable):
        """ Constructor.

        :param f_bottom_bar_changer: change the bottom bar main text.
        :param f_bottom_bar_adder: add to the actions list in bottom bar.
        """
        self.window = None
        # A manager to handle settings
        self.settings = PluginSettings().settings
        # Using like a global function
        self.bottom_bar_text_set = f_bottom_bar_changer
        self.bottom_bar_add = f_bottom_bar_adder
        GLib.threads_init()
        self.recogniser = SpeechRecogniser(f_bottom_bar_changer, self.action_handler)
        self.threader = threading.Thread(target=self.recogniser.start_recognising)
        self.threader.daemon = True
        logger.debug("Actions INIT")

    def on_setup_activate(self, action):
        """Demands noise fix from recogniser."""
        logger.debug("Demand noise variable set to True")
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "None", "setup_dictation")
        self.recogniser.demand_fix_ambient_noise = True

    def on_listen_activate(self, action):
        """Start recogniser thread."""
        if not self.threader.isAlive():
            self.threader.start()
            logger.debug('Thread Started')
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "None", "start_dictation")
        self.recogniser.wants_to_run = True
        logger.debug("wants to run is true")

    def on_stop_activate(self, action):
        """Stop recogniser thread."""
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "None", "stop_dictation")
        self.recogniser.wants_to_run = False
        logger.debug("wants to run is false")

    def inserttext(self, text: str):
        """Inserts the text in the document at cursor position."""
        doc = self.window.get_active_document()
        doc.begin_user_action()
        ei = self.get_cursor_position(doc)
        if not ei.ends_sentence():
            logger.debug("********************************")
            text = text.capitalize()
        doc.insert_at_cursor(text)
        doc.end_user_action()
        # logger.debug("Inserted Text")

    @staticmethod
    def get_cursor_position(doc: Gedit.Document):
        """Gets the current cursor position from the doc given, Gtk+ 2.1 has this inbuilt as property."""
        c_mark = doc.get_insert()
        i = doc.get_iter_at_mark(c_mark)
        return i

    def on_logit_activate(self, action):
        """A test function."""
        # ei = self.get_cursor_position(self.window.get_active_document())
        # ;ogger.debug(str(ei.starts_sentence()) + str(ei.inside_sentence()) + str(ei.ends_sentence()))
        # self.inserttext("i am abhinav")
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "", "log_it")
        # a fuction to test other functions

    def action_handler(self, text: str):
        """Based on output by the decide_state we choose action."""
        currstate = statesmod.decide_state(text)
        self.bottom_bar_add(time.strftime("%H:%M:%S"), text, currstate)
        if currstate == "continue_dictation":
            self.inserttext(text)
        elif currstate == "start_dictation":
            self.on_listen_activate(None)
        elif currstate == "stop_dictation":
            self.on_stop_activate(None)
        elif currstate == "hold_dictation":
            pass
        elif currstate == "scroll_to_cursor":
            vi = self.window.get_active_view()
            vi.scroll_to_cursor()
        elif currstate == "goto_line":
            pass
        elif currstate == "undo":
            doc = self.window.get_active_document()
            if doc.can_undo():
                doc.begin_user_action()
                doc.undo()
                doc.end_user_action()
        elif currstate == "redo":
            doc = self.window.get_active_document()
            if doc.can_redo():
                doc.begin_user_action()
                doc.redo()
                doc.end_user_action()
        elif currstate == "cut_clipboard":
            vi = self.window.get_active_view()
            vi.cut_clipboard()
        elif currstate == "copy_clipboard":
            vi = self.window.get_active_view()
            vi.copy_clipboard()
        elif currstate == "paste_clipboard":
            vi = self.window.get_active_view()
            vi.paste_clipboard()
        elif currstate == "delete_selection":
            vi = self.window.get_active_view()
            vi.delete_selection()
        elif currstate == "select_all":
            vi = self.window.get_active_view()
            vi.select_all()
        elif currstate == "spacebar_input":
            self.inserttext(' ')
        elif currstate == "sentence_end":
            self.inserttext('. ')
        elif currstate == "delete_line":
            doc = self.window.get_active_document()
            doc.begin_user_action()
            ei = self.get_cursor_position(doc)
            si = self.get_cursor_position(doc)
            si.set_line(ei.get_line())
            ei.forward_to_line_end()
            doc.delete(si, ei)
            doc.end_user_action()
        elif currstate == "delete_sentence":
            doc = self.window.get_active_document()
            doc.begin_user_action()
            ei = self.get_cursor_position(doc)
            si = self.get_cursor_position(doc)
            if not si.starts_sentence():
                si.backward_sentence_start()
            si.backward_char()
            ei.forward_sentence_end()
            doc.delete(si, ei)
            doc.end_user_action()
        elif currstate == "delete_word":
            doc = self.window.get_active_document()
            doc.begin_user_action()
            ei = self.get_cursor_position(doc)
            si = self.get_cursor_position(doc)
            si.backward_word_start()
            si.backward_char()
            ei.forward_word_end()
            doc.delete(si, ei)
            doc.end_user_action()
        elif currstate == "clear_document":
            doc = self.window.get_active_document()
            if not doc:
                return
            doc.begin_user_action()
            doc.set_text('')
            doc.end_user_action()
        elif currstate == "new_document":
            self.window.create_tab(True)
        elif currstate == "save_document":
            doc = self.window.get_active_document()
            # checking if the document is a new document
            if doc.is_untitled():
                self.bottom_bar_text_set("First save should be Save As...")
                FileSaveAsDialog(self.window)
            else:
                doc.save(Gedit.DocumentSaveFlags(15))
        elif currstate == "save_as_document":
            FileSaveAsDialog(self.window)
        elif currstate == "close_document":
            if self.window.get_active_document.is_untouched():
                self.window.close_tab(self.window.get_active_tab())
            else:
                # to prevent data loss
                self.bottom_bar_text_set("You might wanna save the document before quitting.")
        elif currstate == "force_close_document":
            self.window.close_tab(self.window.get_active_tab())
        elif currstate == "error_state":
            logger.debug("Some Error ######")
        else:
            self.bottom_bar_text_set("Turned OFF")
        return

    def stop(self):
        """Stop Actions class."""
        del self.window
        del self.settings
        del self.bottom_bar_text_set

    def __del__(self):
        logger.debug("Actions DEL")
