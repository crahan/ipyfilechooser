#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ipyfilechooser",
    version="0.1.2",
    author="Thomas Bouve (@crahan)",
    author_email="crahan@n00.be",
    description=(
        "Python file chooser widget for use in "
        "Jupyter/IPython in conjunction with ipywidgets"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crahan/ipyfilechooser",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    install_requires=[
        'ipywidgets'
    ]
)
