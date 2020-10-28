from setuptools import setup, find_packages
import subprocess
import sys
import os
try:
    from dotenv import load_dotenv
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'python-dotenv'])
    from dotenv import load_dotenv

load_dotenv()

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
README_FILE = 'README.md'
REQUIREMENTS_FILE = 'requirements_dev.txt'


def remove_version(in_line):
    if '==' in in_line:
        return in_line.split('==')[0].strip()
    else:
        return in_line.strip()


def read_file(in_file):
    with open(in_file, 'r', errors='replace') as fileobject:
        _out = fileobject.read()
    return _out


def read_filelines(in_file, line_modifier=None):
    _out = []
    with open(in_file, 'r', errors='replace') as fileobject:
        _temp_list = fileobject.read().splitlines()

    for line in _temp_list:
        if line.startswith('-e') is False and line != '':
            if line_modifier is not None:
                _out.append(line_modifier(line))
            else:
                _out.append(line.strip())
    return _out


def get_description_type(in_readme_file):
    _type_dict = {
        'md': 'text/markdown',
        'rst': 'text/x-rst',
        'txt': 'text/plain'
    }
    _ext = in_readme_file.split('.')[-1]
    return _type_dict.get(_ext, 'text/plain')


def get_name():
    _name = os.getenv('PACK_NAME')
    if _name is None:
        _name = os.path.basename(THIS_FILE_DIR).lower().replace(' ', '_').replace('_', '')
    return _name


setup(name=get_name(),
      version='0.1',
      description='',
      long_description=read_file(README_FILE),
      long_description_content_type=get_description_type(README_FILE),
      url='',
      author='Giddi',
      license='MIT',
      packages=find_packages(),
      install_requires=read_filelines(REQUIREMENTS_FILE, remove_version),
      include_package_data=True
      )
