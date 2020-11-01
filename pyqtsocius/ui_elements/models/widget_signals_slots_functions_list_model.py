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

from pyqtsocius.init_userdata.user_data_setup import Support, request_support_objects
from gidqtutils.gidqtstuff import make_icons
import pyqtsocius.ui_elements.pyqt_sorter_ressources_rc
# endregion[Imports]

__updated__ = '2020-11-01 02:16:28'

# region [AppUserData]

APPDATA, USER_CONFIG, SOLID_CONFIG = request_support_objects(Support.ALL)

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class Assignment(Enum):
    FunctionsSlots = 'functions_slots'
    Signals = 'signal'

    def __str__(self):
        return self.value + "_list_model"


class WidgetSignalsSlotsFunctionsListModel(QAbstractTableModel):

    def __init__(self, assignment: Assignment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignment = assignment
        self.content = []
        self.header = ['Name']
        self.role_switch = {Qt.DisplayRole: self.display_data,
                            Qt.EditRole: self.display_data,
                            Qt.DecorationRole: self.icon_data,
                            Qt.BackgroundRole: self.background_color_data,
                            Qt.ForegroundRole: self.font_color_data,
                            Qt.SizeHintRole: self.size_hint_data,
                            Qt.ToolTipRole: self.tool_tip_data,
                            Qt.StatusTipRole: self.status_tip_data}

    def data(self, index, role):
        if index.isValid() is False:
            return None
        elif role in self.role_switch:
            return self.role_switch.get(role)(index)
        else:
            return None

    def insert_data(self, data):
        self.layoutAboutToBeChanged.emit()
        self.content = data
        self.layoutChanged.emit()

    def display_data(self, index):
        return self.content[index.row()]

    def icon_data(self, index):
        return None

    def background_color_data(self, index):
        if USER_CONFIG.getboolean(str(self.assignment), 'use_background_color') is True:
            _hsv_colors = USER_CONFIG.getlist(str(self.assignment), 'background_color_hsv')
            _hsv_colors = map(int, _hsv_colors)
            return QColor().fromHsv(*_hsv_colors)
        else:
            return QColor().setNamedColor('white')

    def font_color_data(self, index):
        return QColor().setNamedColor(USER_CONFIG.get(str(self.assignment), 'font_color'))

    def size_hint_data(self, index):
        return None

    def tool_tip_data(self, index):
        return None

    def status_tip_data(self, index):
        return None

    def rowCount(self, index):
        return len(self.content)

    def columnCount(self, parent):
        return len(self.header)

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def double_clicked(self, index, widget):
        _data = self.content[index.row()]

        if USER_CONFIG.get(str(self.assignment), 'on_double_click') == 'copy':
            if self.assignment is Assignment.FunctionsSlots:
                _data = f'self.{widget}.{_data}()'
            elif self.assignment is Assignment.Signals:
                _data = f'self.{widget}.{_data}.connect()'
        pyperclip.copy(_data)

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
