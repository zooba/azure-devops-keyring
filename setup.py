#!/usr/bin/env python3

import os
import setuptools
import shutil
import sys
import tarfile
import tempfile
import urllib.request

CREDENTIAL_PROVIDER = (
    "https://github.com/Microsoft/artifacts-credprovider/releases/download/"
    + "v0.1.7"
    + "/Microsoft.NuGet.CredentialProvider.tar.gz"
)


def download_credential_provider(root):
    dest = os.path.join(root, "azure_devops_keyring", "plugins")

    if not os.path.isdir(dest):
        tmp = tempfile.mkdtemp()

        with urllib.request.urlopen(CREDENTIAL_PROVIDER) as fileobj:
            tar = tarfile.open(mode="r|gz", fileobj=fileobj)
            tar.extractall(tmp)

        shutil.copytree(os.path.join(tmp, "plugins"), dest)


if __name__ == "__main__":
    download_credential_provider(os.path.dirname(os.path.abspath(__file__)))
    setuptools.setup()
