# region [Imports]

# *NORMAL Imports -->
import os
import pyperclip
import webbrowser

# *GID Imports -->
from gidqtutils.gidqtstuff import make_icons, make_icons
from gidtools.gidfiles import loadjson, pathmaker, writejson
import gidlogger as glog

# *QT Imports -->
from PyQt5.QtCore import QAbstractListModel, QAbstractTableModel, Qt
from PyQt5.QtGui import QBrush, QColor

# *Local Imports -->
from pyqt_sorter_utility import ConfigRental, Cfg

# endregion [Imports]

__updated__ = '2020-10-30 05:03:26'

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]

# region [Constants]

SNIPPET_ICON_LIST = [
    "snippet1",
    "snippet2",
    "snippet3",
    "snippet_4",
    "snippet_5",
    "snippet_6",
    "snippet_7",
    "snippet_8",
    "snippet_9",
    "snippet_10",
    "snippet_11",
    "snippet_12",
    "snippet_13",
    "snippet_14",
    "snippet_15",
    "snippet_16",
    "snippet_17",
]


# endregion [Constants]


# region [Global_Functions]


# endregion [Global_Functions]


# region [Functions_1]


# endregion [Functions_1]


# region [Functions_2]


# endregion [Functions_2]


# region [Functions_3]


# endregion [Functions_3]


# region [Support_Objects]

# class RowColorizer:

#     def __init__(self, number_of_colors, colors):
#         self.num_col = number_of_colors
#         self.colors = colors
#         if len(self.colors) != self.num_col:
#             raise ValueError('number of colors and provided colors amount does not match')

#     def get_row_color(self, index, alpha=200):
#         _out = QBrush(QColor(256, 256, 256, alpha))
#         for i in reversed(range(self.num_col)):
#             if index % i == 0:
#                 red, green, blue, _ = self.colors[i]
#                 _out = QBrush(QColor(int(red), int(green), int(blue), alpha))
#                 break
#         return _out

# endregion [Support_Objects]


# region [Factories]

# def color_factory(*colors, rand_col_num=5):
#     randomcol = RandomRGB(alpha=0.1)
#     if len(colors) == 0:
#         _color_list = [randomcol() for _ in range(rand_col_num)]
#         _out = RowColorizer(rand_col_num, _color_list)
#     else:
#         _color_list = [color() for color in colors]
#         _out = RowColorizer(len(_color_list), _color_list)
#     return _out

# endregion [Factories]

# region [Model_1]


# endregion [Model_1]

# region [Model_2]

class SignalModel(QAbstractTableModel):
    user_config = ConfigRental.get_config(Cfg.User)
    solid_config = ConfigRental.get_config(Cfg.Solid)
    color_dict = {
        'signal': Qt.darkYellow,
        'function': Qt.darkCyan,
        'slot': Qt.darkGray
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_master_dict = loadjson(self.solid_config.get_path('locations', 'widget_json'))
        self.header = ['Signals']
        self.cur_widget = ''
        self.cur_name = ''
        self.content = None
        self.font_color = Qt.darkYellow

        log.info(*glog.class_initiated(self.__class__))

    @ property
    def settings(self):
        _settings = {}
        for name, value in self.user_config.items(str(self)):
            _settings[name] = value
        return _settings

    def data(self, index, role):
        if not index.isValid() and self.cur_widget != '':
            return None
        elif role in [Qt.DisplayRole]:
            return self.content[index.row()][0]
        elif role == Qt.ToolTipRole:
            return self.content[index.row()][1]
        elif role == Qt.BackgroundRole:
            _color = self.user_config.get_color(str(self), 'background_color_hsv')
            if _color == 'no_color':
                return None
            else:
                hue, value, saturation, alpha = _color
                alpha = int(150)
                return QBrush(QColor.fromHsv(int(hue), int(value), int(saturation), int(alpha)))

        elif role == Qt.ForegroundRole:
            return QColor(self.color_dict.get(self.content[index.row()][1]))

    def set_current_widget(self, widget, name):
        self.layoutAboutToBeChanged.emit()
        if widget in self.widget_master_dict:
            self.cur_widget = widget
            self.cur_name = name
            self.content = self.get_content()
        else:
            print('Error! widget not in widget_dict.json!')
        self.layoutChanged.emit()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def rowCount(self, index):
        if self.cur_widget != '':
            return len(self.content)
        else:
            return 0

    def columnCount(self, parent):
        return len(self.header)

    def get_content(self):
        # sourcery skip: inline-immediately-returned-variable, list-comprehension
        _out = []
        for item in self.widget_master_dict[self.cur_widget].get('signals', ['not set']):
            _out.append((item, 'signal'))
        if len(_out) == 0:
            _out = [('not set', 'signal')]
        return _out

    def double_clicked(self, index):
        _data = ''
        if self.settings.get('on_double_click', '') == 'copy':
            _data = f'self.{self.cur_name}.{self.content[index.row()][0]}.connect(print)'
        pyperclip.copy(_data)

    def __setitem__(self, key, value):
        self.beginResetModel()
        self.widget_master_dict[self.cur_widget][key].append(value)
        self.save_widget_dict()
        self.content = []
        self.content = self.get_content()
        self.endResetModel()

    def __delitem__(self, key):
        self.beginResetModel()
        self.widget_master_dict[self.cur_widget][key[0]].remove(key[1])
        self.save_widget_dict()
        self.content = []
        self.content = self.get_content()
        self.endResetModel()

    def change_background_color(self, color):
        self.beginResetModel()
        self.user_config.set(str(self), 'background_color_hsv', str(color))
        self.user_config.save()
        self.endResetModel()

    def save_widget_dict(self):
        writejson(self.widget_master_dict, pathmaker('cwd', self.solid_config.get_path('locations', 'widget_json')))

    def __str__(self):
        return 'signal_list_model'

# endregion [Model_2]

# region [Model_3]


class FunctionsSlotsModel(SignalModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = ['Functions and Slots']
        self.font_color = Qt.darkBlue
        log.info(*glog.class_initiated(self.__class__))

    def get_content(self):
        _out = []
        for item in self.widget_master_dict[self.cur_widget].get('functions', ['not set']):
            _out.append((item, 'function'))
        for bitem in self.widget_master_dict[self.cur_widget].get('slots', ['not set']):
            _out.append((bitem, 'slot'))
        if len(_out) == 0:
            _out = [('not set', 'function'), ('not set', 'slot')]
        return _out

    def double_clicked(self, index):
        _data = ''
        if self.settings.get('on_double_click', '') == 'copy':
            _data = f'self.{self.cur_name}.{self.content[index.row()][0]}()'
        pyperclip.copy(_data)

    def __str__(self):
        return 'functions_slots_list_model'
# endregion [Model_3]

# region [Model_4]


class UsefulLinksModel(QAbstractTableModel):
    user_config = ConfigRental.get_config(Cfg.User)
    solid_config = ConfigRental.get_config(Cfg.Solid)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.link_file = self.solid_config.get_path('locations', 'useful_links_file')
        self.raw_content = self.get_json()
        self.content = self.transform_content()
        self.header = ['Name', 'Description']
        log.info(*glog.class_initiated(self.__class__))

    def update_everything(self):
        self.beginResetModel()
        self.save_json()
        self.raw_content = {}
        self.raw_content = self.get_json()
        self.content = self.transform_content()
        self.endResetModel()

    def get_json(self):
        if os.path.isfile(self.link_file) is False:
            _dict = {'Placeholder': {'name': 'Placeholder', 'link': 'Placeholder.com', 'description': 'Placeholder'}}
            writejson(_dict, self.link_file)
        return loadjson(self.link_file)

    def save_json(self):
        writejson(self.raw_content, self.link_file)

    def transform_content(self):
        _out = []
        for key, value in self.raw_content.items():
            _out.append((value['name'], value['description'], value['link'], key))
        return _out

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role in [Qt.DisplayRole]:
            return self.content[index.row()][index.column()]
        elif role == Qt.ToolTipRole:
            return self.content[index.row()][2]
        # elif role == Qt.BackgroundRole:
        #     return QBrush(QColor.fromHsv(int(hue), int(value), int(saturation), int(alpha)))

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def rowCount(self, index):
        return len(self.content)

    def columnCount(self, parent):
        return len(self.header)

    def __setitem__(self, key, value):
        self.raw_content[key] = {'name': value[0], 'link': value[1], 'description': value[2]}
        if 'Placeholder' in self.raw_content:
            del self.raw_content['Placeholder']
        self.update_everything()

    def __delitem__(self, key):
        del self.raw_content[key]
        self.update_everything()

    def double_clicked(self, index):
        webbrowser.open(self.content[index.row()][2])


# endregion [Model_4]

# region [Model_5]


# endregion [Model_5]

# region [Model_6]


class IconListModel(QAbstractListModel):
    user_config = ConfigRental.get_config(Cfg.User)
    solid_config = ConfigRental.get_config(Cfg.Solid)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_folder = self.solid_config.get_path('locations', 'icon_folder')
        self.icon_files = SNIPPET_ICON_LIST

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role in [Qt.DisplayRole]:
            return self.icon_files[index.row()]
        elif role in [Qt.DecorationRole]:
            return make_icons(':/icons/' + self.icon_files[index.row()], 50, 50)

    def rowCount(self, index):
        return len(self.icon_files)

    def __str__(self):
        return 'icons_list_model'

# endregion [Model_6]

# region [Model_7]

# endregion [Model_7]

# region [Model_8]

# endregion [Model_8]

# region [Model_9]

# endregion [Model_9]


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]
