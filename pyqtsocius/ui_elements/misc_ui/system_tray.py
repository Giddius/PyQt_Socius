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
import requests
import pyperclip
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from jinja2 import BaseLoader, Environment
from natsort import natsorted
from fuzzywuzzy import fuzz, process


# * PyQt5 Imports -->
from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QCursor, QPixmap, QStandardItem, QRegExpValidator
from PyQt5.QtCore import (Qt, QRect, QSize, QObject, QRegExp, QThread, QMetaObject, QCoreApplication,
                          QFileSystemWatcher, QPropertyAnimation, QAbstractTableModel, pyqtSlot, pyqtSignal)
from PyQt5.QtWidgets import (QMenu, QFrame, QLabel, QDialog, QLayout, QWidget, QWizard, QMenuBar, QSpinBox, QCheckBox, QComboBox,
                             QGroupBox, QLineEdit, QListView, QCompleter, QStatusBar, QTableView, QTabWidget, QDockWidget, QFileDialog,
                             QFormLayout, QGridLayout, QHBoxLayout, QHeaderView, QListWidget, QMainWindow, QMessageBox, QPushButton,
                             QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWizardPage, QApplication, QButtonGroup, QRadioButton,
                             QFontComboBox, QStackedWidget, QListWidgetItem, QTreeWidgetItem, QDialogButtonBox, QAbstractItemView,
                             QCommandLinkButton, QAbstractScrollArea, QGraphicsOpacityEffect, QTreeWidgetItemIterator, QSystemTrayIcon, QAction)
# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)
from gidqtutils.gidgets import make_icons
import pyqtsocius.ui_elements.pyqt_sorter_ressources_rc

# endregion[Imports]

__updated__ = '2020-10-31 06:41:58'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class SystemTray(QSystemTrayIcon):
    def __init__(self, window, in_app, *args, **kwargs):
        super().__init__(* args, **kwargs)
        self.window = window
        self.app = in_app
        self.icon = None
        self.setup_menu()

    def setup_menu(self):
        _actions = {'Show': self.window.show,
                    'Hide': self.window.hide,
                    'Close': self.window.close}
        self.systray_menu = QMenu(self.window)
        for _name, _target in _actions.items():
            _action = QAction(_name, self.systray_menu)
            _action.triggered.connect(_target)
            if _name != 'Close':
                _action.triggered.connect(partial(self.hide_option, _name))
            if _name == 'Show':
                _action.setEnabled(False)
                _action.triggered.connect(self.window.activateWindow)
            self.systray_menu.addAction(_action)

        self.setContextMenu(self.systray_menu)

    def hide_option(self, name):
        for _action in self.systray_menu.actions():
            if _action.text() == name:
                _action.setEnabled(False)
            else:
                _action.setEnabled(True)

    def new_icon(self, icon):
        self.icon = make_icons(f':/icons/{icon}', 100, 100)
        self.setIcon(self.icon)

    def show_hide_message(self, title, message, icon=None):
        _icon = self.icon if icon is None else make_icons(f':/icons/{icon}', 100, 100)
        self.showMessage(title, message, _icon, 500)
