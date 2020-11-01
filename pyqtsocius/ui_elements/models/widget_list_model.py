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
from pyqtsocius.init_userdata.user_data_setup import Support, request_support_objects
from pyqtsocius.non_ui_elements.data import DocType
# endregion[Imports]

__updated__ = '2020-11-01 20:31:24'

# region [AppUserData]
APPDATA, USER_CONFIG, SOLID_CONFIG = request_support_objects(Support.ALL)
# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class WidgetListModel(QAbstractTableModel):
    content_item = namedtuple('ContentItem', ['name', 'widget_class', 'color', 'icon', 'is_important'])

    def __init__(self, widget_styler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_styler = widget_styler
        self.data_provider = None
        self.raw_content = None
        self.unfiltered_content = []
        self.content = []
        self.current_file = None
        self.current_top_parent = None

        self.header = ['Name', 'QWidget_type']

    def assign_dataprovider(self, data_provider):
        self.data_provider = data_provider
        self.raw_content = self.data_provider.collect_data
        self.pickup_data()

    def pickup_data(self):
        self.layoutAboutToBeChanged.emit()
        log.debug("starting data pickup")
        self.unfiltered_content = []
        self.content = []
        for index, widget_data in enumerate(self.raw_content()):
            if index == 0:
                self.current_file = widget_data.file_name
                self.current_top_parent = widget_data.main_parent_class_name
            _name = widget_data.name
            _class = widget_data.widget_class
            _color, _icon, _is_important = self.widget_styler.process_widget(widget_data)

            _item = self.content_item(_name, _class, _color, _icon, _is_important)
            self.unfiltered_content.append(_item)
            self.content = self.unfiltered_content
            self.layoutChanged.emit()

    def data(self, index, role):

        if not index.isValid():
            return None
        elif role in [Qt.DisplayRole]:
            return self.content[index.row()].name
        elif role == Qt.ToolTipRole:
            return self.content[index.row()].widget_class
        elif role == Qt.BackgroundRole and USER_CONFIG.getboolean(str(self), 'use_background_color') is True:
            return QBrush(self.content[index.row()].color)
        elif role == Qt.ForegroundRole and USER_CONFIG.getboolean(str(self), 'use_font_color') is True:
            _color = USER_CONFIG.get(str(self), 'font_color')
            return QColor(_color)
        elif role == Qt.DecorationRole:  # and USER_CONFIG.getboolean(str(self), 'use_icons') is True:

            return self.content[index.row()].icon

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def rowCount(self, index):
        return len(self.content)

    def columnCount(self, parent):
        return len(self.header)

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self.content.sort(key=lambda x: x[column])
        if order == Qt.DescendingOrder:
            self.content.reverse()
        self.layoutChanged.emit()

    def extra_sorting(self, mode):
        self.layoutAboutToBeChanged.emit()
        if mode[1] == 'name':
            self.content.sort(key=lambda x: x.name)
        elif mode[1] == 'widgets':
            self.content.sort(key=lambda x: x.widget_class)
        if mode[0] == 'descending':
            self.content = list(reversed(self.content))

        self.layoutChanged.emit()

    def filter_important(self):
        self.layoutAboutToBeChanged.emit()
        self.content = []
        for item in self.unfiltered_content:
            if item.is_important is True:
                self.content.append(item)
        self.layoutChanged.emit()

    def clear_filter(self):
        self.layoutAboutToBeChanged.emit()
        self.content = self.unfiltered_content
        self.layoutChanged.emit()

    def filter_by_other(self, attribute, filter_phrase):
        self.layoutAboutToBeChanged.emit()
        self.content = []
        if filter_phrase == '':
            self.content = self.unfiltered_content
        else:
            for item in self.unfiltered_content:
                if filter_phrase.casefold() in getattr(item, attribute).casefold():
                    self.content.append(item)
        self.layoutChanged.emit()

    def double_clicked(self, index):
        log.debug('function was trigger, for row %s', index.row())
        _data = ''

        if USER_CONFIG.get(str(self), 'on_double_click') == 'copy':
            _data = 'self.' + self.content[index.row()].name
        pyperclip.copy(_data)

    def get_description_html(self, item):
        return self.widget_styler.demand_widget_documentation(item, DocType.Html)

    def get_url(self, item):
        return self.widget_styler.demand_widget_documentation_url(item)

    def get_signals_functions_slots(self, item):
        return self.widget_styler.demand_signals_functions_slots(item)

    def change_background_color(self, index, color: QColor):
        item = self.content[index.row()]
        self.widget_styler.save_new_color(item, color)
        self.beginResetModel()
        self.pickup_data()
        self.endResetModel()

    def list_of_names(self):
        return [item.name for item in self.content]

    def list_of_widget_classes(self):
        _out = []
        for item in self.content:
            if item.widget_class not in _out:
                _out.append(item.widget_class)
        log.debug("list of widget_class names: %s", str(_out))
        return _out

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return 'widget_list_model'

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
