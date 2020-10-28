import configparser
from gidtools.gidfiles import pathmaker
from enum import Enum, auto
import gidlogger as glog

log = glog.aux_logger(__name__)
log.info(*glog.imported(__name__))


class Cfg(Enum):
    User = auto()
    Solid = auto()
    Database = auto()


class ConfigHandler(configparser.ConfigParser):
    def __init__(self, config_file=None, auto_read=True, **kwargs):
        super().__init__(**kwargs)
        self.config_file = '' if config_file is None else config_file
        self.auto_read = auto_read
        if self.auto_read is True:
            self.read()
        log.info(*glog.class_initiated(self.__class__))

    def getlist(self, section, key, delimiter=',', as_set=False):
        _raw = self.get(section, key).strip()
        if _raw.endswith(delimiter):
            _raw = _raw.rstrip(delimiter)
        if _raw.startswith(delimiter):
            _raw = _raw.lstrip(delimiter).strip()
        _out = _raw.replace(delimiter + ' ', delimiter).split(delimiter)
        if as_set is True:
            _out = set(_out)
        return _out

    def list_from_keys_only(self, section, as_set=True):
        _result = self.options(section)
        _out = []
        for line in _result:
            if line != '':
                _out.append(line)
        if as_set is True:
            _out = set(_out)
        return _out

    def get_path(self, section, key, cwd_symbol='+cwd+'):
        _raw_path = self.get(section, key)
        if cwd_symbol in _raw_path:
            _out = pathmaker('cwd', _raw_path.replace(cwd_symbol, ''))
        else:
            _out = pathmaker(_raw_path)
        return _out

    def get_color(self, section, key):
        _out = self.get(section, key)
        if _out.startswith('('):
            _out = eval(_out)
        elif _out == 'no_color':
            _out = _out
        else:
            raise ValueError('is not a list of colors')
        return _out

    @property
    def general_font_settings(self):
        _name = self.get('general_font', 'name')
        _size = self.getint('general_font', 'size')
        _bold = self.getboolean('general_font', 'bold')
        return (_name, _size, _bold)

    def save(self):
        with open(self.config_file, 'w') as confile:
            self.write(confile)
        self.read()

    def read(self):
        super().read(self.config_file)


class ConfigRental:
    UCFG = None
    SCFG = None
    config_folder = pathmaker('cwd', 'config')

    @classmethod
    def get_config(cls, variant=Cfg.User):
        if variant == Cfg.User:
            if cls.UCFG is None:
                cls.UCFG = ConfigHandler(pathmaker(cls.config_folder, 'user_config.ini'), inline_comment_prefixes='#')
            return cls.UCFG
        elif variant == Cfg.Solid:
            if cls.SCFG is None:
                cls.SCFG = ConfigHandler(pathmaker(cls.config_folder, 'solid_config.ini'), inline_comment_prefixes='#')
            return cls.SCFG


if __name__ == '__main__':
    pass
