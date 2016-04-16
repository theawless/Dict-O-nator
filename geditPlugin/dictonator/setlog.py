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

"""Sets up the logger."""

import logging
import os

logger = logging.getLogger('dictonator')
GEDIT_PLUGIN_PATH = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(GEDIT_PLUGIN_PATH + '/.logs'):
    os.makedirs(GEDIT_PLUGIN_PATH + '/.logs')

LOG_DIR_PATH = GEDIT_PLUGIN_PATH + "/.logs/"


def _setup_logger():
    # setting format of log
    formatter = logging.Formatter('%(threadName)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    # file location
    debug_log = LOG_DIR_PATH + 'log.txt'

    # adding handler for console logs
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # adding handler for file logs
    fh = logging.FileHandler(debug_log)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.debug('Setlog logger setup done')


_setup_logger()
