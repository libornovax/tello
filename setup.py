#!/usr/bin/env python

from setuptools import setup, find_packages
from subprocess import check_output


def setup_package():

    # Determine package version from git
    version = check_output("git describe --tags --dirty".split()).decode('utf-8').strip()

    setup(

        # ----------------------------------- PACKAGE METADATA ----------------------------------- #

        name="tello",
        version=version,
        author="Libor Novak",
        author_email="libornovax@gmail.com",

        # --------------------------------- PACKAGE DEPENDENCIES --------------------------------- #

        install_requires=[
            "numpy",
        ],
        setup_requires=[
            "pytest-runner",
        ],
        tests_require=[
            "pytest",
            "pytest-cov",
        ],

        # ----------------------------------- PACKAGE CONTENTS ----------------------------------- #

        packages=find_packages("src"),
        package_dir={
            "": "src"
        },
        package_data={
        },

        # ----------------------------------- PACKAGE SCRIPTS ------------------------------------ #

        entry_points={
        }

    )


if __name__ == "__main__":
    setup_package()
