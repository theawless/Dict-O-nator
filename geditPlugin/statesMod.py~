#!/usr/bin/python3
import sys
sys.path.append('.local/share/gedit/plugins/')
# setting up logger
import setlog
logger=setlog.logger

cstate=''
#defining the states
states=["start", "stop","wait","spacebar","sentence_end","delete_line","delete_word","clear"]

def decideState(txt):
    #Deciding states
    if txt=='stop':
        cstate=states[1]
    elif txt=='wait':
        cstate=states[2]
    elif txt=='spacebar':
        cstate=states[3]
    elif txt=='end sentence':
        cstate=states[4]
    else:
        cstate=states[0]
    logger.debug("Decided state: " + cstate)
    return cstate

