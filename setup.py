#!/usr/bin/env python3

import setuptools
import sys

name = 'azure-artifacts-keyring'
description = 'Automatically retrieve passwords for Azure Artifacts.'
version = '0.1.0'

params = dict(
    name=name,
    version=version,
    author="Microsoft Corporation",
    author_email="python@microsoft.com",
    description=description or name,
    url="https://github.com/Microsoft/azure-artifacts-keyring",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'keyring',
        'importlib_resources',
    ],
    extras_require={
    },
    setup_requires=[
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        'keyring.backends': [
            'AzureArtifacts = azure_artifacts_keyring:AzureArtifactsKeyring',
        ],
    },
    package_data={
        'azure_artifacts_keyring': ['CredentialProvider.VSS.exe'],
    },
)

if __name__ == '__main__':
    setuptools.setup(**params)
