import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="sbb_fallblatt",
    version="0.0.0",
    author="Adfinis",
    author_email="support@adfinis.com",
    description="Code and documentation for SBB split flap displays",
    license="GNU General Public License v3 (GPLv3)",
    keywords="sbb train display",
    url="https://github.com/adfinis/sbb-fallblatt",
    packages=['sbb_fallblatt'],
    long_description=read('README.md'),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
