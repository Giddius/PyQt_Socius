import os
from gidtools.gidfiles import QuickFile, pathmaker, writeit, writejson, loadjson, readit
from inspect import getclasstree, getmembers, signature, getsourcelines, getsource, ismethod, isclass, isfunction, getdoc, getsourcefile, getfile, getcomments
import gidtools.gidfiles
from gidtools.gidfiles.functions import linereadit
from pyqt_sorter_main import PyQtSorterMainWindow
import shutil
import re
import statistics
import jinja2
from PyQt5.QtGui import QPushButton

DEF_REGEX = re.compile(r"(?<=def ).*?(?=\()")

MAIN_DIR = "D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/dev_ressources/code_clean_and_sort"


def save_filter_dict(in_data):
    writejson(in_data, "D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/dev_ressources/dev_data/code_clean_sort_dict.json")


def get_filter_dict():
    return loadjson("D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/dev_ressources/dev_data/code_clean_sort_dict.json")


def create_folder(in_folder):
    if isinstance(in_folder, list):
        for folder in in_folder:
            _path = "D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/dev_ressources/code_clean_and_sort/" + folder
            if os.path.isdir(_path) is False:
                os.makedirs(_path)
    if isinstance(in_folder, str):
        _path = "D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/dev_ressources/code_clean_and_sort/" + in_folder
        if os.path.isdir(_path) is False:
            os.makedirs(_path)


def create_files(object):
    _path = "D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/dev_ressources/code_clean_and_sort"
    _list = [object]
    _temp = []
    for item in _list:
        print(str(item))
        for _name, _method in getmembers(item, predicate=isfunction):

            writeit(pathmaker(_path, _name + '.py'), getsource(_method))


def add_to_filter_dict(name, folder, keyword=None):
    _dict = get_filter_dict()
    _word = ('',) if keyword is None else keyword
    if name not in _dict:
        _dict[name] = {'folder': folder, 'keyword': _word, 'files': []}
    else:
        print(name + ' already in json file')
    save_filter_dict(_dict)


def filter_files():
    _dict = get_filter_dict()
    for key, value in _dict.items():
        create_folder(value['folder'])
        for _file in os.listdir(MAIN_DIR):
            _the_file = None
            if _file.endswith('.py'):
                if value['keyword'][1] == 'full':
                    if _file.replace('.py', '') == value['keyword'][0]:
                        value['files'].append(_file)
                        _the_file = _file

                elif value['keyword'][1] == 'starts':
                    if _file.replace('.py', '').startswith(value['keyword'][0]):
                        _the_file = _file

                elif value['keyword'][1] == 'ends':
                    if _file.replace('.py', '').endswith(value['keyword'][0]):
                        _the_file = _file

                elif value['keyword'][1] == 'any':
                    if value['keyword'][0] in _file.replace('.py', ''):
                        _the_file = _file

            if _the_file is not None and _the_file != '':
                value['files'].append(_the_file)
                shutil.move(pathmaker(MAIN_DIR, _the_file), pathmaker(MAIN_DIR, value['folder']))
    save_filter_dict(_dict)


# add_to_filter_dict('setup', 'setup_methods', ('setup', 'starts'))


def super_main(name, folder, keyword, keyword_type):
    add_to_filter_dict(name, folder, (keyword, keyword_type))
    filter_files()


def rename_to_file_name():
    _rename_dict = {}
    for dirname, _m, filelist in os.walk(MAIN_DIR):
        for _file in filelist:
            if _file.endswith('.py'):
                _file_name = _file
                _full_path = pathmaker(dirname, _file_name)
                _cleaned_file_name = _file_name.replace('.py', '')
                _content = readit(_full_path)

                if DEF_REGEX.search(_content):
                    _def_line_old = DEF_REGEX.search(_content).group()
                    if _def_line_old != _cleaned_file_name:
                        _rename_dict[_def_line_old] = _cleaned_file_name
    for dirname, _m, filelist in os.walk(MAIN_DIR):
        for _file in filelist:
            if _file.endswith('.py'):
                _file_name = _file
                _full_path = pathmaker(dirname, _file_name)
                _content = readit(_full_path)
                for key, value in _rename_dict.items():
                    if key in _content:
                        _content = _content.replace(key, value)
                        writeit(_full_path, _content)


def list_folder():
    _out = []
    for folder in os.listdir(MAIN_DIR):
        if os.path.isdir(pathmaker(MAIN_DIR, folder)):
            _out.append(folder)
    writeit('D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/dev_ressources/code_clean_and_sort/folder_list.txt', '\n'.join(_out))
    writejson(_out, "D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/dev_ressources/dev_data/folder_list.json")


def replace_source():
    _new_file = 'temp_file.py'
    _old_file = "D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/pyqt_sorter_main.py"
    _old_source = getsource(PyQtSorterMainWindow)
    _new_source = _old_source.splitlines()[0] + '\n'
    _new_source += _old_source.splitlines()[1] + '\n'
    _new_source += _old_source.splitlines()[2] + '\n'
    for folder in loadjson("D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/dev_ressources/dev_data/folder_list.json"):
        _folder_source = ''
        for files in os.listdir(pathmaker(MAIN_DIR, folder)):
            if '_combined' not in files:
                _folder_source += readit(pathmaker(MAIN_DIR, folder, files)) + '\n'
        writeit(pathmaker(MAIN_DIR, folder, folder + '_combined.py'), _folder_source, append=False)
    for _folder in linereadit('D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/dev_ressources/code_clean_and_sort/folder_list.txt'):
        if _folder != '':
            _path = pathmaker(MAIN_DIR, _folder, _folder + '_combined.py')
            _content = readit(_path)
            seperator = '\n# | ' + _folder + ' ----->\n\n'
            _new_source += seperator.replace('_', ' ').title()
            _new_source += _content + '\n\n'
    writeit(_new_file, readit(_old_file).replace(_old_source, _new_source))


import PyQt5.QtGui
import PyQt5.QtCore
import PyQt5.QtDesigner
import PyQt5.QtWidgets
from PyQt5.QtCore import QLibraryInfo
OOOUT = QuickFile()
Out2 = QuickFile()
Out3 = QuickFile()
Out4 = QuickFile()
Out5 = QuickFile()
Out6 = QuickFile()
Out7 = QuickFile()
Out8 = QuickFile()
Out9 = QuickFile()
Out10 = QuickFile()
_mat = [PyQt5.QtGui, PyQt5.QtCore, PyQt5.QtDesigner, PyQt5.QtWidgets]
_listi = []
for item in getmembers(PyQt5.QtDesigner.QExtensionManager):
    Out8.apwrite(str(item))
    _name, other = item
    if not _name.startswith('__') and isfunction(other):
        OOOUT.apwrite(_name)
    elif isclass(other):
        Out2.apwrite(_name)
    elif ismethod(other):
        Out3.apwrite(_name)
    elif isfunction(other):
        Out7.apwrite(_name)
    Out4.apwrite(str(getdoc(other)) + '\n')

    if isclass(other):
        _listi.append(other)

Out5.write(str(getclasstree(_listi)))

Out6.write(getmembers(PyQt5.QtDesigner.QAbstractExtensionManager), pretty=True)
_enu_list = [
    QLibraryInfo.PrefixPath,
    QLibraryInfo.DocumentationPath,
    QLibraryInfo.HeadersPath,
    QLibraryInfo.LibrariesPath,
    QLibraryInfo.LibraryExecutablesPath,
    QLibraryInfo.BinariesPath,
    QLibraryInfo.PluginsPath,
    QLibraryInfo.ImportsPath,
    QLibraryInfo.Qml2ImportsPath,
    QLibraryInfo.ArchDataPath,
    QLibraryInfo.DataPath,
    QLibraryInfo.TranslationsPath,
    QLibraryInfo.ExamplesPath,
    QLibraryInfo.TestsPath,
    QLibraryInfo.SettingsPath,
]
_enu_name_list = [
    "QLibraryInfo.PrefixPath",
    "QLibraryInfo.DocumentationPath",
    "QLibraryInfo.HeadersPath",
    "QLibraryInfo.LibrariesPath",
    "QLibraryInfo.LibraryExecutablesPath",
    "QLibraryInfo.BinariesPath",
    "QLibraryInfo.PluginsPath",
    "QLibraryInfo.ImportsPath",
    "QLibraryInfo.Qml2ImportsPath",
    "QLibraryInfo.ArchDataPath",
    "QLibraryInfo.DataPath",
    "QLibraryInfo.TranslationsPath",
    "QLibraryInfo.ExamplesPath",
    "QLibraryInfo.TestsPath",
    "QLibraryInfo.SettingsPath",
]
for index, enu in enumerate(_enu_list):
    Out9.apwrite(_enu_name_list[index])
    Out9.apwrite(PyQt5.QtCore.QLibraryInfo.location(enu))
    Out9.apwrite('\n\n--###########################################################################---\n\n')


Out10.write(str(PyQt5.QtDesigner.QExtensionManager.pyqtConfigure))
