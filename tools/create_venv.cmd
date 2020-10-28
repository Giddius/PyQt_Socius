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
call pip install setuptools
echo.
Echo ################# Installing pywin32
call pip install pywin32
echo.
Echo ################# Installing python-dotenv
call pip install python-dotenv
echo.
echo.
Echo +++++++++++++++++++++++++++++ Qt Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing PyQt5
call pip install PyQt5
echo.
Echo ################# Installing pyopengl
call pip install pyopengl
echo.
Echo ################# Installing PyQt3D
call pip install PyQt3D
echo.
Echo ################# Installing PyQtChart
call pip install PyQtChart
echo.
Echo ################# Installing PyQtDataVisualization
call pip install PyQtDataVisualization
echo.
Echo ################# Installing PyQtWebEngine
call pip install PyQtWebEngine
echo.
Echo ################# Installing pyqtgraph
call pip install pyqtgraph
echo.
Echo ################# Installing QScintilla
call pip install QScintilla
echo.
echo.

rem Echo +++++++++++++++++++++++++++++ Packages From Github +++++++++++++++++++++++++++++
rem echo.
rem Echo ################# Installing git+https://github.com/overfl0/Armaclass.git
rem call pip install git+https://github.com/overfl0/Armaclass.git
rem echo.
echo.

Echo +++++++++++++++++++++++++++++ Misc Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing pyperclip
call pip install pyperclip
echo.
Echo ################# Installing jinja2
call pip install jinja2
echo.
Echo ################# Installing bs4
call pip install bs4
echo.
Echo ################# Installing requests
call pip install requests
echo.
rem Echo ################# Installing PyGithub
rem call pip install PyGithub
rem echo.
Echo ################# Installing fuzzywuzzy
call pip install fuzzywuzzy
echo.
Echo ################# Installing fuzzysearch
call pip install fuzzysearch
echo.
Echo ################# Installing python-Levenshtein
call pip install python-Levenshtein
echo.
Echo ################# Installing jsonpickle
call pip install jsonpickle
echo.
rem Echo ################# Installing discord.py
rem call pip install discord.py
rem echo.
Echo ################# Installing regex
call pip install regex
echo.
Echo ################# Installing marshmallow
call pip install marshmallow
echo.
Echo ################# Installing click
call pip install click
echo.
Echo ################# Installing checksumdir
call pip install checksumdir
echo.

echo.
Echo +++++++++++++++++++++++++++++ Gid Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidqtutils
call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidqtutils
echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidlogger_rep

call pip install gidlogger

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
Echo ################# writing ..\requirements_dev.txt
echo ########################################################## created at --^> %TIMEBLOCK% ##########################################################> ..\requirements_dev.txt
call pip freeze >> ..\requirements_dev.txt
echo.
echo.
echo.
Echo +++++++++++++++++++++++++++++ Test Packages +++++++++++++++++++++++++++++
echo.

Echo ################# Installing pytest-qt
call pip install pytest-qt
echo.
Echo ################# Installing pytest
call pip install pytest
echo.

echo.
Echo +++++++++++++++++++++++++++++ Dev Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing wheel
call pip install --no-cache-dir wheel
echo.
Echo ################# Installing https://github.com/pyinstaller/pyinstaller/tarball/develop
call pip install --force-reinstall --no-cache-dir https://github.com/pyinstaller/pyinstaller/tarball/develop
echo.
Echo ################# Installing pep517
call pip install  --no-cache-dir pep517
echo.
Echo ################# Installing flit
call pip install --force-reinstall --no-cache-dir flit
echo.
Echo ################# Installing pyqt5-tools==5.15.1.1.7.5
call pip install --pre pyqt5-tools==5.15.1.1.7.5
echo.
Echo ################# Installing PyQt5-stubs
call pip install PyQt5-stubs
echo.
Echo ################# Installing sip
call pip install sip
echo.
Echo ################# Installing PyQt-builder
call pip install PyQt-builder
echo.
Echo ################# Installing pyqtdeploy
call pip install pyqtdeploy
echo.
rem Echo ################# Installing nuitka
rem call pip install nuitka
rem echo.
rem Echo ################# Installing memory-profiler
rem call pip install memory-profiler
rem echo.
rem Echo ################# Installing matplotlib
rem call pip install matplotlib
rem echo.
rem Echo ################# Installing import-profiler
rem call pip install import-profiler
rem echo.
rem Echo ################# Installing objectgraph
rem call pip install objectgraph
rem echo.
rem Echo ################# Installing pipreqs
rem call pip install pipreqs
rem echo.
rem Echo ################# Installing pydeps
rem call pip install pydeps
rem echo.
rem Echo ################# Installing bootstrap-discord-bot
rem call pip install bootstrap-discord-bot
rem echo.
rem echo.

echo -------------------calling pyqt5toolsinstalluic.exe-----------------------------
call ..\.venv\Scripts\pyqt5toolsinstalluic.exe
echo.
echo.

echo.
Echo ################# converting ..\requirements_dev.txt to ..\requirements.txt by calling %OLDHOME_FOLDER%convert_requirements_dev_to_normal.py
call %OLDHOME_FOLDER%convert_requirements_dev_to_normal.py
echo.
Echo INSTALL THE PACKAGE ITSELF AS -dev PACKAGE SO I DONT HAVE TO DEAL WITH RELATIVE PATHS
cd ..\
call pip install -e .
rem call flit install -s
echo.
echo.
echo.
Echo ################# restarting Dropbox
call pssuspend64 Dropbox -r
echo.
Echo ################# telling dropbox to leave .venv out of it
call D:\Dropbox\hobby\Modding\Ressources\VScode_task_files\python_files\tell_dropbox_to_eat_shit.py
echo.
echo ###############################################################################################################
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ---------------------------------------------------------------------------------------------------------------
echo                                                     FINISHED
echo ---------------------------------------------------------------------------------------------------------------
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ###############################################################################################################
