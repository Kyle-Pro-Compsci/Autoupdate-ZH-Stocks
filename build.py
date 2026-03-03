#!/usr/bin/env python3

from src import constants
import os
import subprocess
from pathlib import Path

# AFTER BUILDING : MOVE data folder and config.json from _internal to the main folder
BUILD_CONFIG = {
    'app_name': 'autoupdate_gui',
    'entry_point': (Path('src/gui.py')),
    
    'commands': [
        '--onedir',
        '--console',
        '--clean'
    ],
    'hidden_imports': [
        'pandas',
        'numpy',
        'requests'
    ],
    'datas': [
        (Path('src/data'), 'data'),
        (Path(r'C:\Users\MyPC\AppData\Local\Programs\Python\Python314\Lib\site-packages\akshare\file_fold\*'), Path(r'akshare/file_fold')),
        (Path('src/config.json'), '.')
    ],
    'exclusions': [
        'QtQuick',
        'QtPdf',
        'QtQml',
        'QtNetwork',
        'QtSvg'
    ],
    'UPX_path': (Path(r'D:\upx-5.1.0-win64'))
} # Maybe should delete datas - need to take data folder and config.json out manually after building - or setup MEIPASS

def build_from_config():
    cmd = ['pyinstaller']
    cmd.extend(['--name', BUILD_CONFIG['app_name']])
    
    for item in BUILD_CONFIG['commands']:
        cmd.append(item)
        
    for item in BUILD_CONFIG['hidden_imports']:
        cmd.extend(['--hidden-import', item])
        
    for item in BUILD_CONFIG['datas']:
        source, destination = item
        cmd.extend(['--add-data', f"{source}{os.pathsep}{destination}"])
    
    for item in BUILD_CONFIG['exclusions']:
        cmd.append(f'--exclude-module={item}')
        
    cmd.append(BUILD_CONFIG['entry_point'])
    
    cmd.append(f'--upx-dir={BUILD_CONFIG["UPX_path"]}')
    
    subprocess.run(cmd)
    
build_from_config()