#!/usr/bin/env python3

import os


startup_executables = [
    r'"C:\Users\jguzman2\OneDrive - Infor\Desktop\workdump\keys.ahk"',
    r'"C:\Users\jguzman2\AppData\Local\MyEclipse 2017 CI\myeclipse.exe"',
    r'"C:\Program Files\internet explorer\iexplore.exe"',
    r'"C:\Program Files (x86)\Microsoft Office\root\Office16\lync.exe"',
    r'"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE"',
    r'"C:\Program Files\Sublime Text 3\sublime_text.exe"',
    r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"',
    r'"C:\Users\jguzman2\AppData\Local\SourceTree\app-2.5.5\SourceTree.exe"',
    #r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --app=https://www.xodo.com/app/#/pdf',
    #r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --app=https://evernote.com/'
    #r"C:\Program Files (x86)\Microsoft SQL Server\120\Tools\Binn\ManagementStudio\Ssms.exe",
    #r"C:\Users\jguzman2\OneDrive - Infor\Downloads\jptemp\dbvis_windows-x64_10_0_6\DbVisualizer\dbvis.exe",
]

for exe in startup_executables: # startup_executables[-2:]
    print(exe)
    os.startfile(exe)
input("Finishes running commands. Press Enter to continue...")
