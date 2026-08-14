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
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.10",
]

# long description from README.md
with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.readlines()
install_requires = [r.strip() for r in requirements]

setuptools.setup(
    name                            = "NetworkWrangler",
    version                         = VERSION,
    description                     = "Wrangles networks for MTC Travel Model 1/1.5",
    long_description                = long_description,
    long_description_content_type   = "text/markdown",
    url                             = "https://github.com/BayAreaMetro/NetworkWrangler",
    license                         = "Apache 2",
    platforms                       = "any",
    # `_static` has to ship: Wrangler/__init__.py adds it to sys.path and
    # TransitAssignmentData.py imports dataTable from it, so leaving it out means
    # `import Wrangler` fails on any non-editable install.
    #
    # Short-term fix.  `_static` is conventionally for build output and static assets,
    # not source -- dataTable.py and odict.py belong inside Wrangler/ as ordinary
    # submodules with relative imports.  Promoting them breaks callers that do
    # `from dataTable import ...`, so it wants coordinating rather than dropping in.
    packages                        = ["Wrangler", "_static"],
    include_package_data            = True,
    install_requires                = install_requires,
    scripts                         = [
        "scripts/build_network_mtc.py",
        "scripts/build_network_mtc_blueprint.py",
    ],
)