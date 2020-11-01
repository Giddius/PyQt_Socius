# region [Imports]

# * Standard Library Imports -->
import gc
import os
import re
import sys
import json
import lzma
import time
import queue
import logging
import platform
import subprocess
from enum import Enum, Flag, auto
from time import sleep
from pprint import pprint, pformat
from typing import Union
from datetime import tzinfo, datetime, timezone, timedelta
from functools import wraps, lru_cache, singledispatch, total_ordering, partial
from contextlib import contextmanager
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# * Third Party Imports -->
# import requests
# import pyperclip
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# from github import Github, GithubException
# from jinja2 import BaseLoader, Environment
# from natsort import natsorted
# from fuzzywuzzy import fuzz, process

# * PyQt5 Imports -->
from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QCursor, QPixmap, QStandardItem, QRegExpValidator
from PyQt5.QtCore import (Qt, QRect, QSize, QObject, QRegExp, QThread, QMetaObject, QCoreApplication,
                          QFileSystemWatcher, QPropertyAnimation, QAbstractTableModel, pyqtSlot, pyqtSignal)
from PyQt5.QtWidgets import (QMenu, QFrame, QLabel, QDialog, QLayout, QWidget, QWizard, QMenuBar, QSpinBox, QCheckBox, QComboBox,
                             QGroupBox, QLineEdit, QListView, QCompleter, QStatusBar, QTableView, QTabWidget, QDockWidget, QFileDialog,
                             QFormLayout, QGridLayout, QHBoxLayout, QHeaderView, QListWidget, QMainWindow, QMessageBox, QPushButton,
                             QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWizardPage, QApplication, QButtonGroup, QRadioButton,
                             QFontComboBox, QStackedWidget, QListWidgetItem, QTreeWidgetItem, QDialogButtonBox, QAbstractItemView,
                             QCommandLinkButton, QAbstractScrollArea, QGraphicsOpacityEffect, QTreeWidgetItemIterator, QAction, QSystemTrayIcon)
# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)
from gidqtutils.gidqtstuff import make_icons, create_new_font
from pyqtsocius.init_userdata.user_data_setup import Support, request_support_objects
from pyqtsocius.non_ui_elements.data import DocType
from pyqtsocius.utilities_and_vendored.exceptions import FeatureNotYetImplemented
import pyqtsocius.ui_elements.pyqt_sorter_ressources_rc
# endregion[Imports]

__updated__ = '2020-11-01 20:23:37'

# region [AppUserData]

APPDATA, USER_CONFIG, SOLID_CONFIG = request_support_objects(Support.ALL)

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class WidgetItemStyleJson:

    def __init__(self, widget_style_data_file='widget_dict.json'):
        self.data_file = APPDATA[widget_style_data_file]
        self.content = None
        self.read()

    def read(self):
        self.content = loadjson(self.data_file)

    def save(self):
        writejson(self.content, self.data_file)
        self.read()

    @staticmethod
    def _check_make_icons(icon: str):
        if icon == '':
            icon = "placeholder_icon"
        if '/' in icon:
            _out = make_icons(icon, 50, 50)
        else:
            _out = make_icons(f':/icons/{icon}', 50, 50)

        return _out

    def process_widget(self, widget_tuple):
        _widget_dict = self.content.get(widget_tuple.widget_class, None)
        if _widget_dict is None:
            _color = ''
            _icon = ''
            _is_important = False
        else:
            _color = _widget_dict.get('color')
            _icon = _widget_dict.get('icon')
            log.debug('icon found as %s', _icon)
            _is_important = _widget_dict.get('important')

        _color = USER_CONFIG.getlist('widget_list_model', 'default_background_color') if _color == '' else _color
        _icon = self._check_make_icons(_icon)
        _is_important = False if _is_important == '' else _is_important
        return (QColor.fromHsv(*map(int, _color)), _icon, _is_important)

    def demand_widget_documentation(self, item, documentation_typ: DocType):
        _documentation = self.content.get(item.widget_class, {}).get('description', '')
        if documentation_typ is DocType.Html:
            return _documentation
        else:
            raise FeatureNotYetImplemented("documentation styles other than Html")

    def demand_widget_documentation_url(self, item):
        return self.content.get(item.widget_class, {}).get('documentation_link', '')

    def demand_signals_functions_slots(self, item):
        _item_dict = self.content.get(item.widget_class, {})
        _signals = _item_dict.get('signals', [])
        _functions = _item_dict.get('functions', [])
        _slots = _item_dict.get('slots', [])
        return _signals, _functions, _slots

    def save_new_color(self, item, color: QColor):
        _color_components = color.getHsv()
        if item.widget_class not in self.content:
            self.content[item.widget_class] = {"attributes": [],
                                               "color": "",
                                               "description": "",
                                               "documentation_link": "",
                                               "functions": [],
                                               "icon": "placeholder_icon",
                                               "important": True,
                                               "notes": "",
                                               "signals": [],
                                               "slots": []}
        self.content[item.widget_class]['color'] = _color_components
        self.save()


# region[Main_Exec]
if __name__ == '__main__':
    pass

# endregion[Main_Exec]
