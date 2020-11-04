@echo off
setlocal enableextensions
set OLDHOME_FOLDER=%~dp0
set INPATH=%~dp1
set INFILE=%~nx1
set INFILEBASE=%~n1

rem ---------------------------------------------------
set _date=%DATE:/=-%
set _time=%TIME::=%
set _time=%_time: =0%
rem ---------------------------------------------------
rem ---------------------------------------------------
set _decades=%_date:~-2%
set _years=%_date:~-4%
set _months=%_date:~3,2%
set _days=%_date:~0,2%
rem ---------------------------------------------------
set _hours=%_time:~0,2%
set _minutes=%_time:~2,2%
set _seconds=%_time:~4,2%
rem ---------------------------------------------------
set TIMEBLOCK=%_years%-%_months%-%_days%_%_hours%-%_minutes%-%_seconds%
Echo ################# Current time is %TIMEBLOCK%
Echo.
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" amd64
Echo.
Echo.
Echo -------------------------------------------- BASIC VENV SETUP --------------------------------------------
Echo.
Echo.
Echo ################# changing directory to %OLDHOME_FOLDER%
cd %OLDHOME_FOLDER%
Echo.
echo ################# suspending Dropbox
call pssuspend64 Dropbox
echo.
Echo ################# removing old venv folder
RD /S /Q ..\.venv
echo.

Echo ################# creating new venv folder
mkdir ..\.venv
echo.
Echo ################# calling venv module to initialize new venv
python -m venv ..\.venv
echo.

Echo ################# changing directory to ..\.venv
cd ..\.venv
echo.
Echo ################# activating venv for package installation
call .\Scripts\activate.bat
echo.

Echo ################# upgrading pip to get rid of stupid warning
call %OLDHOME_FOLDER%get-pip.py
echo.
echo.
echo.
Echo -------------------------------------------- INSTALLING PACKAGES --------------------------------------------
echo.
echo.
Echo +++++++++++++++++++++++++++++ Standard Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing Setuptools
call pip install --upgrade --pre setuptools
echo.
Echo ################# Installing pywin32
call pip install --upgrade --pre pywin32
echo.
Echo ################# Installing python-dotenv
call pip install --upgrade --pre python-dotenv
echo.
echo.
Echo +++++++++++++++++++++++++++++ Qt Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing PyQt5
call pip install --upgrade --pre PyQt5
echo.
Echo ################# Installing pyopengl
call pip install --upgrade --pre pyopengl
echo.
Echo ################# Installing PyQt3D
call pip install --upgrade --pre PyQt3D
echo.
Echo ################# Installing PyQtChart
call pip install --upgrade --pre PyQtChart
echo.
Echo ################# Installing PyQtDataVisualization
call pip install --upgrade --pre PyQtDataVisualization
echo.
Echo ################# Installing PyQtWebEngine
call pip install --upgrade --pre PyQtWebEngine
echo.
Echo ################# Installing pyqtgraph
call pip install --upgrade --pre pyqtgraph
echo.
Echo ################# Installing QScintilla
call pip install --upgrade --pre QScintilla
echo.

echo.

rem Echo +++++++++++++++++++++++++++++ Packages From Github +++++++++++++++++++++++++++++
rem echo.
rem Echo ################# Installing git+https://github.com/overfl0/Armaclass.git
rem call pip install --upgrade --pre git+https://github.com/overfl0/Armaclass.git
rem echo.
echo.

Echo +++++++++++++++++++++++++++++ Misc Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing pyperclip
call pip install --upgrade --pre pyperclip
echo.
Echo ################# Installing jinja2
call pip install --upgrade --pre jinja2
echo.
Echo ################# Installing bs4
call pip install --upgrade --pre bs4
echo.
Echo ################# Installing requests
call pip install --upgrade --pre requests
echo.
rem Echo ################# Installing PyGithub
rem call pip install --upgrade --pre PyGithub
rem echo.
Echo ################# Installing fuzzywuzzy
call pip install --upgrade --pre fuzzywuzzy
echo.
Echo ################# Installing fuzzysearch
call pip install --upgrade --pre fuzzysearch
echo.
Echo ################# Installing python-Levenshtein
call pip install --upgrade --pre python-Levenshtein
echo.
Echo ################# Installing jsonpickle
call pip install --upgrade --pre jsonpickle
echo.
rem Echo ################# Installing discord.py
rem call pip install --upgrade --pre discord.py
rem echo.
Echo ################# Installing regex
call pip install --upgrade --pre regex
echo.
Echo ################# Installing marshmallow
call pip install --upgrade --pre marshmallow
echo.
Echo ################# Installing click
call pip install --upgrade --pre click
echo.
Echo ################# Installing checksumdir
call pip install --upgrade --pre checksumdir
echo.
Echo ################# Installing pdfkit
call pip install --upgrade --pre pdfkit
echo.
rem Echo ################# Installing sip
rem call pip install --upgrade --pre --no-cache-dir --force-reinstall sip
rem echo.
rem Echo ################# Installing PyQt-builder
rem call pip install --upgrade --pre --no-cache-dir --force-reinstall PyQt-builder
rem echo.
rem Echo ################# Installing python-poppler-qt5
rem call pip install --upgrade --pre --no-cache-dir --force-reinstall git+https://github.com/mitya57/python-poppler-qt5.git@sip5
rem echo.
echo.
Echo +++++++++++++++++++++++++++++ Gid Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing flit
call pip install --force-reinstall --no-cache-dir --upgrade --pre flit
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils
pushd D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils
call flit install -s
popd
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidqtutils
call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidqtutils
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidlogger_rep
echo.

call pip install --force-reinstall --no-cache-dir --upgrade --pre gidlogger

echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Vscode_Wrapper
call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Vscode_Wrapper
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_View_models
call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_View_models
echo.
echo.

Echo ################# changing directory to %OLDHOME_FOLDER%
cd %OLDHOME_FOLDER%
echo.
rem Echo ################# writing ..\requirements_dev.txt
rem echo ########################################################## created at --^> %TIMEBLOCK% ##########################################################> ..\requirements_dev.txt
rem call pip freeze>>..\requirements_dev.txt
echo.
echo.
echo.
Echo +++++++++++++++++++++++++++++ Test Packages +++++++++++++++++++++++++++++
echo.

Echo ################# Installing pytest-qt
call pip install --upgrade --pre pytest-qt
echo.
Echo ################# Installing pytest
call pip install --upgrade --pre pytest
echo.

echo.
Echo +++++++++++++++++++++++++++++ Dev Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing wheel
call pip install --no-cache-dir --upgrade --pre wheel
echo.
Echo ################# Installing https://github.com/pyinstaller/pyinstaller/tarball/develop
call pip install --force-reinstall --no-cache-dir --upgrade --pre https://github.com/pyinstaller/pyinstaller/tarball/develop
echo.
Echo ################# Installing pep517
call pip install  --no-cache-dir --upgrade --pre pep517
echo.

Echo ################# Installing pyqt5-tools==5.15.1.1.7.5
call pip install --pre --upgrade --pre pyqt5-tools==5.15.1.1.7.5
echo.
Echo ################# Installing PyQt5-stubs
call pip install --upgrade --pre PyQt5-stubs
echo.


Echo ################# Installing pyqtdeploy
call pip install --upgrade --pre pyqtdeploy
echo.
rem Echo ################# Installing nuitka
rem call pip install --upgrade --pre nuitka
rem echo.
Echo ################# Installing memory-profiler
call pip install --upgrade --pre memory-profiler
echo.
Echo ################# Installing matplotlib
call pip install --upgrade --pre matplotlib
echo.
Echo ################# Installing import-profiler
call pip install --upgrade --pre import-profiler
echo.
Echo ################# Installing objectgraph
call pip install --upgrade --pre objectgraph
echo.
rem Echo ################# Installing pipreqs
rem call pip install --upgrade --pre pipreqs
rem echo.
rem Echo ################# Installing pydeps
rem call pip install --upgrade --pre pydeps
rem echo.
rem Echo ################# Installing bootstrap-discord-bot
rem call pip install --upgrade --pre bootstrap-discord-bot
rem echo.
rem echo.

echo -------------------calling pyqt5toolsinstalluic.exe-----------------------------
call ..\.venv\Scripts\pyqt5toolsinstalluic.exe
echo.
echo.

echo.
rem Echo ################# converting ..\requirements_dev.txt to ..\requirements.txt by calling %OLDHOME_FOLDER%convert_requirements_dev_to_normal.py
rem call %OLDHOME_FOLDER%convert_requirements_dev_to_normal.py
echo.
Echo INSTALL THE PACKAGE ITSELF AS -dev PACKAGE SO I DONT HAVE TO DEAL WITH RELATIVE PATHS
cd ..\
rem call pip install -e --upgrade --pre .
call flit --debug install -s
echo.
echo.
echo.
Echo setting modified env vars!!
call %OLDHOME_FOLDER%create_venv_extra_envvars.py %OLDHOME_FOLDER% pyqtsocius
echo.
Echo ################# restarting Dropbox
call pssuspend64 Dropbox -r
echo.

echo ###############################################################################################################
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ---------------------------------------------------------------------------------------------------------------
echo                                                     FINISHED
echo ---------------------------------------------------------------------------------------------------------------
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ###############################################################################################################
