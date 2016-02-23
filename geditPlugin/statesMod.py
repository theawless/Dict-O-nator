#!/usr/bin/python3
import sys
sys.path.append('.local/share/gedit/plugins/')
import setlog
logger=setlog.logger
cstate=''
states=["start", "stop","wait"]
def decideState(txt):
    #logger.debug("Deciding state now")
    if txt=='stop':
        cstate=states[1]
    elif txt=='wait':
        cstate=states[2]
    else:
        cstate=states[0]
    logger.debug("Decided state: " + cstate)
    return cstate

