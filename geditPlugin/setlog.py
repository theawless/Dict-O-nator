#!/usr/bin/python3

import logging
logger = logging.getLogger()

def setupLogger():

    #setting format of log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    #file location
    debug_log='.local/share/gedit/plugins/pluginlogfile.txt'
    
    #adding handler for console logs
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    
    #adding handler for file logs
    fh = logging.FileHandler(debug_log)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    logger.debug('SETLOG logger setup done')
   
setupLogger()

