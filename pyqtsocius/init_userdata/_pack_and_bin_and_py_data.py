# taskarg: ${fileDirname}
# * Standard Library Imports -->
import os
import json
import shutil
import base64
from dotenv import load_dotenv
# * Gid Imports -->
import gidlogger as glog

log = glog.main_logger_stdout('debug')
log.info(glog.NEWRUN())
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


def as_kb(in_size: int):
    conv = 1024
    return in_size / conv


def as_mb(in_size: int):
    conv = 1024 * 1024
    return in_size / conv


def as_gb(in_size: int):
    conv = 1024 * 1024 * 1024
    return in_size / conv


def pathmaker(first_segment, *in_path_segments, rev=False):
    """
    Normalizes input path or path fragments, replaces '\\\\' with '/' and combines fragments.

    Parameters
    ----------
    first_segment : str
        first path segment, if it is 'cwd' gets replaced by 'os.getcwd()'
    rev : bool, optional
        If 'True' reverts path back to Windows default, by default None

    Returns
    -------
    str
        New path from segments and normalized.
    """
    _first = os.getcwd() if first_segment == 'cwd' else first_segment
    _path = os.path.join(_first, *in_path_segments)
    _path = _path.replace('\\\\', '/')
    _path = _path.replace('\\', '/')
    if rev is True:
        _path = _path.replace('/', '\\')

    return _path.strip()


def loadjson(in_file):
    with open(in_file, 'r') as jsonfile:
        _out = json.load(jsonfile)
    return _out


def writeit(in_file, in_data, append=False, in_encoding='utf-8'):
    """
    Writes to a file.

    Parameters
    ----------
    in_file : str
        The target file path
    in_data : str
        The data to write
    append : bool, optional
        If True appends the data to the file, by default False
    in_encoding : str, optional
        Sets the encoding, by default 'utf-8'
    """
    if isinstance(in_file, (tuple, list)):
        _file = pathmaker(*in_file)
    elif isinstance(in_file, str):
        _file = pathmaker(in_file)
    _write_type = 'w' if append is False else 'a'
    _in_data = in_data
    with open(_file, _write_type, encoding=in_encoding) as _wfile:
        _wfile.write(_in_data)


def appendwriteit(in_file, in_data, in_encoding='utf-8'):
    with open(in_file, 'a', encoding=in_encoding) as appendwrite_file:
        appendwrite_file.write(in_data)


def readit(in_file, per_lines=False, strip_n=False, in_encoding='utf-8', in_errors='strict'):
    """
    Reads a file.

    Parameters
    ----------
    in_file : str
        A file path
    per_lines : bool, optional
        If True, returns a list of all lines, by default False
    strip_n : bool, optional
        If True remove the newline marker from the string, by default False
    in_encoding : str, optional
        Sets the encoding, by default 'utf-8'
    in_errors : str, optional
        How to handle encoding errors, either 'strict' or 'ignore', by default 'strict'

    Returns
    -------
    str
        the read in file as string
    """
    _file = in_file
    _output_list = []
    with open(_file, 'r', encoding=in_encoding, errors=in_errors) as _rfile:
        if per_lines is True:
            _output_list.extend(_rfile.readlines())
            if strip_n is True:
                _output = [item.replace('\n', '') for item in _output_list]

            else:
                _output = _output_list

        elif per_lines is False:
            _output_string = _rfile.read()
            if strip_n is True:
                _output = _output_string.replace('\n', '')

            else:
                _output = _output_string

    return _output


def linereadit(in_file, in_encoding='utf-8', in_errors='strict'):
    with open(in_file, 'r', encoding=in_encoding, errors=in_errors) as lineread_file:
        _out = lineread_file.read().splitlines()
    return _out


def find_files():
    # sourcery skip: inline-immediately-returned-variable, list-comprehension
    _out = []
    for _file in os.scandir():
        if not _file.name.endswith('.py') and not os.path.isdir(_file.path):
            _out.append(_file.path)
    return _out


def pack_data():
    _folder = pathmaker('cwd', 'data_pack')

    a = shutil.make_archive(pathmaker('cwd', 'base_userdata_archive'), format='zip', root_dir=_folder, logger=log)
    return pathmaker(a)


def convert_to_bin(archive, use_base64=False):
    with open(archive, 'rb') as binf:
        _content = binf.read()
    if use_base64 is True:
        _content = base64.b64encode(_content)
    return _content


def write_to_pyfile(**kwargs):
    with open('bin_data.py', 'w') as _file:
        for key, value in kwargs.items():
            _content = value
            _file.write(f'{key} = {_content}\n\n')
    return pathmaker(os.path.abspath('bin_data.py'))


def write_construction_info(uses_base64=False):
    with open('construction_info.py', 'w') as confo_file:
        _appname = "PyQt_Socius"  # input('Name of the Application: ')
        _author = "BrocaProgs"  # input('Author or Organization [Default=BrocaProgs]: ')
        _author = _author if _author != '' else 'BrocaProgs'
        confo_file.write(f"USES_BASE64 = {str(uses_base64)}\n")
        confo_file.write("REDIRECT = None\n")
        confo_file.write(f"AUTHOR = '{str(_author)}'\n")
        confo_file.write(f"APPNAME = '{str(_appname)}'\n")


def generate_user_data_binfile(use_base64):
    this_file_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(pathmaker(this_file_dir))
    _archive = pack_data()
    size = os.stat(_archive).st_size
    if as_gb(size) > 1:
        log_size = round(as_gb(size), 3)
        log_size_type = 'gb'
    elif as_mb(size) > 1:
        log_size = round(as_mb(size), 3)
        log_size_type = 'mb'
    elif as_kb(size) > 1:
        log_size = round(as_kb(size), 1)
        log_size_type = 'kb'
    else:
        log_size = size
        log_size_type = 'b'

    log.info('data was archived with size of %s%s', log_size, log_size_type)
    log.info('converted archive to bin')
    _py_file = write_to_pyfile(bin_archive_data=convert_to_bin(_archive, use_base64))
    write_construction_info(use_base64)
    log.info('bin data was written to python file: %s', _py_file)
    log.info("starting cleanup!")
    os.remove(_archive)
    log.info("cleanup done")
    log.info('---done---')


if __name__ == '__main__':
    generate_user_data_binfile(True)
