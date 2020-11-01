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
from typing import Union, Iterable
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
from pyqtsocius.ui_elements.compound_widgets.converted_files.Ui_content_tab_widget import Ui_ContentTab
from pyqtsocius.utilities_and_vendored.widget_insert_items import combobox_insert_set
from pyqtsocius.ui_elements.models.widget_list_model import WidgetListModel
from pyqtsocius.ui_elements.misc_ui.widget_list_item_styler import WidgetItemStyleJson
from pyqtsocius.ui_elements.models.widget_signals_slots_functions_list_model import WidgetSignalsSlotsFunctionsListModel, Assignment
from pyqtsocius.init_userdata.user_data_setup import Support, request_support_objects
# endregion[Imports]

__updated__ = '2020-11-01 21:48:50'

# region [AppUserData]

APPDATA, USER_CONFIG, SOLID_CONFIG = request_support_objects(Support.ALL)

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


def create_font_from_config(section, prefix=None):
    font_name_key = 'font' if prefix is None else f'{prefix}_font'
    font_size_key = 'font_size' if prefix is None else f'{prefix}_font_size'
    font_bold_key = 'font_bold' if prefix is None else f'{prefix}_font_bold'
    font_name = USER_CONFIG.get(section, font_name_key)
    font_size = USER_CONFIG.getint(section, font_size_key)
    bold = USER_CONFIG.getboolean(section, font_bold_key)
    log.info("created new font, with name '%s', size '%s', bold '%s'", font_name, font_size, bold)
    return create_new_font(font_name, font_size, bold)


def create_new_filesystemwatcher(file_to_watch, signal_target, signal_type='file'):
    _fsw = QFileSystemWatcher()
    _fsw.addPath(file_to_watch)
    if signal_type == 'file':
        _fsw.fileChanged.connect(signal_target)
    elif signal_type == 'folder':
        _fsw.directoryChanged.connect(signal_target)
    log.info("created filewatcher to watch '%s'", file_to_watch)
    return _fsw


class ContentPageWidget(Ui_ContentTab, QWidget):
    """
    [summary]

    [extended_summary]

    Args:
        Ui_ContentTab ([type]): [description]
        QWidget ([type]): [description]
    """
    _default_tab_name = "&Content"
    _default_icon_name = "checklist"

    def __init__(self, *args, icon=None, name=None, **kwargs):
        super().__init__(*args, **kwargs)
        super().setupUi(self)
        self.icon_name = self._default_icon_name if icon is None else icon
        self.tab_name = self._default_tab_name if name is None else name
        self.icon = make_icons(f":/icons/{self.icon_name}", 50, 50) if '/' not in self.icon_name else make_icons(self.icon_name, 50, 50)
        self.widget_styler = WidgetItemStyleJson()
        self.widget_list_model = WidgetListModel(self.widget_styler)
        self.styler_filesystemwatcher = create_new_filesystemwatcher(self.widget_styler.data_file, self.widget_list_model.pickup_data)
        self.completer_widget = None
        self.completer_name = None
        self.setup()
        self.actions()

    def setup(self):
        self.setup_comboboxes()
        self.widget_listView.setModel(self.widget_list_model)
        self.selected_widget_lineEdit.setReadOnly(True)
        self.functions_slots_listView.setModel(WidgetSignalsSlotsFunctionsListModel(Assignment.FunctionsSlots))
        self.signals_listView.setModel(WidgetSignalsSlotsFunctionsListModel(Assignment.Signals))
        self.create_fonts()

    def create_fonts(self):
        self.functions_slots_listView.setFont(create_font_from_config('functions_slots_list_model'))

        self.signals_listView.setFont(create_font_from_config('signal_list_model'))

    def actions(self):

        _buttons = {self.sort_widgets_pushButton: [('pressed', self.sort_widget_list)],
                    self.clear_filter_input_pushButton: [('pressed', self.clear_filter)],
                    self.filter_by_widget_radioButton: [('toggled', self.switch_completer)],
                    self.filter_by_name_radioButton: [('toggled', self.switch_completer)]}

        _views = {self.widget_listView: [('doubleClicked', self.copy_from_widget_list)],
                  self.widget_listView.selectionModel(): [('currentChanged', self.item_selected_display_changes)],

                  self.functions_slots_listView: [('doubleClicked', self.copy_from_functions_slots)],
                  self.signals_listView: [('doubleClicked', self.copy_from_signals)]}

        _other = {self.filter_widget_comboBox: [('currentIndexChanged', self.filter_widget_list)],
                  self.filter_input_lineEdit: [('textChanged', self.filter_by_input)]}

        _action_listdict = [_buttons, _views, _other]

        for _action_dict in _action_listdict:
            for key, action_tuple in _action_dict.items():
                for trigger, target in action_tuple:
                    getattr(key, trigger).connect(target)

    def copy_from_widget_list(self, index):
        log.debug('function was trigger, for row %s', index.row())
        self.widget_list_model.double_clicked(index)

    def copy_from_signals(self, index):
        log.debug('function was trigger, for row %s', index.row())
        _widget = self.widget_list_model.content[self.widget_listView.currentIndex().row()].name
        self.signals_listView.model().double_clicked(index, _widget)

    def copy_from_functions_slots(self, index):
        log.debug('function was trigger, for row %s', index.row())
        _widget = self.widget_list_model.content[self.widget_listView.currentIndex().row()].name
        self.functions_slots_listView.model().double_clicked(index, _widget)

    def item_selected_display_changes(self, index, previous_index):
        log.debug('previous index was %s', previous_index.row())
        _item = self.widget_list_model.content[index.row()]
        _widget_class = _item.widget_class
        self.selected_widget_lineEdit.setText(_widget_class)
        _signals, _functions, _slots = self.widget_list_model.get_signals_functions_slots(_item)
        self.functions_slots_listView.model().insert_data(_functions + _slots)
        self.signals_listView.model().insert_data(_signals)

    def setup_comboboxes(self):
        _comboboxes = {self.sort_direction_comboBox: (['ascending', 'descending'], 'ascending'),
                       self.sort_by_comboBox: (['Name', 'Widgets'], 'Name'),
                       self.filter_widget_comboBox: (['--no filter--', 'only_important'], '--no filter--')}
        for key, value in _comboboxes.items():
            combobox_insert_set(key, value[0], value[1])

    def display_data(self, file, file_reader):
        self.widget_list_model.assign_dataprovider(data_provider=file_reader)
        create_new_filesystemwatcher(file, self.widget_list_model.pickup_data)
        self.widget_list_model.pickup_data()
        self.file_name_label.setText(self.widget_list_model.current_top_parent)
        self.widget_listView.update()
        self.filter_by_widget_radioButton.setChecked(True)
        self.setup_completer()
        self.filter_input_lineEdit.setCompleter(self.completer_widget)
        self.setEnabled(True)

    def setup_completer(self):
        self.completer_widget = QCompleter(self.widget_list_model.list_of_widget_classes())
        self.completer_name = QCompleter(self.widget_list_model.list_of_names())
        for completer in [self.completer_widget, self.completer_name]:
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchContains)
            completer.setCompletionMode(QCompleter.PopupCompletion)

    def switch_completer(self):
        self.setup_completer()
        if self.filter_by_name_radioButton.isChecked():
            self.filter_input_lineEdit.setCompleter(self.completer_name)

        elif self.filter_by_widget_radioButton.isChecked():
            self.filter_input_lineEdit.setCompleter(self.completer_widget)

    def filter_by_input(self, text):
        _attribute = 'name' if self.filter_by_name_radioButton.isChecked() else 'widget_class'
        self.widget_list_model.filter_by_other(_attribute, text)

    def filter_widget_list(self):
        _filter_setting = self.filter_widget_comboBox.currentText()
        if _filter_setting == '--no filter--':
            self.widget_list_model.clear_filter()
        elif _filter_setting == 'only_important':
            self.widget_list_model.filter_important()

    def clear_filter(self):
        self.filter_input_lineEdit.clear()
        self.widget_list_model.clear_filter()

    def sort_widget_list(self):
        _direction = self.sort_direction_comboBox.currentText()
        _sort_by = self.sort_by_comboBox.currentIndex()
        _order = Qt.AscendingOrder if _direction == 'ascending' else Qt.DescendingOrder
        self.widget_list_model.sort(_sort_by, _order)

    def debug(self, button):
        _index = self.widget_listView.currentIndex()
        _icon = self.widget_list_model.content[_index.row()].icon
        button.setIcon(_icon)
# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
