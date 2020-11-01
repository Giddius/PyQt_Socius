# * Standard Library Imports -->
import os
import enum
from typing import Union

# * Gid Imports -->
import gidlogger as glog
from gidtools.gidfiles import pathmaker
from gidtools.gidconfig import Cfg, Get, ConfigRental
from gidtools.gidappdata import AppdataFactory
from pyqtsocius.init_userdata.construction_info import APPNAME, AUTHOR, REDIRECT, USES_BASE64
log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


def _check_dev():
    _old_cwd = os.getcwd()
    os.chdir(THIS_FILE_DIR)
    if os.path.exists("dev_env.trigger") is True:

        _out = pathmaker(THIS_FILE_DIR, 'data_pack')
        log.info('dev_marker exists')
    else:

        _out = None
    os.chdir(_old_cwd)
    return _out


class Support(enum.Enum):
    APPDATA = enum.auto()
    ALL = enum.auto()


def _get_appdata():
    if _check_dev() is not None:
        appdata_object = AppdataFactory.setup_appdata(AUTHOR, APPNAME, None, None, None, _check_dev(), REDIRECT)
    log.info("Appdata Handler object is: %s", str(AppdataFactory.handler))
    if AppdataFactory.handler is None:
        log.info("importing bin_data")

        from .bin_data import bin_archive_data
        log.info("Appdata variables are : 'author_name'='%s', 'app_name'='%s', 'dev'='%s', 'redirect'='%s', 'uses_base64'='%s'", AUTHOR, APPNAME, _check_dev(), REDIRECT, USES_BASE64)
        appdata_object = AppdataFactory.setup_from_binarchive(AUTHOR, APPNAME, bin_archive_data, USES_BASE64, _check_dev(), REDIRECT, True)
    else:
        appdata_object = AppdataFactory.get_handler()
    return appdata_object


# @profile
def request_support_objects(request_input: Union[Support, Cfg] = Support.ALL):
    _out = None
    if request_input == Support.ALL:
        appdata_object = _get_appdata()
        usercfg_object = ConfigRental.get_config(Cfg.User)
        solidcfg_object = ConfigRental.get_config(Cfg.Solid)
        _out = (appdata_object, usercfg_object, solidcfg_object)
    elif request_input == Support.APPDATA:
        _out = _get_appdata()
    elif isinstance(request_input, Cfg):
        if AppdataFactory.handler is None:
            _ = _get_appdata()
        _out = ConfigRental.get_config(request_input)
    return _out


if __name__ == '__main__':
    pass
