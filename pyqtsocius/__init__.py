"""helper to create gui with QtDesigner files and much more"""

__version__ = '0.1'

from pyqtsocius.init_userdata.user_data_setup import Support, request_support_objects
import gidlogger as glog
import logging
import os
import pyqtsocius.ui_elements.pyqt_sorter_ressources_rc
APPDATA, USER_CONFIG, SOLID_CONFIG = request_support_objects(Support.ALL)
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
_log_file = glog.log_folderer("__main__", in_log_folder_directory=THIS_FILE_DIR)
log = glog.main_logger(_log_file, USER_CONFIG.get('general_settings', 'logging_level'))
log.info(glog.NEWRUN())
if USER_CONFIG.getboolean('general_settings', 'use_logging') is False:
    logging.disable(logging.CRITICAL)
