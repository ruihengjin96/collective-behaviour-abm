#! /usr/bin/env python

from setuptools import setup

# Project metadata
DESCRIPTION = "An interactive toolkit for agent-based modelling"
DISTNAME = ""
URL = "https://github.com/ruihengjin96/collective-behaviour-abm"
DOWNLOAD_URL = "https://github.com/ruihengjin96/collective-behaviour-abm"

# Setup
if __name__ == "__main__":
       setup(
        version="0.0.1",
        description=DESCRIPTION,
        url=URL,
        download_url=DOWNLOAD_URL,
        license="Apache-2.0",
        platforms=["Windows", "Linux", "Mac OS-X"],
        install_requires=[],
        classifiers=[
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
            "Topic :: Scientific/Engineering :: Visualization",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: MacOS",
        ],
       )
