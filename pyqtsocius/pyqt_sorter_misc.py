#!d:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/.venv/scripts/python
import xml.etree.ElementTree as ET
from pprint import pprint
from gidtools.gidfiles import QuickFile, readit, writejson


my_str = readit('D:/Dropbox/hobby/Modding/Projects/[Py_base]_PyQt-Sorter/pyqt_sorter/pyqt_sorter_ressources.qrc')

_list = []
tree = ET.ElementTree(ET.fromstring(my_str))
for elt in tree.iter('file'):
    _list.append(elt.attrib)
    for key, value in elt.attrib.items():
        if "snippet" in value:
            print(value)

# writejson(_list, 'test.json')
