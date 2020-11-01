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
import xml.etree.ElementTree as ET
# from dotenv import load_dotenv
# from github import Github, GithubException
# from jinja2 import Environment, BaseLoader

# * PyQt5 Imports -->
from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QCursor, QPixmap, QStandardItem, QRegExpValidator
from PyQt5.QtCore import (Qt, QRect, QSize, QObject, QRegExp, QThread, QMetaObject, QCoreApplication,
                          QFileSystemWatcher, QPropertyAnimation, QAbstractTableModel, pyqtSlot, pyqtSignal)
from PyQt5.QtWidgets import (QMenu, QFrame, QLabel, QDialog, QLayout, QWidget, QWizard, QMenuBar, QSpinBox, QCheckBox, QComboBox,
                             QGroupBox, QLineEdit, QListView, QCompleter, QStatusBar, QTableView, QTabWidget, QDockWidget, QFileDialog,
                             QFormLayout, QGridLayout, QHBoxLayout, QHeaderView, QListWidget, QMainWindow, QMessageBox, QPushButton,
                             QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWizardPage, QApplication, QButtonGroup, QRadioButton,
                             QFontComboBox, QStackedWidget, QListWidgetItem, QTreeWidgetItem, QDialogButtonBox, QAbstractItemView,
                             QCommandLinkButton, QAbstractScrollArea, QGraphicsOpacityEffect, QTreeWidgetItemIterator)
# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file, splitoff)

from pyqtsocius.utilities_and_vendored.exceptions import WrongInputFileTypeError
# endregion[Imports]

__updated__ = '2020-10-30 07:19:45'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class DesignerFileReader:
    WidgetTuple = namedtuple('WidgetTuple', ['name', 'widget_class', 'main_parent_class_name', 'file_name'])

    def __init__(self, in_file: str):
        self.file = in_file
        if not self.file.endswith('.ui'):
            raise WrongInputFileTypeError(self.file, 'ui')
        self.classname = ''
        self.widgets = []

    def process_content(self):
        _xml_content = readit(self.file)
        xml_tree = ET.ElementTree(ET.fromstring(_xml_content))
        self.classname = 'Ui_' + xml_tree.find('class').text
        for element in xml_tree.iter('widget'):
            _widget = element.attrib.get('class')
            _name = element.attrib.get('name')
            self.widgets.append(self.WidgetTuple(_name, _widget, self.classname, pathmaker(self.file)))

    def collect_data(self):
        self.widgets = []
        self.process_content()
        return self.widgets


if __name__ == '__main__':
    pass
