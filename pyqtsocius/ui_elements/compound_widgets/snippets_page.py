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
from functools import wraps, lru_cache, singledispatch, total_ordering
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
from PyQt5.Qsci import QsciLexerPython
# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)
from gidqtutils.gidqtstuff import make_icons, create_new_font
from pyqtsocius.ui_elements.compound_widgets.converted_files.Ui_snippets_tab_widget import Ui_SnippetsTab
from pyqtsocius.ui_elements.models.snippet_list_model import SnippetsListModel
from pyqtsocius.init_userdata.user_data_setup import Support, request_support_objects
# endregion[Imports]

__updated__ = '2020-10-30 06:49:46'

# region [AppUserData]

APPDATA, USER_CONFIG, SOLID_CONFIG = request_support_objects(Support.ALL)

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class SnippetsPageWidget(Ui_SnippetsTab, QWidget):
    _default_tab_name = "&Snippets"
    _default_icon_name = "cut"

    def __init__(self, *args, icon=None, name=None, **kwargs):
        super().__init__(*args, **kwargs)
        super().setupUi(self)
        self.icon_name = self._default_icon_name if icon is None else icon
        self.tab_name = self._default_tab_name if name is None else name
        self.icon = make_icons(f":/icons/{self.icon_name}", 50, 50) if '/' not in self.icon_name else make_icons(self.icon_name, 50, 50)
        self.snippet_model = SnippetsListModel()
        self.setup()
        self.actions()
        glog.class_initiated(self)

    def setup(self):
        self.snippets_tableView.setModel(self.snippet_model)
        header = self.snippets_tableView.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

        _snippet_font = self.snippet_font()
        self.snippet_preview_Scintilla.setFont(_snippet_font)
        self.snippet_preview_Scintilla.setMarginsFont(_snippet_font)
        self.snippet_preview_Scintilla.zoomIn()
        self.snippet_preview_Scintilla.setMarginLineNumbers(0, True)
        self.snippet_preview_Scintilla.setMarginWidth(0, 35)
        self.snippet_preview_Scintilla.setReadOnly(True)
        self.snippet_preview_Scintilla.setIndentationsUseTabs(False)
        self.snippet_preview_Scintilla.setIndentationWidth(4)
        self.lexer = QsciLexerPython()

        self.lexer.setDefaultFont(_snippet_font)
        self.snippet_preview_Scintilla.setLexer(self.lexer)

    @staticmethod
    def snippet_font():
        _name = USER_CONFIG.get('snippet_preview', 'default_font')
        _size = USER_CONFIG.getint('snippet_preview', 'default_font_size')
        _bold = USER_CONFIG.getboolean('snippet_preview', 'default_font_bold')
        return create_new_font(_name, _size, _bold)

    def actions(self):
        self.snippets_tableView.selectionModel().currentChanged.connect(self.show_snippet_preview)

    def show_snippet_preview(self, current_index, previous_index):
        self.snippet_preview_Scintilla.setText(self.snippet_model.get_full_snippet(current_index))


# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
