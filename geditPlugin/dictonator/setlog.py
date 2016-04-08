"""Sets up the logger."""

import logging

logger = logging.getLogger('dictonator')
path = '.local/share/gedit/plugins/dictonator/logs/'


def _setup_logger():
    # setting format of log
    formatter = logging.Formatter('%(threadName)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    # file location
    debug_log = path + 'log.txt'

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
