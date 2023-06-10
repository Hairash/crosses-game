from setuptools import setup


setup(
    app=['main.py'],
    data_files=[],
    options={
        'py2app': {
            'iconfile': 'croco.icns',
            'argv_emulation': True,
            'packages': ['pygame'],
        },
    },
    setup_requires=['py2app'],
)
