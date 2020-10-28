# region [Imports]

# *NORMAL Imports -->
import re
import xml.etree.ElementTree as ET
# *GID Imports -->
from gidtools.gidfiles import ext_splitter, linereadit, pathmaker, readit, splitoff
import gidlogger as glog
# *QT Imports -->

# *Local Imports -->
from pyqt_sorter_models import Cfg, ConfigRental, FunctionsSlotsModel, SignalModel, WidgetListModel, UsefulLinksModel, SnippetsListModel, IconListModel

# endregion [Imports]

__updated__ = '2020-09-02 19:54:36'

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion [Logging]


# region [Constants]


# endregion [Constants]


# region [Global_Functions]


# endregion [Global_Functions]


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

# region [Enums]


# endregion [Enums]

# region [Factories]


# endregion [Factories]

# region [Class_1]

class UiFileIndexer:
    user_config = ConfigRental.get_config(Cfg.User)
    solid_config = ConfigRental.get_config(Cfg.Solid)

    def __init__(self, in_file):
        self.file = in_file
        self.raw_content = linereadit(self.file)
        self.classname = ''
        self.widgets = []
        self.models = {'widget': None, 'menu': None, 'action': None}
        log.info(*glog.class_initiated(self.__class__))

    # def process_content(self):
    #     for line in self.raw_content:
    #         if 'self.' in line and '=' in line and '#' not in line:
    #             _namepart, _widgetpart = line.split(' = ', 1)
    #             _name = _namepart.split('.', 1)[1]
    #             _widget = _widgetpart.split('(', 1)[0]
    #             if '.' in _widget:
    #                 _widget = _widget.split('.', 1)[1]
    #                 self.widgets.append((_name.strip(), _widget.strip()))
    #         elif 'class' in line:
    #             _withparenthesis = line.split(' ', 1)[1]
    #             self.classname = _withparenthesis.split('(', 1)[0].strip()

    def process_content(self):
        _xml_content = readit(self.file)
        xml_tree = ET.ElementTree(ET.fromstring(_xml_content))
        for element in xml_tree.iter('widget'):
            _widget = element.attrib.get('class')
            _name = element.attrib.get('name')
            self.widgets.append((_name, _widget))
        self.get_classname()

    def get_classname(self):
        _path, _file = splitoff(self.file)
        _file = 'Ui_' + ext_splitter(_file) + '.py'
        _content = readit(pathmaker(_path, _file))
        self.classname = re.search('(?<=class ).*?(?=\()', _content).group()

    def create_models(self):
        _widget_model = WidgetListModel(self.widgets)
        _signal_model = SignalModel()
        _funct_slot_model = FunctionsSlotsModel()
        self.models['widget'] = _widget_model
        self.models['signal'] = _signal_model
        self.models['function_slot'] = _funct_slot_model

# endregion [Class_1]

# region [Class_2]


# endregion [Class_2]

# region [Class_3]

# endregion [Class_3]

# region [Class_4]

# endregion [Class_4]

# region [Class_5]

# endregion [Class_5]

# region [Class_6]

# endregion [Class_6]

# region [Class_7]

# endregion [Class_7]

# region [Class_8]

# endregion [Class_8]

# region [Class_9]
# endregion [Class_9]
# region [Main_Exec]
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
