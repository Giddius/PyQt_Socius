
# region [Imports]
import init_userdata
# *NORMAL Imports -->
import os
import logging
import sys

# *GID Imports -->
from gidqtutils.gidgets import open_one_line_dialog
from gidqtutils.gidqtstuff import create_new_font, make_icons
from gidtools.gidfiles import pathmaker
import gidlogger as glog

# *QT Imports -->
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QEvent, QProcessEnvironment, QSize
from PyQt5.QtGui import QCursor, QFontInfo
from PyQt5.QtWidgets import QAction, QColorDialog, QCompleter, QFileDialog, QFontDialog, QGraphicsDropShadowEffect, QMenu, QSystemTrayIcon, QMainWindow
from gidtools.gidfiles.functions import loadjson, writejson

# *Local Imports -->
from Ui_pyqt_sorter_mainwindow import Ui_GidPyQtSorterMain
from pyqt_sorter_classes import UiFileIndexer, ConfigRental, Cfg, UsefulLinksModel, SnippetsListModel, IconListModel
from pyqt_sorter_dialogs import WidgetInfoDialog, BoilerCreationDialog, SnippetAddDialog, PythonHighlighter, PyQtSorterSettingsDialog

# endregion [Imports]

__updated__ = '2020-10-29 18:30:19'

# region [Configs]

USER_CONFIG = ConfigRental.get_config(Cfg.User)
print(USER_CONFIG.config_file)
SOLID_CONFIG = ConfigRental.get_config(Cfg.Solid)

# endregion [Configs]


# region [Logging]

_log_file = glog.log_folderer(__name__)
log = glog.main_logger(_log_file, USER_CONFIG.get('general_settings', 'logging_level'))
log.info(glog.NEWRUN())
if USER_CONFIG.getboolean('general_settings', 'use_logging') is False:
    logging.disable(logging.CRITICAL)

# endregion [Logging]

# region [Constants]


# endregion [Constants]


# region [Global_Functions]


# endregion [Global_Functions]


# region [Main_Window_Widget]

# +TODO - sort whole file structur and import tree
# +TODO - add dialog boiler option via combobox to boiler create


class PyQtSorterMainWindow(Ui_GidPyQtSorterMain, QMainWindow):
    ucfg = USER_CONFIG
    scfg = SOLID_CONFIG

# | Init ----->

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().setupUi(self)
        self.setup_mainwindow()
        self.highlighter = PythonHighlighter(self.snippet_preview_textEdit.document())
        self.indexer = None
        self.selected_widget_lineEdit.setReadOnly(True)
        self.toolBox.setEnabled(False)
        self.setup_useful_links()
        self.completer = None
        self.setup_combobox()
        self.snippet_model = SnippetsListModel()
        self.icon_model = IconListModel()
        self.tray = SystemTray(self, app)
        self.tray.show()
        self.setup_snippet_tab()
        self.setup_font()
        self.setup_listview_style()
        self.setup_disable_most()
        self.setup_recent_files_menu()
        self.actions()
        log.info(*glog.class_initiated(self.__class__))


# | Open Methods ----->

    def open_new_file(self, in_file=None, uselessbool=True):
        log.debug('uselessbool is very useless and also has a value of: %s', uselessbool)
        if isinstance(in_file, bool) or in_file is None:
            _new_file = QFileDialog.getOpenFileName(None, 'Open Ui file to Parse', pathmaker('cwd'), 'Qt Ui-File (*.ui)')[0]

        else:
            _new_file = in_file
        if _new_file and _new_file.endswith('.ui'):
            _recent_file_list = loadjson(self.scfg.get_path('locations', 'recent_files_json'))
            if _new_file not in _recent_file_list:
                self.insert_to_recent_files(_new_file, _recent_file_list)
            _indexer = UiFileIndexer(pathmaker(_new_file))
            _indexer.process_content()
            self.file_name_label.setText(_indexer.classname)
            _indexer.create_models()
            self.widget_listView.setModel(_indexer.models.get('widget'))
            _indexer.models.get('widget').parent = self.widget_listView
            self.signals_listView.setModel(_indexer.models.get('signal'))
            _indexer.models.get('signal').parent = self.signals_listView
            self.functions_slots_listView.setModel(_indexer.models.get('function_slot'))
            _indexer.models.get('function_slot').parent = self.functions_slots_listView
            self.filter_widget_comboBox.addItems(sorted(list({item[1] for item in _indexer.models['widget'].content})))
            self.indexer = _indexer
            self.statusbar.showMessage(_new_file)
            self.toolBox.setEnabled(True)
            self.setup_completer()
            self.sort()
            self.actions_model_reliant()
            self.content_tab.setEnabled(True)
            self.actionMake_Boiler_File.setEnabled(True)


# | Setup Methods ----->


    def setup_combobox(self):
        self.sort_direction_comboBox.addItems(['ascending', 'descending'])
        self.sort_direction_comboBox.setCurrentText('ascending')
        self.sort_by_comboBox.addItems(['Name', 'Widgets'])
        self.sort_by_comboBox.setCurrentText('Widgets')
        self.filter_widget_comboBox.addItem('only_important')
        self.filter_widget_comboBox.insertItem(0, '--no filter--')
        self.filter_widget_comboBox.setCurrentText('--no filter--')

    def setup_completer(self):
        if self.filter_by_name_radioButton.isChecked():
            self.completer = QCompleter([item[0] for item in self.indexer.models['widget'].content])
        else:
            self.completer = QCompleter([item[1].lstrip('Q') for item in self.indexer.models['widget'].content])
        self.completer.setCaseSensitivity(False)
        self.filter_input_lineEdit.setCompleter(self.completer)

    def setup_disable_most(self):
        self.content_tab.setEnabled(False)
        self.snippets_tab.setEnabled(True)
        self.useful_links_tab.setEnabled(True)
        self.actionMake_Boiler_File.setEnabled(False)

    def setup_font(self):
        _name, _size, _bold = self.ucfg.general_font_settings
        _general_font = create_new_font(in_font_name=_name, in_size=int(_size), in_bold=_bold)
        self.widget_listView.setFont(_general_font)
        self.functions_slots_listView.setFont(_general_font)
        self.signals_listView.setFont(_general_font)

    def setup_listview_style(self):
        self.widget_listView.setSpacing(6)
        self.widget_listView.setIconSize(QSize(50, 50))
        self.widget_listView.setUniformItemSizes(True)
        self.widget_listView.setSelectionRectVisible(True)
        self.widget_listView.verticalScrollBar().setSingleStep(self.ucfg.getint('widget_list_model', 'scroll_speed'))

    def setup_mainwindow(self):
        self.setWindowTitle(self.scfg.get('DEFAULT', 'project_name'))
        self.resize(self.ucfg.getint('main_window', 'main_window_width'), self.ucfg.getint('main_window', 'main_window_height'))
        self.main_output_tabWidget.setCurrentIndex(self.ucfg.getint('main_window', 'starting_tab'))

    def setup_snippet_tab(self):
        self.snippets_tableView.setModel(self.snippet_model)
        self.snippets_tableView.setIconSize(QSize(50, 50))
        self.snippets_tableView.resizeRowsToContents()
        header = self.snippets_tableView.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.snippet_preview_textEdit.setFont(create_new_font('Semi Coder', 11, in_weight=65))

    def setup_useful_links(self):
        self.useful_links_tableView.setModel(UsefulLinksModel())
        header = self.useful_links_tableView.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

    def setup_recent_files_menu(self):
        self.menuRecent_Files.clear()
        _recent_files = loadjson(self.scfg.get_path('locations', 'recent_files_json'))
        for _file in _recent_files:
            _mitem = QAction(self)
            _mitem.setText(_file)
            _mitem.triggered.connect(lambda uselessbool, x=_file: self.open_recent_file(x))
            self.menuRecent_Files.addAction(_mitem)


# | Actions Methods ----->


    def actions(self):
        # *Open File actions -->
        self.actionOpen_Ui_File.triggered.connect(self.open_new_file)
        self.useful_links_tableView.doubleClicked.connect(self.useful_links_tableView.model().double_clicked)
        # *Context Menu actions -->
        self.widget_listView.customContextMenuRequested.connect(self.showmenu_widgets)
        self.signals_listView.customContextMenuRequested.connect(self.showmenu_signals)
        self.functions_slots_listView.customContextMenuRequested.connect(self.showmenu_func_slots)
        # *Filter List actions -->
        self.filter_widget_comboBox.currentTextChanged.connect(self.filter_widgets)
        self.filter_input_lineEdit.textChanged.connect(self.filter_widgets_by_input)
        self.clear_filter_input_pushButton.pressed.connect(self.clear_filters)
        # *Menu actions -->
        self.insert_new_link_pushButton.pressed.connect(self.insert_new_link)
        self.actionMake_Boiler_File.triggered.connect(self.show_create_boiler)
        self.actionOpen_Settings.triggered.connect(self.show_settings_menu)

        self.snippets_tableView.doubleClicked.connect(self.snippets_tableView.model().double_clicked)
        self.new_snippet_pushButton.pressed.connect(self.show_create_new_snippet_dialog)
        self.snippets_tableView.selectionModel().currentChanged.connect(self.show_snippet_preview)
        self.delete_snippet_pushButton.pressed.connect(self.delete_current_snippet)
        self.change_font_pushButton.pressed.connect(self.change_snippet_font)

    def actions_model_reliant(self):
        # *List View double click actions -->
        self.widget_listView.doubleClicked.connect(self.widget_listView.model().double_clicked)
        self.signals_listView.doubleClicked.connect(self.signals_listView.model().double_clicked)
        self.functions_slots_listView.doubleClicked.connect(self.functions_slots_listView.model().double_clicked)
        # *Signal Functions Slots actions -->
        self.widget_listView.selectionModel().currentChanged.connect(self.show_signals_functions_slots)
        # *Sorting and Filter actions -->
        self.sort_widgets_pushButton.pressed.connect(self.sort)
        self.filter_by_name_radioButton.toggled.connect(self.setup_completer)
        self.filter_by_widget_radioButton.toggled.connect(self.setup_completer)


# | Filter Methods ----->

    def filter_widgets(self, text):
        _model = self.widget_listView.model()
        for index, _data in enumerate(_model.content):
            self.widget_listView.setRowHidden(index, False)
            if self.filter_input_lineEdit.text() != '':
                self.filter_widgets_by_input(self.filter_input_lineEdit.text())
            if text == 'only_important':
                if _model.widget_master_dict[_data[1]]['important'] is False:
                    self.widget_listView.setRowHidden(index, True)
            elif text == '--no filter--':
                self.widget_listView.setRowHidden(index, False)
                if self.filter_input_lineEdit.text() != '':
                    self.filter_widgets_by_input(self.filter_input_lineEdit.text())
            else:
                if text.casefold() != _data[1].casefold():
                    self.widget_listView.setRowHidden(index, True)

    def filter_widgets_by_input(self, text):
        _model = self.widget_listView.model()
        _col = 0 if self.filter_by_name_radioButton.isChecked() else 1
        for index, _data in enumerate(_model.content):
            if text == '':
                self.widget_listView.setRowHidden(index, False)
                if self.filter_widget_comboBox.currentText() != '--no filter--':
                    self.filter_widgets(self.filter_widget_comboBox.currentText())
            else:
                if text.casefold() not in _data[_col].casefold():
                    self.widget_listView.setRowHidden(index, True)


# | Change Methods ----->

    def change_funct_slot_background_color(self, event):
        _model = self.functions_slots_listView.model()
        _color = QColorDialog.getColor().toHsv().getHsv()
        log.debug("backgroundcolor selected for functions and slots as HSV values: %s", str(_color))
        _model.change_background_color(_color)

    def change_signal_background_color(self, event):
        _model = self.signals_listView.model()
        _color = QColorDialog.getColor().toHsv().getHsv()
        log.debug("backgroundcolor selected for Signals as HSV values: %s", str(_color))
        _model.change_background_color(_color)

    def change_snippet_font(self):
        _font, _accepted = QFontDialog.getFont(self.snippet_preview_textEdit.font())
        _info = QFontInfo(_font)
        if _accepted:
            self.snippet_preview_textEdit.setFont(_font)
            if self.ucfg.has_section('snippet_font') is False:
                self.ucfg.add_section('snippet_font')
            self.ucfg.set('snippet_font', 'name', str(_info.family()))
            self.ucfg.set('snippet_font', 'size', str(_info.pointSize()))
            _bold = 'no' if _info.bold() is False else 'yes'
            self.ucfg.set('snippet_font', 'bold', _bold)
            self.ucfg.save()

    def change_widget_background_color(self, event):
        _model = self.widget_listView.model()
        _index = self.widget_listView.currentIndex()
        _color = QColorDialog.getColor().toHsv().getHsv()
        log.debug("backgroundcolor selected for widget '%s' as HSV values: %s", _model.index_to_widget(_index), str(_color))
        _model.change_background_color(_index, _color)


# | Clear Methods ----->

    def clear_filters(self):
        self.filter_input_lineEdit.clear()
        self.filter_widget_comboBox.setCurrentText('--no filter--')

    def clear_funct_slot_background_color(self, event):
        _model = self.functions_slots_listView.model()

        log.debug("backgroundcolor selected for Signals as HSV values: %s", 'CLEAR')
        _model.change_background_color('no_color')

    def clear_signal_background_color(self, event):
        _model = self.signals_listView.model()

        log.debug("backgroundcolor selected for Signals as HSV values: %s", 'CLEAR')
        _model.change_background_color('no_color')

# | Menu Methods ------>
    def open_recent_file(self, _file):
        self.open_new_file(in_file=_file, uselessbool=True)

# | Contextmenu Methods ----->

    def showmenu_func_slots(self, event):
        fsmenu = QMenu(self.functions_slots_listView)
        self.add_remove_function_or_slot = fsmenu.addAction('Remove Function or Slot')
        self.add_remove_function_or_slot.triggered.connect(self.delete_func_or_slot)
        color_sub = QMenu(fsmenu)
        color_sub.setTitle('Colors')
        self.add_change_funct_slot_background_color = color_sub.addAction('Change Functions and Slots Background Color')
        self.add_change_funct_slot_background_color.triggered.connect(self.change_funct_slot_background_color)
        self.add_clear_funct_slot_background_color = color_sub.addAction('Clear Functions and Slots Background Color')
        self.add_clear_funct_slot_background_color.triggered.connect(self.clear_funct_slot_background_color)
        fsmenu.addMenu(color_sub)
        if self.functions_slots_listView.currentIndex().row() != -1:
            action = fsmenu.exec_(QCursor.pos())

    def showmenu_signals(self, event):
        smenu = QMenu(self.signals_listView)
        self.add_remove_signal = smenu.addAction('Remove Signal')
        self.add_remove_signal.triggered.connect(self.delete_signal)
        color_sub = QMenu(smenu)
        color_sub.setTitle('Colors')
        self.add_change_signal_background_color = color_sub.addAction('Change Signal Background Color')
        self.add_change_signal_background_color.triggered.connect(self.change_signal_background_color)
        self.add_clear_signal_background_color = color_sub.addAction('Clear Signal Background Color')
        self.add_clear_signal_background_color.triggered.connect(self.clear_signal_background_color)
        smenu.addMenu(color_sub)
        if self.signals_listView.currentIndex().row() != -1:
            action = smenu.exec_(QCursor.pos())

    def showmenu_widgets(self, event):
        wmenu = QMenu(self.widget_listView)

        self.add_showinfo = wmenu.addAction('Show Info')
        self.add_showinfo.triggered.connect(self.show_info_widget)
        self.add_new_signal = wmenu.addAction('Add new SIGNAL to list')
        self.add_new_signal.triggered.connect(self.insert_new_signal)
        self.add_new_function = wmenu.addAction('Add new FUNCTION to list')
        self.add_new_function.triggered.connect(self.insert_new_function)
        self.add_new_slot = wmenu.addAction('Add new SLOT to list')
        self.add_new_slot.triggered.connect(self.insert_new_slot)
        self.add_change_widget_background_color = wmenu.addAction('Change Widget Background Color')
        self.add_change_widget_background_color.triggered.connect(self.change_widget_background_color)
        if self.widget_listView.currentIndex().row() != -1:
            action = wmenu.exec_(QCursor.pos())


# | Delete Methods ----->

    def delete_current_snippet(self):
        _index = self.snippets_tableView.currentIndex()
        _model = self.snippets_tableView.model()
        del _model[_model.content[_index.row()][0]]

    def delete_func_or_slot(self):
        _model = self.functions_slots_listView.model()
        _index = self.functions_slots_listView.currentIndex()
        _fun_slot, _typus = _model.content[_index.row()]
        if _fun_slot != 'not set':
            del _model[(_typus, _fun_slot)]
        self.functions_slots_listView.update()

    def delete_signal(self):
        _model = self.signals_listView.model()
        _signal = _model.content[self.signals_listView.currentIndex().row()][0]
        if _signal != 'not set':
            del _model[('signals', _signal)]
        self.signals_listView.update()


# | Dialog Show Methods ----->

    def show_create_boiler(self):
        converted_file = 'Ui_' + os.path.basename(self.indexer.file).replace('.ui', '.py')
        converted_class = self.file_name_label.text()
        dialog = QtWidgets.QDialog()
        dialog.ui = BoilerCreationDialog(converted_file, converted_class, dialog)
        dialog.exec_()

    def show_create_new_snippet_dialog(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = SnippetAddDialog(self.icon_model, self.snippet_model, dialog)
        dialog.exec_()

    def show_info_widget(self):
        _cur_index = self.widget_listView.currentIndex()
        _model = self.widget_listView.model()
        dialog = QtWidgets.QDialog()
        dialog.ui = WidgetInfoDialog(_model, _cur_index, dialog)
        dialog.exec_()

    def show_settings_menu(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = PyQtSorterSettingsDialog(dialog)
        dialog.exec_()
        self.main_output_tabWidget.setCurrentIndex(self.ucfg.getint('main_window', 'starting_tab'))

    def show_signals_functions_slots(self, current_index, previous_index):
        _widget = self.widget_listView.model().content[current_index.row()][1]
        _name = self.widget_listView.model().content[current_index.row()][0]
        self.signals_listView.model().set_current_widget(_widget, _name)
        self.functions_slots_listView.model().set_current_widget(_widget, _name)
        self.selected_widget_lineEdit.setText(_widget)

    def show_snippet_preview(self, current_index, previous_index):
        self.snippet_preview_textEdit.setText(self.snippet_model.get_full_snippet(current_index))


# | Sort Methods ----->

    def sort(self):
        _direction = self.sort_direction_comboBox.currentText().casefold()
        _by = self.sort_by_comboBox.currentText().casefold()
        self.indexer.models['widget'].extra_sorting((_direction, _by))


# | Insert Methods ----->

    def insert_to_recent_files(self, in_file, in_list):
        if (len(in_list) + 1) > self.ucfg.getint('general_settings', 'recent_files_limit'):
            _ = in_list.pop(-1)

        in_list.insert(0, in_file)
        writejson(in_list, self.scfg.get_path('locations', 'recent_files_json'))
        self.setup_recent_files_menu()

    def insert_new_function(self):
        _model = self.functions_slots_listView.model()
        _new_function = open_one_line_dialog()
        if _new_function != '':
            _model['functions'] = _new_function
        self.functions_slots_listView.update()

    def insert_new_link(self):
        _name = self.new_link_name_lineEdit.text()
        _link = self.new_link_lineEdit.text()
        _description = self.new_link_description_plainTextEdit.toPlainText()
        if _name != '' and _link != '':
            self.useful_links_tableView.model()[_name] = (_name, _link, _description)

    def insert_new_signal(self):
        _model = self.signals_listView.model()
        _new_signal = open_one_line_dialog()
        if _new_signal != '':
            _model['signals'] = _new_signal
        self.signals_listView.update()

    def insert_new_slot(self):
        _model = self.functions_slots_listView.model()
        _new_slot = open_one_line_dialog()
        if _new_slot != '':
            _model['slots'] = _new_slot
        self.functions_slots_listView.update()


# | Helper Methods ----->

    def _addshadoweffect(self, item):
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(1)
        effect.setOffset(3, 3)
        item.setGraphicsEffect(effect)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                event.ignore()
                self.hide()
                self.tray.showMessage("Minimized to Systray", "PyQt-Sorter is minimized to systray, you can always maximize it again via the context menu", make_icons(":/icons/gid_logo", 50, 50))

    def exit_app(self):
        self.tray.hide()  # Do this or icon will linger until you hover after exit
        app.quit()


# endregion [Main_Window_Widget]

# region [Main_Exec]
if __name__ == '__main__':
    try:
        env = QProcessEnvironment.systemEnvironment()
        env.insert('QT_DEBUG_PLUGINS', "1")
        app = QtWidgets.QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(True)
        MainWindow = PyQtSorterMainWindow()
        MainWindow.show()
        sys.exit(app.exec_())
    except:
        log.exception(sys.exc_info()[0])
        raise

# endregion [Main_Exec]
