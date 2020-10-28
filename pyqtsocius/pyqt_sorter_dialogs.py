# region [Imports]

# *NORMAL Imports -->
from jinja2 import Environment, BaseLoader
import os
import re
from bs4 import BeautifulSoup
import webbrowser
# *GID Imports -->
from gidqtutils.gidqtstuff import create_new_font, make_icons
from gidtools.gidfiles import pathmaker, readit, writeit
import gidlogger as glog
from gidtools.gidcolor import GidColorHSV
# *QT Imports -->
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
# *Local Imports -->
from Ui_pyqt_sorter_widget_info_dialog import Ui_widget_info_Dialog
from Ui_pyqt_sorter_boiler_creator import Ui_boiler_create_Dialog
from pyqt_sorter_utility import ConfigRental, Cfg
from Ui_pyqt_sorter_snippet_add import Ui_add_snippet_Dialog
from Ui_pyqt_sorter_settings import Ui_settings_Dialog
from pyqt_sorter_syntax_highlight import PythonHighlighter

# endregion [Imports]

__updated__ = '2020-09-17 03:22:49'

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]

# region [Constants]


# endregion [Constants]


# region [Global_Functions]


# endregion [Global_Functions]


# region [Factories]


# endregion [Factories]


# region [Paths]


# endregion [Paths]


# region [Functions_1]


# endregion [Functions_1]


# region [Functions_2]


# endregion [Functions_2]


# region [Functions_3]


# endregion [Functions_3]


# region [Functions_4]


# endregion [Functions_4]


# region [Functions_5]


# endregion [Functions_5]


# region [Functions_6]


# endregion [Functions_6]


# region [Functions_7]


# endregion [Functions_7]


# region [Functions_8]

def color_object_from_string(in_string):
    for name, member in GidColorHSV.__members__.items():
        if in_string.casefold() == name.casefold():
            _out = member
    return _out

# endregion [Functions_8]


# region [Functions_9]

def colors_as_list():
    _out = []
    for name in GidColorHSV.__members__:
        _out.append(name)
    return sorted(_out)

# endregion [Functions_9]


# region [Setting_Window_Widget]


# endregion [Setting_Window_Widget]


# region [Dialog_1]

class WidgetInfoDialog(Ui_widget_info_Dialog):
    def __init__(self, model, index, widget_info_Dialog):
        super().setupUi(widget_info_Dialog)
        self.model = model
        self.index = index
        self.widget_name = self.model.content[index.row()][1]
        self.widget_dict = self.model.widget_master_dict.get(self.widget_name)
        self.url = self.widget_dict.get('documentation_link')
        self.remove_regex = re.compile('<a.*?</a>', re.DOTALL)
        self.description_font = create_new_font('Rockwell Nova', in_size=12)
        self.setup_label()
        self.setup_url()
        self.setup_description()
        self.setup_notes()
        self.actions()

    def setup_label(self):
        self.widget_name_label.setText(self.widget_name.upper())

    def setup_url(self):
        self.doc_url_lineEdit.setText(self.url)
        self.doc_url_lineEdit.setReadOnly(True)

    def setup_description(self):
        _html = self.widget_dict.get('description')
        soup = BeautifulSoup(_html, features="html.parser")

        _html = soup.prettify(formatter="html")
        self.description_textBrowser.setHtml(_html)
        self.description_textBrowser.setFont(self.description_font)

    def setup_notes(self):
        self.notes_textEdit.setText(self.widget_dict.get('notes'))

    def actions(self):
        self.notes_textEdit.textChanged.connect(self.notes_changes)
        self.open_site_pushButton.pressed.connect(self.open_site)

    def open_site(self):
        webbrowser.open(self.url)

    def notes_changes(self):
        self.model.widget_master_dict[self.widget_name]['notes'] = self.notes_textEdit.toMarkdown()
        self.model.save_widget_dict()


# endregion [Dialog_1]


# region [Dialog_2]

class BoilerCreationDialog(Ui_boiler_create_Dialog):
    user_config = ConfigRental.get_config(Cfg.User)
    solid_config = ConfigRental.get_config(Cfg.Solid)

    def __init__(self, conv_file, conv_class, boiler_create_dialog):
        super().setupUi(boiler_create_dialog)
        self.dialog_name = boiler_create_dialog
        self.template_file = self.solid_config.get_path('locations', 'boiler_template')
        self.converted_file = conv_file.replace('.py', '')
        self.converted_class = conv_class
        self.new_class = ''
        self.setup_lineedit()
        self.actions()

    def setup_lineedit(self):
        self.converted_class_lineEdit.setText(self.converted_class)
        self.converted_ui_lineEdit.setText(self.converted_file)

    def actions(self):
        self.output_pushButton.pressed.connect(self.get_output_filepath)
        self.add_method_pushButton.pressed.connect(self.add_method_to_list)
        self.delete_method_pushButton.pressed.connect(self.delete_method_from_list)
        self.buttonBox.accepted.connect(self.make_boiler)
        self.methods_listWidget.itemDoubleClicked.connect(self.edit_item)

    def edit_item(self, item):
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.methods_listWidget.editItem(item)

    def get_output_filepath(self):
        _path = QFileDialog.getSaveFileName(None, 'Save Boiler to', os.getcwd())[0]
        self.output_lineEdit.setText(_path)

    def add_method_to_list(self):
        self.methods_listWidget.addItem('EDIT')

    def delete_method_from_list(self):
        if self.methods_listWidget.currentIndex is not None:
            self.methods_listWidget.takeItem(self.methods_listWidget.currentIndex().row())

    def make_boiler(self):
        _template_string = readit(self.template_file)
        _template = Environment(loader=BaseLoader).from_string(_template_string)
        _method_list = []
        if self.output_lineEdit.text() != '':
            for i in range(self.methods_listWidget.count()):
                _method_list.append(self.methods_listWidget.item(i).text())
            _data = _template.render(converted_file=self.converted_file, converted_class=self.converted_class, new_class=self.new_class_lineEdit.text(), methods=_method_list)
            writeit(self.output_lineEdit.text(), _data)

            self.dialog_name.accept()

# endregion [Dialog_2]


# region [Dialog_3]

class SnippetAddDialog(Ui_add_snippet_Dialog):
    user_config = ConfigRental.get_config(Cfg.User)
    solid_config = ConfigRental.get_config(Cfg.Solid)

    def __init__(self, icon_model, snippet_model, add_snippet_Dialog):
        super().setupUi(add_snippet_Dialog)
        self.snippet_data_textEdit.setFont(self.get_new_font())
        self.highlighter = PythonHighlighter(self.snippet_data_textEdit.document())
        self.dialog = add_snippet_Dialog
        self.icon_model = icon_model
        self.snippet_model = snippet_model
        self.icon_listView.setModel(self.icon_model)
        self.snippet_buttonBox.accepted.connect(self.make_new_snippet)
        self.color_comboBox.addItems(colors_as_list())

    def get_new_font(self):
        _name = self.user_config.get('snippet_font', 'name')
        _size = self.user_config.getint('snippet_font', 'size')
        _bold = self.user_config.getboolean('snippet_font', 'bold')
        return create_new_font(_name, _size, _bold)

    def make_new_snippet(self):
        log.info('starting creation of new snippet')
        if self.snippet_name_lineEdit.text() != '':
            _name = self.snippet_name_lineEdit.text()
            _description = self.snippet_description_lineEdit.text()
            _icon = self.icon_model.icon_files[self.icon_listView.currentIndex().row()]
            _color = color_object_from_string(self.color_comboBox.currentText())(100)
            _data = self.snippet_data_textEdit.toPlainText()
            self.snippet_model[_name] = (_description, _icon, _color, _data)
            self.dialog.accept()

# endregion [Dialog_3]


# region [Dialog_4]

class PyQtSorterSettingsDialog(Ui_settings_Dialog):
    user_config = ConfigRental.get_config(Cfg.User)
    solid_config = ConfigRental.get_config(Cfg.Solid)

    def __init__(self, settings_dialog, *args, **kwargs):
        super().setupUi(settings_dialog, *args, **kwargs)
        self.dialog = settings_dialog
        self.tab_dict = {0: 'Main', 1: 'Snippets', 2: 'Useful Links'}
        self.widget_list = ['widget_list_model', 'signal_list_model', 'functions_slots_list_model', 'snippets_list_model']
        self.setup()
        self.actions()

# | Setup Methods -->

    def setup(self):
        self.setup_selection_mechanism()
        self.setup_general_settings()
        self.setup_location_settings()
        self.setup_mainwindow_settings()
        self.setup_widget_settings()

    def setup_general_settings(self):
        logging_bool = self.user_config.getboolean('general_settings', 'use_logging')
        self.uselogging_yes_radioButton.setChecked(logging_bool)
        self.uselogging_no_radioButton.setChecked(not logging_bool)
        self.logginglevel_comboBox.setCurrentText(self.user_config.get('general_settings', 'logging_level').upper())

    def setup_location_settings(self):
        self.output_lineEdit.setText(self.user_config.get_path('locations', 'output'))

    def setup_mainwindow_settings(self):
        self.mainwindow_height_spinBox.setValue(self.user_config.getint('main_window', 'main_window_height'))
        self.mainwindow_width_spinBox.setValue(self.user_config.getint('main_window', 'main_window_width'))
        self.starttab_comboBox.setCurrentText(self.tab_dict[self.user_config.getint('main_window', 'starting_tab')])

    def setup_widget_settings(self):
        for _widget in self.widget_list:
            getattr(self, _widget + '_doubleclickaction_comboBox').setCurrentText(self.user_config.get(_widget, 'on_double_click'))
            getattr(self, _widget + '_usebackgroundcolor_checkBox').setChecked(self.user_config.getboolean(_widget, 'use_background_color'))
            getattr(self, _widget + '_usefontcolor_checkBox').setChecked(self.user_config.getboolean(_widget, 'use_font_color'))
            getattr(self, _widget + '_useicons_checkBox').setChecked(self.user_config.getboolean(_widget, 'use_icons'))
            getattr(self, _widget + '_fontcolor_comboBox').setCurrentText(self.user_config.get(_widget, 'font_color'))
            getattr(self, _widget + '_scroll_speed_spinBox').setValue(self.user_config.getint(_widget, 'scroll_speed'))

# | Setup for Selection Mechanism -->

    def setup_selection_mechanism(self):
        self.section_select_listWidget.setCurrentRow(0)
        self.section_stackedWidget.setCurrentIndex(0)
        self.section_select_listWidget.currentItemChanged.connect(self.change_page)

    def change_page(self, current, previous):
        if not current:
            current = previous
        self.section_stackedWidget.setCurrentIndex(self.section_select_listWidget.row(current))

# | Action List -->

    def actions(self):
        self.settings_buttonBox.accepted.connect(self.settings_accepted)
        self.settings_buttonBox.rejected.connect(self.settings_rejected)

        self.uselogging_yes_radioButton.toggled.connect(self.change_use_logging_setting)
        self.uselogging_no_radioButton.toggled.connect(self.change_use_logging_setting)
        self.logginglevel_comboBox.currentTextChanged.connect(self.change_logging_level)
        self.num_recent_files_spinBox.valueChanged.connect(self.change_num_recent_files)

        self.output_filedialog_toolButton.pressed.connect(self.set_output_folder)
        self.output_lineEdit.textChanged.connect(self.output_path_to_config)
        self.mainwindow_height_spinBox.valueChanged.connect(self.mainwindow_height_to_config)
        self.mainwindow_width_spinBox.valueChanged.connect(self.mainwindow_width_to_config)
        self.starttab_comboBox.currentTextChanged.connect(self.startab_to_config)

        self.widget_list_model_doubleclickaction_comboBox.currentTextChanged.connect(self.widget_list_model_doubleclickaction_to_config)
        self.widget_list_model_usebackgroundcolor_checkBox.toggled.connect(self.widget_list_model_usebackgroundcolor_to_config)
        self.widget_list_model_usefontcolor_checkBox.toggled.connect(self.widget_list_model_usefontcolor_to_config)
        self.widget_list_model_useicons_checkBox.toggled.connect(self.widget_list_model_useicons_to_config)
        self.widget_list_model_fontcolor_comboBox.currentTextChanged.connect(self.widget_list_model_fontcolor_to_config)
        self.widget_list_model_scroll_speed_spinBox.valueChanged.connect(self.widget_list_model_scroll_speed_to_config)
        self.signal_list_model_doubleclickaction_comboBox.currentTextChanged.connect(self.signal_list_model_doubleclickaction_to_config)
        self.signal_list_model_usebackgroundcolor_checkBox.toggled.connect(self.signal_list_model_usebackgroundcolor_to_config)
        self.signal_list_model_usefontcolor_checkBox.toggled.connect(self.signal_list_model_usefontcolor_to_config)
        self.signal_list_model_useicons_checkBox.toggled.connect(self.signal_list_model_useicons_to_config)
        self.signal_list_model_fontcolor_comboBox.currentTextChanged.connect(self.signal_list_model_fontcolor_to_config)
        self.signal_list_model_scroll_speed_spinBox.valueChanged.connect(self.signal_list_model_scroll_speed_to_config)
        self.functions_slots_list_model_doubleclickaction_comboBox.currentTextChanged.connect(self.functions_slots_list_model_doubleclickaction_to_config)
        self.functions_slots_list_model_usebackgroundcolor_checkBox.toggled.connect(self.functions_slots_list_model_usebackgroundcolor_to_config)
        self.functions_slots_list_model_usefontcolor_checkBox.toggled.connect(self.functions_slots_list_model_usefontcolor_to_config)
        self.functions_slots_list_model_useicons_checkBox.toggled.connect(self.functions_slots_list_model_useicons_to_config)
        self.functions_slots_list_model_fontcolor_comboBox.currentTextChanged.connect(self.functions_slots_list_model_fontcolor_to_config)
        self.functions_slots_list_model_scroll_speed_spinBox.valueChanged.connect(self.functions_slots_list_model_scroll_speed_to_config)
        self.snippets_list_model_doubleclickaction_comboBox.currentTextChanged.connect(self.snippets_list_model_doubleclickaction_to_config)
        self.snippets_list_model_usebackgroundcolor_checkBox.toggled.connect(self.snippets_list_model_usebackgroundcolor_to_config)
        self.snippets_list_model_usefontcolor_checkBox.toggled.connect(self.snippets_list_model_usefontcolor_to_config)
        self.snippets_list_model_useicons_checkBox.toggled.connect(self.snippets_list_model_useicons_to_config)
        self.snippets_list_model_fontcolor_comboBox.currentTextChanged.connect(self.snippets_list_model_fontcolor_to_config)
        self.snippets_list_model_scroll_speed_spinBox.valueChanged.connect(self.snippets_list_model_scroll_speed_to_config)


# | Config Writting Actions -->

    def change_num_recent_files(self, number):
        self.user_config.set('general_settings', 'recent_files_limit', str(number))

    def widget_list_model_doubleclickaction_to_config(self, in_data):
        self.user_config.set('widget_list_model', 'on_double_click', str(in_data))

    def widget_list_model_usebackgroundcolor_to_config(self):
        self.user_config.set('widget_list_model', 'use_background_color', str(self.widget_list_model_usebackgroundcolor_checkBox.isChecked()))

    def widget_list_model_usefontcolor_to_config(self):
        self.user_config.set('widget_list_model', 'use_font_color', str(self.widget_list_model_usefontcolor_checkBox.isChecked()))

    def widget_list_model_useicons_to_config(self):
        self.user_config.set('widget_list_model', 'use_icons', str(self.widget_list_model_useicons_checkBox.isChecked()))

    def widget_list_model_fontcolor_to_config(self, in_data):
        self.user_config.set('widget_list_model', 'font_color', str(in_data))

    def widget_list_model_scroll_speed_to_config(self, in_data):
        self.user_config.set('widget_list_model', 'scroll_speed', str(in_data))

    def signal_list_model_doubleclickaction_to_config(self, in_data):
        self.user_config.set('signal_list_model', 'on_double_click', str(in_data))

    def signal_list_model_usebackgroundcolor_to_config(self):
        self.user_config.set('signal_list_model', 'use_background_color', str(self.signal_list_model_usebackgroundcolor_checkBox.isChecked()))

    def signal_list_model_usefontcolor_to_config(self):
        self.user_config.set('signal_list_model', 'use_font_color', str(self.signal_list_model_usefontcolor_checkBox.isChecked()))

    def signal_list_model_useicons_to_config(self):
        self.user_config.set('signal_list_model', 'use_icons', str(self.signal_list_model_useicons_checkBox.isChecked()))

    def signal_list_model_fontcolor_to_config(self, in_data):
        self.user_config.set('signal_list_model', 'font_color', str(in_data))

    def signal_list_model_scroll_speed_to_config(self, in_data):
        self.user_config.set('signal_list_model', 'scroll_speed', str(in_data))

    def functions_slots_list_model_doubleclickaction_to_config(self, in_data):
        self.user_config.set('functions_slots_list_model', 'on_double_click', str(in_data))

    def functions_slots_list_model_usebackgroundcolor_to_config(self):
        self.user_config.set('functions_slots_list_model', 'use_background_color', str(self.functions_slots_list_model_usebackgroundcolor_checkBox.isChecked()))

    def functions_slots_list_model_usefontcolor_to_config(self):
        self.user_config.set('functions_slots_list_model', 'use_font_color', str(self.functions_slots_list_model_usefontcolor_checkBox.isChecked()))

    def functions_slots_list_model_useicons_to_config(self):
        self.user_config.set('functions_slots_list_model', 'use_icons', str(self.functions_slots_list_model_useicons_checkBox.isChecked()))

    def functions_slots_list_model_fontcolor_to_config(self, in_data):
        self.user_config.set('functions_slots_list_model', 'font_color', str(in_data))

    def functions_slots_list_model_scroll_speed_to_config(self, in_data):
        self.user_config.set('functions_slots_list_model', 'scroll_speed', str(in_data))

    def snippets_list_model_doubleclickaction_to_config(self, in_data):
        self.user_config.set('snippets_list_model', 'on_double_click', str(in_data))

    def snippets_list_model_usebackgroundcolor_to_config(self):
        self.user_config.set('snippets_list_model', 'use_background_color', str(self.snippets_list_model_usebackgroundcolor_checkBox.isChecked()))

    def snippets_list_model_usefontcolor_to_config(self):
        self.user_config.set('snippets_list_model', 'use_font_color', str(self.snippets_list_model_usefontcolor_checkBox.isChecked()))

    def snippets_list_model_useicons_to_config(self):
        self.user_config.set('snippets_list_model', 'use_icons', str(self.snippets_list_model_useicons_checkBox.isChecked()))

    def snippets_list_model_fontcolor_to_config(self, in_data):
        self.user_config.set('snippets_list_model', 'font_color', str(in_data))

    def snippets_list_model_scroll_speed_to_config(self, in_data):
        self.user_config.set('snippets_list_model', 'scroll_speed', str(in_data))

    def change_use_logging_setting(self):
        self.user_config.set('general_settings', 'use_logging', self.uselogging_yes_radioButton.isChecked())

    def change_logging_level(self, text):
        self.user_config.set('general_settings', 'logging_level', text.casefold())

    def set_output_folder(self):
        _path = pathmaker(QFileDialog.getExistingDirectory(caption='Output Folder Selection'))
        self.output_lineEdit.setText(_path)
        self.output_lineEdit.textChanged.emit()

    def output_path_to_config(self):
        self.user_config.set('locations', 'output', self.output_lineEdit.Text())

    def mainwindow_height_to_config(self, num):
        self.user_config.set('main_window', 'main_window_height', str(num))

    def mainwindow_width_to_config(self, num):
        self.user_config.set('main_window', 'main_window_width', str(num))

    def startab_to_config(self, text):
        _set_tab = 0
        for key, value in self.tab_dict.items():
            if text.casefold() in value.casefold():
                _set_tab = int(key)
        self.user_config.set('main_window', 'starting_tab', str(_set_tab))


# | Implemented accept/reject Action -->

    def settings_accepted(self):
        self.user_config.save()
        self.dialog.accept()

    def settings_rejected(self):
        self.user_config.read()
        self.dialog.rejected()


# endregion [Dialog_4]

# region [Dialog_5]

# endregion [Dialog_5]

# region [Dialog_6]

# endregion [Dialog_6]

# region [Dialog_7]

# endregion [Dialog_7]

# region [Dialog_8]

# endregion [Dialog_8]

# region [Dialog_9]

# endregion [Dialog_9]

# region [Main_Exec]
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
