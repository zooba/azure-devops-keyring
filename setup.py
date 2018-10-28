#!/usr/bin/env python3

import os
import setuptools
import shutil
import sys
import tarfile
import tempfile
import urllib.request

CREDENTIAL_PROVIDER = (
    "https://github.com/Microsoft/artifacts-credprovider/releases/download/" +
    "v0.1.7" +
    "/Microsoft.NuGet.CredentialProvider.tar.gz"
)

name = 'azure-devops-keyring'
description = 'Automatically retrieve passwords for Azure DevOps.'
version = '0.2'

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
    package_data={},
)

if __name__ == '__main__':
    dest = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "azure_devops_keyring",
        "plugins"
    )
    
    if not os.path.isdir(dest):
        tmp = tempfile.mkdtemp()
        
        with urllib.request.urlopen(CREDENTIAL_PROVIDER) as fileobj:
            tar = tarfile.open(mode="r|gz", fileobj=fileobj)
            tar.extractall(tmp)

        shutil.copytree(os.path.join(tmp, "plugins"), dest)

    setuptools.setup(**params)
