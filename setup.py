#!/usr/bin/env python3

import setuptools
import sys

name = 'azure-devops-keyring'
description = 'Automatically retrieve passwords for Azure DevOps.'
version = '0.1.0'

params = dict(
    name=name,
    version=version,
    author="Microsoft Corporation",
    author_email="python@microsoft.com",
    description=description or name,
    url="https://github.com/Microsoft/azure-devops-keyring",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        'keyring.backends': [
            'AzureDevOpsKeyring = azure_devops_keyring:AzureDevOpsKeyring',
        ],
    },
    package_data={
        'azure_devops_keyring': [
            'CredentialProvider.VSS.exe',
        ],
    },
)

if __name__ == '__main__':
    setuptools.setup(**params)
