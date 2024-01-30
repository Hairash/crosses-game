from setuptools import setup, find_packages

setup(
    name='croco-game',
    version='1.0.0',
    packages=find_packages(),
    package_data={
        'app': [
            'images/*.png',
            'images/labels/*.png',
            'images/digits/*.png',
            'sound/*.mp3',
        ],
    },
    install_requires=['pygame'],
    entry_points={
        'console_scripts': [
            'croco-game=app.main:main'
        ]
    },
)