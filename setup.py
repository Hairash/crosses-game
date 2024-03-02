from setuptools import setup


setup(
    app=['main.py'],
    data_files=[],
    options={
        'py2app': {
            'iconfile': 'croco.icns',
            'argv_emulation': True,
            'packages': ['pygame'],
            'plist': {
                'CFBundleName': 'Croco game',
                'CFBundleDisplayName': 'Croco game',
                'CFBundleShortVersionString': '1.0.1',
                'CFBundleVersion': '1.0.1',
            },
        },
    },
    setup_requires=['py2app'],
)
