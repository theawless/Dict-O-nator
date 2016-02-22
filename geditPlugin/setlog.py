#!/usr/bin/python
# -*- coding: utf8 -*-

import logging
logger = logging.getLogger()
def setupLogger():
     logger.setLevel(logging.DEBUG)
     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
     fh = logging.FileHandler('.local/share/gedit/plugins/pluginlogfile.txt')
     fh.setLevel(logging.DEBUG)
     fh.setFormatter(formatter)
     logger.addHandler(fh)


     sh = logging.StreamHandler()
     sh.setLevel(logging.DEBUG)
     sh.setFormatter(formatter)
     logger.addHandler(sh)
     logger.debug('Setlog log setup done')

setupLogger()

