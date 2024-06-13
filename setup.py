"""
Installation script for NetworkWrangler package
"""

import os
import setuptools

VERSION="1.5"

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
]

# long description from README.md
with open("README.md") as f:
    long_description = f.read()

# with open("requirements.txt") as f:
#     requirements = f.readlines()
# install_requires = [r.strip() for r in requirements]
install_requires = []

setuptools.setup(
    name                            = "NetworkWrangler",
    version                         = VERSION,
    description                     = "Wrangles networks for MTC Travel Model 1/1.5",
    long_description                = long_description,
    long_description_content_type   = "text/markdown",
    url                             = "https://github.com/BayAreaMetro/NetworkWrangler",
    license                         = "Apache 2",
    platforms                       = "any",
    packages                        = ["Wrangler"],
    include_package_data            = True,
    install_requires                = install_requires,
    scripts                         = [
        "scripts/build_network_mtc.py",
        "scripts/build_network_mtc_blueprint.py",
    ],
)