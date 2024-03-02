# How to build app

## For MacOS
**Prepare to build**
1. Change version in setup.py
    ```
    'CFBundleShortVersionString': '1.0.1',
    'CFBundleVersion': '1.0.1',
    ```
1. Change icon, if needed
    `'iconfile': 'croco.icns',`

**Building**
1. Run py2app
    `python setup.py py2app`
1. Move all the game files (images, sounds) to the app


## For Windows
1. Run pyinstaller
    `pyinstaller --onefile --noconsole --icon=croco.ico main.py`
1. Move all the game files (images, sounds) to the the same folder as .exe file
1. Rename 'main.exe' -> 'Croco game.exe'
