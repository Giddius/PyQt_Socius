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
from dotenv import load_dotenv
import requests
from jinja2 import Environment, BaseLoader
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
from natsort import natsorted

# * PyQt5 Imports -->
from PyQt5.QtGui import QFont, QIcon, QBrush, QColor, QCursor, QPixmap, QStandardItem, QRegExpValidator, QFontInfo, QFontDatabase
from PyQt5.QtCore import (QEvent, Qt, QRect, QSize, QObject, QRegExp, QThread, QMetaObject, QCoreApplication,
                          QFileSystemWatcher, QPropertyAnimation, QAbstractTableModel, pyqtSlot, pyqtSignal)
from PyQt5.QtWidgets import (QMenu, QFrame, QLabel, QDialog, QLayout, QWidget, QWizard, QMenuBar, QSpinBox, QCheckBox, QComboBox,
                             QGroupBox, QLineEdit, QListView, QCompleter, QStatusBar, QTableView, QTabWidget, QDockWidget, QFileDialog,
                             QFormLayout, QGridLayout, QHBoxLayout, QHeaderView, QListWidget, QMainWindow, QMessageBox, QPushButton,
                             QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout, QWizardPage, QApplication, QButtonGroup, QRadioButton,
                             QFontComboBox, QStackedWidget, QListWidgetItem, QTreeWidgetItem, QDialogButtonBox, QAbstractItemView,
                             QCommandLinkButton, QAbstractScrollArea, QGraphicsOpacityEffect, QTreeWidgetItemIterator, QGraphicsDropShadowEffect, QAction)
# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import (QuickFile, readit, clearit, readbin, writeit, loadjson, pickleit, writebin, pathmaker, writejson,
                               dir_change, linereadit, get_pickled, ext_splitter, appendwriteit, create_folder, from_dict_to_file)
from gidqtutils.gidqtstuff import create_new_font

from pyqtsocius.init_userdata.user_data_setup import Support, request_support_objects
from pyqtsocius.converted_files.Ui_pyqt_sorter_mainwindow import Ui_GidPyQtSorterMain
from pyqtsocius.ui_elements.misc_ui.system_tray import SystemTray
import pyqtsocius.ui_elements.pyqt_sorter_ressources_rc
from pyqtsocius.utilities_and_vendored.visual_effects import addshadoweffect
from pyqtsocius.utilities_and_vendored.widget_insert_items import combobox_insert_set
from pyqtsocius.ui_elements.compound_widgets import SnippetsPageWidget, ContentPageWidget, LinksPageWidget
from pyqtsocius.non_ui_elements.reading import DesignerFileReader
# endregion[Imports]

__updated__ = '2020-10-31 07:32:45'

# region [AppUserData]

APPDATA, USER_CONFIG, SOLID_CONFIG = request_support_objects(Support.ALL)

# endregion [AppUserData]

# region [Configs]

# endregion [Configs]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

# endregion[Constants]


class GidPyQtSociusMainWindow(Ui_GidPyQtSorterMain, QMainWindow):
    # region[Class_Attribute]
    debug_request = pyqtSignal(QPushButton)
    tab_page_info = namedtuple("TabPageInfo", ['widget', 'index', 'description'], defaults=(0, ''))
    # endregion[Class_Attribute]
    # region[Init]

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.main_font = None
        self.completer = None
        self.systemtray = None
        self.design_file_reader = None
        self.recent_files_json = APPDATA['recent_files.json']
        self.tab_page_widgets = {'content_page': self.tab_page_info(ContentPageWidget(), 0),
                                 'snippets_page': self.tab_page_info(SnippetsPageWidget(), 1),
                                 'links_page': self.tab_page_info(LinksPageWidget(), 2)}
        super().setupUi(self)
        self.setup()
        self.actions()
        log.info(glog.class_initiated(self))

# endregion[Init]
# region[Setup]
    def setup(self):
        self.setup_meta_attributes()
        self.setup_main_window()
        self.setup_tabs()
        self.setup_extras()

    def setup_sorter_tab(self):
        self.setup_comboboxes()
        self.switch_enable_input_dependent(False)

    def setup_meta_attributes(self):
        self.setup_main_font()

    def setup_extras(self):

        self.setup_disable_not_implemented()
        self.setup_recent_files_menu()

    def setup_tabs(self):
        for key, widget_tup in self.tab_page_widgets.items():
            self.main_output_tabWidget.insertTab(widget_tup.index, widget_tup.widget, widget_tup.widget.icon, widget_tup.widget.tab_name)
            if key == 'content_page':
                widget_tup.widget.setEnabled(False)

    def setup_main_font(self):
        _name = USER_CONFIG.get('general_font', 'name')
        _size = USER_CONFIG.getint('general_font', 'size')
        _bold = USER_CONFIG.getboolean('general_font', 'bold')
        self.main_font = create_new_font(_name, _size, _bold)

    def setup_main_window(self):
        self.setWindowTitle(SOLID_CONFIG.get('DEFAULT', 'project_name'))
        self.resize(USER_CONFIG.getint('main_window', 'main_window_width'), USER_CONFIG.getint('main_window', 'main_window_height'))
        self.main_output_tabWidget.setCurrentIndex(USER_CONFIG.getint('main_window', 'starting_tab'))
        self.setFont(self.main_font)
        self.debug_pushButton = QPushButton('DEBUG', self.statusbar)
        self.debug_pushButton.pressed.connect(self.debug_requested)
        self.statusbar.addWidget(self.debug_pushButton)
        if USER_CONFIG.getboolean('general_settings', 'use_debbug') is False:
            self.debug_pushButton.setHidden(True)

    def setup_disable_not_implemented(self):
        _not_implemented = loadjson(APPDATA["not_implemented.json"])
        for key, widgetlist in _not_implemented.items():
            _object = self if key == 'main_window' else self.tab_page_widgets[key].widget
            for widget_name in widgetlist:
                getattr(_object, widget_name).setEnabled(False)

    def setup_recent_files_menu(self):
        self.menuRecent_Files.clear()
        _recent_files = loadjson(APPDATA['recent_files.json'])
        for _file in _recent_files:
            _mitem = QAction(self)
            _mitem.setText(_file)
            _mitem.triggered.connect(partial(self.open_file, file=_file))
            self.menuRecent_Files.addAction(_mitem)
        _clear_recent_files = QAction(self)
        _clear_recent_files.setText('Clear Recent Files')
        _clear_recent_files.triggered.connect(self.clear_recent_files)
        self.menuRecent_Files.addSeparator()
        self.menuRecent_Files.addAction(_clear_recent_files)


# endregion[Setup]

# region[Actions]


    def actions(self):
        self.actionClose.triggered.connect(self.app.quit)
        self.actionOpen_Ui_File.triggered.connect(self.open_file)
        self.debug_request.connect(self.tab_page_widgets['content_page'].widget.debug)

# endregion[Actions]

# region[General_Methods]

    def open_file(self, _=None, file=None):
        if file is None:
            file = QFileDialog.getOpenFileName(None, 'Open Ui file to Parse', pathmaker(os.getcwd()), 'Qt Ui-File (*.ui)')[0]
        self.add_to_recent_files(file)
        self.design_file_reader = DesignerFileReader(file)
        self.tab_page_widgets['content_page'].widget.display_data(file, self.design_file_reader)

    def clear_recent_files(self):
        writejson([], self.recent_files_json)
        log.info("recent files list located at %s, was CLEARED", self.recent_files_json)
        self.setup_recent_files_menu()

    def add_to_recent_files(self, file):
        _recent_files = loadjson(self.recent_files_json)
        _file = pathmaker(file)
        if _file not in _recent_files:
            _recent_files.append(_file)
        writejson(_recent_files, self.recent_files_json)
        self.setup_recent_files_menu()

# endregion[General_Methods]
# region[Helper_Methods]

    def changeEvent(self, event):  # sourcery skip: merge-nested-ifs
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.ignore()
                self.hide()
                self.systemtray.show_hide_message("Minimized to Systray", "PyQt-Sorter is minimized to systray, you can always maximize it again via the context menu")
                self.systemtray.hide_option('Hide')

    def exit_app(self):
        self.tray.hide()  # Do this or icon will linger until you hover after exit
        self.app.quit()

    def add_systemtray(self, systemtray):
        self.systemtray = systemtray(self, self.app)
        self.systemtray.new_icon('sidecar_2')
        self.systemtray.show()

    def debug_requested(self):
        # print('nothing set to debug')
        apptest, _, _ = request_support_objects(Support.ALL)
        print(APPDATA == apptest)
# endregion[Helper_Methods]
# region[Mandatory]

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return "Main_Application_Window"


# endregion[Mandatory]

# region [Main_Exec]
if __name__ == '__main__':
    pass
# endregion [Main_Exec]
