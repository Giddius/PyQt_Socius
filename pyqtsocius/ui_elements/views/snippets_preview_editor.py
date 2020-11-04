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
from PyQt5.Qsci import QsciLexerPython, QsciScintilla
from pyqtsocius.init_userdata.user_data_setup import Support, request_support_objects
from gidqtutils.gidqtstuff import make_icons, create_new_font
# endregion[Imports]

__updated__ = '2020-11-01 22:01:17'

# region [AppUserData]
APPDATA, USER_CONFIG, SOLID_CONFIG = request_support_objects(Support.ALL)
# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class SnippetsPreviewEditor(QsciScintilla):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snippet_font = self.make_snippet_font()
        self.lexer = QsciLexerPython()
        self.setup()

    def setup(self):
        self.setFont(self.snippet_font)
        self.setMarginsFont(self.snippet_font)
        self.zoomIn()
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(0, 35)
        self.setReadOnly(True)
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.lexer.setDefaultFont(self.snippet_font)
        self.setLexer(self.lexer)

    @staticmethod
    def make_snippet_font():
        _name = USER_CONFIG.get('snippet_preview', 'default_font')
        _size = USER_CONFIG.getint('snippet_preview', 'default_font_size')
        _bold = USER_CONFIG.getboolean('snippet_preview', 'default_font_bold')
        return create_new_font(_name, _size, _bold)

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
