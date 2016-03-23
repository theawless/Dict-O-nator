# !/usr/bin/python3

# setting up logger
import DicNator.setlog as setlog

logger = setlog.logger
# logger.debug("Started States Mod")
# defining the states
states = {"start_dictation": {"start dictation", "start dictator", "start speaking"},
          "stop_dictation": {"stop dictation", "stop dictator", "stop dictation"},
          "hold_dictation": {"hold dictation", "hold dictator", "wait dictation"},

          "scroll_to_cursor": {"scroll to cursor"},
          "goto_line": {"go to line"},
          "undo": {"undo", "do undo"},
          "redo": {"redo", "do redo"},
          "cut_clipboard": {"cut clipboard", "cut to clipboard"},
          "copy_clipboard": {"copy clipboard", "copy to clipboard"},
          "paste_clipboard": {"paste clipboard", "paste from clipboard"},
          "delete_selection": {"delete selection", "delete selected text"},
          "select_all": {"select all", "select all text"},

          "spacebar_input": {"spacebar", "input spacebar", "word end", "end word"},
          "sentence_end": {"sentence end", "end sentence", "full stop"},

          "delete_line": {"delete line", "delete last line"},
          "delete_word": {"delete word", "delete last word"},
          "delete_sentence": {"delete sentence", "delete this sentence", "delete current sentence", },

          "delete_line2": {""},
          "delete_word2": {""},
          "delete_sentence2": {""},

          "clear_document": {"clear document", "empty document", "clear file", "empty file"},
          "new_document": {"new document", "new file"},
          "save_document": {"save document", "save file"},
          "Save_as_document": {"save as document", "save document as", "save as file", "save file as"},
          "close_document": {"close document", "close file"},
          "force_close_document": {"force close document", "force close file"},

          "error_state": {"######"},
          }


def decide_state(txt):
    # Deciding states
    cstate = "start_dictation"
    for state in states:
        if txt in states[state]:
            cstate = state
            logger.debug(cstate)
            return cstate
    logger.debug(cstate)
    return cstate
