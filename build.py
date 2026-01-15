#!/usr/bin/env python3

import constants
import os
import subprocess
from pathlib import Path
from config import Config

config = Config(constants.CONFIG_PATH)

BUILD_CONFIG = {
    'app_name': 'autoupdate',
    'version': '0.1.0',
    'entry_point': 'autoupdate.py',
    
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
        ('data', 'data'),
        (Path(r'C:\Users\MyPC\AppData\Local\Programs\Python\Python314\Lib\site-packages\akshare\file_fold\*'), Path(r'akshare/file_fold'))
    ]
}

def build_from_config():
    cmd = ['pyinstaller']
    cmd.extend(['--name', f"{BUILD_CONFIG['app_name']}-{BUILD_CONFIG['version']}"])
    
    for item in BUILD_CONFIG['commands']:
        cmd.append(item)
        
    for item in BUILD_CONFIG['hidden_imports']:
        cmd.extend(['--hidden-import', item])
        
    for item in BUILD_CONFIG['datas']:
        source, destination = item
        cmd.extend(['--add-data', f"{source}{os.pathsep}{destination}"])
    
    cmd.append(BUILD_CONFIG['entry_point'])
    
    subprocess.run(cmd)
    # print(cmd)
    # print(cmd[-2])
    
build_from_config()