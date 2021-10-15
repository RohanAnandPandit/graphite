import os
from utils import NAME, FONT_NAME, IMAGES

commands = [
    'pyinstaller --onefile main.py',  # Creates executable in dist folder
    'rmdir /s /q build',  # Deletes build folder
    'cd dist && ren main.exe ' + NAME.lower() + '.exe && cd ..',  # Renames executable
    'if exist ' + NAME + ' rmdir /s /q ' + NAME,  # Deletes previous folder
    'ren dist ' + NAME,  # Renames dist folder
    'cd ' + NAME + ' && mkdir ' + IMAGES + ' && cd ..',  # Creates folder for modules,
    'robocopy ' + IMAGES + ' ' + NAME + '/' + IMAGES,  # Copies images folder
    'copy ' + FONT_NAME + ' ' + NAME,  # Copies all module files
]

for cmd in commands:
    os.system(cmd)
