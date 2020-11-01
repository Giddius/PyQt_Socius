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
import pyperclip
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
from gidviewmodels.gidmodels import BasicTableModel
from gidviewmodels.giditems import standarditem_subclasses
from pyqtsocius.init_userdata.user_data_setup import Support, request_support_objects

# endregion[Imports]

__updated__ = '2020-10-31 06:52:01'

# region [AppUserData]

APPDATA, USER_CONFIG, SOLID_CONFIG = request_support_objects(Support.ALL)

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class SnippetsListModel(QAbstractTableModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snippetfile = APPDATA['snippets.json']
        self.raw_content = {}
        self.get_raw_content()
        self.content = []
        self.transform_raw_content()
        self.header = ['Name', 'Description']

    def update_everything(self):
        self.save_json()
        self.beginResetModel()
        self.get_raw_content()
        self.transform_raw_content()
        self.endResetModel()

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role in [Qt.DisplayRole]:
            return self.content[index.row()][index.column()]
        elif role == Qt.ToolTipRole:
            return self.content[index.row()][1]
        elif role == Qt.BackgroundRole and USER_CONFIG.getboolean(str(self), 'use_background_color') is True:
            _col = self.content[index.row()][3] if self.content[index.row()][3] != '' else [100, 175, 100, 100]
            return QBrush(QColor.fromHsv(*_col))
        elif role == Qt.DecorationRole and USER_CONFIG.getboolean(str(self), 'use_icons') is True and index.column() == 0:
            return make_icons(':/icons/' + self.content[index.row()][2], 25, 25)

    def transform_raw_content(self):
        _out = []
        if len(self.raw_content) != 0:
            for key, value in self.raw_content.items():
                _out.append((key.title(), value.get('description', 'missing'), value.get('icon', 'placeholder_icon'), value.get('color', ''), value.get('data', 'no Data')))
        self.content = _out

    def get_raw_content(self):
        if os.path.isfile(self.snippetfile) is False:
            self.save_json()
        self.raw_content = loadjson(self.snippetfile)

    def save_json(self):
        writejson(self.raw_content, self.snippetfile)

    def get_full_snippet(self, index):
        _name = self.content[index.row()][0]
        return f'# ########## {_name} ########## #\n\n' + self.content[index.row()][4]

    def rowCount(self, index):
        return len(self.content)

    def columnCount(self, parent):
        return len(self.header)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def double_clicked(self, index):
        _data = self.get_full_snippet(index)
        pyperclip.copy(_data)

    def __setitem__(self, key, value):
        log.debug('snippet adding started with key %s and value %s', key, str(value))
        self.raw_content[key] = {'description': value[0], 'icon': value[1], 'color': value[2], 'data': value[3]}
        self.update_everything()

    def __delitem__(self, key):
        del self.raw_content[key]
        self.update_everything()

    def __str__(self):
        return 'snippets_list_model'

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
