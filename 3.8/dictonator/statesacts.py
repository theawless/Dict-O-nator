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


"""Defines the dictionary of command words and implement decide function"""
# setting up logger
from enum import Enum

from dictonator.setlog import logger


# defining valid states for dictonator
class DictonatorStates(Enum):
    started = 0
    preparing = 1
    prepared = 2
    stopping = 3
    stopped = 4
    recognising = 5
    error = 6

    recognised = 7
    fatal_error = 8


class DictonatorActions:
    # defining the actions

    actions = dict(start_dictation={"start dictation", "start dictator", "start speaking"},
                   stop_dictation={"stop dictation", "stop dictator", "stop dictation"},
                   hold_dictation={"hold dictation", "hold dictator", "wait dictation"},
                   scroll_to_cursor={"scroll to cursor"},
                   goto_line={"go to line"},
                   undo={"undo", "do undo"},
                   redo={"redo", "do redo"},
                   cut_clipboard={"cut clipboard", "cut clip board", "cut selection", "cut to clipboard"},
                   copy_clipboard={"copy clipboard", "copy to clipboard", "copy selection", "copy clip board"},
                   paste_clipboard={"paste clipboard", "paste clipboard", "paste from clipboard"},
                   delete_selection={"delete selection", "delete selected text"},
                   select_all={"select all", "select all text"},
                   comma_input={"put comma", },
                   question_mark_input={"put question mark", "question mark"},
                   exclamation_mark_input={"put exclamation mark", "exclamation mark"},
                   spacebar_input={"spacebar", "input spacebar", "word end", "end word"},
                   sentence_end={"sentence end", "close sentence", "end sentence", "full stop", "put period"},
                   line_end={"end line", "close line", "input enter", "put enter", "next line"},
                   delete_line={"delete line", "delete last line"},
                   delete_word={"delete word", "delete last word"},
                   delete_sentence={"delete sentence", "delete this sentence", "delete current sentence", },
                   clear_document={"clear document", "empty document", "clear file", "empty file"},
                   new_document={"new document", "new file"},
                   save_document={"save document", "save file"},
                   save_as_document={"save as document", "save document as", "save as file", "save file as"},
                   close_document={"close document", "close file"},
                   force_close_document={"force close document", "force close file"},
                   exit={"exit editor", "exit gedit", "editor exit", "gedit exit", "close editor", "close gedit",
                         "quit editor"})

    @staticmethod
    def decide_action(txt: str):
        # Deciding actions from the dictionary
        cact = "continue_dictation"
        for act in DictonatorActions.actions:
            if txt.lower() in DictonatorActions.actions[act]:
                cact = act
                logger.debug(cact)
                return cact
        logger.debug(cact)
        return cact
