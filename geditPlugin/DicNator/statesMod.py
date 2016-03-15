# !/usr/bin/python3

# setting up logger
import DicNator.setlog as setlog

logger = setlog.logger
logger.debug("Started States Mod")
# defining the states
states = ["start_dictation", "stop_dictation", "wait", "spacebar", "sentence_end", "delete_line", "delete_word",
          "clear", "new_document", "save_document", "close_document", "save_document", "error"]


def decide_state(txt):
    # Deciding states
    if txt == 'stop listening':
        cstate = states[1]
    elif txt == 'wait':
        cstate = states[2]
    elif txt == 'spacebar':
        cstate = states[3]
    elif txt == 'end sentence':
        cstate = states[4]
    elif txt == '######':
        cstate = states[12]
    else:
        cstate = states[0]
    logger.debug("Decided state: " + cstate)
    return cstate
