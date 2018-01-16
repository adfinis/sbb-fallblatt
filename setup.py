import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="sbb_fallblatt",
    version="0.0.0",
    author="Adfinis SyGroup",
    author_email="info@adfinis-sygroup.ch",
    description="Code and documentation for SBB split flap displays",
    license="MIT",
    keywords="sbb train display",
    url="https://github.com/eni23/sbb-fallblatt",
    packages=['sbb_fallblatt'],
    long_description=read('README.md'),
    install_requires=[
      "pyserial"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
)
