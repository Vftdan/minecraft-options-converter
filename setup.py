#! /usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='minecraft-options-converter',
    version='0.0.2',
    description='Minecraft options.txt keycode converter',
    author='Vftdan',
    packages=find_packages(),
    entry_points={
        'console_scripts': 'minecraft-options-converter = minecraft_options_converter:main'
    }
)
