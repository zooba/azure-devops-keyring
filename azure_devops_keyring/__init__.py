# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

__author__ = "Steve Dower <steve.dower@microsoft.com>"
__version__ = "0.1.0"

import json
import urllib.parse
import subprocess
import sys
import warnings

import keyring.backend
import keyring.credentials

try:
    from importlib_resources import path as path_in_package
except ImportError:
    from importlib.resources import path as path_in_package


class AzureDevOpsKeyring(keyring.backend.KeyringBackend):
    SUPPORTED_NETLOC = frozenset(("dev.azure.com", "pkgs.dev.azure.com"))

    def __init__(self):
        # In-memory cache of user-pass combination, to allow
        # fast handling of applications that insist on querying
        # username and password separately. get_password will
        # pop from this cache to avoid keeping the value
        # around for longer than necessary.
        self._cache = {}

    @property
    def priority(self):
        return 10

    def _get_win32(self, service):
        with path_in_package(__name__, "CredentialProvider.VSS.exe") as f:
            with subprocess.Popen(
                [str(f), "-N", "-U", service],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ) as proc:
                proc.wait()
                data = json.load(proc.stdout)
                if proc.returncode != 0:
                    return None
        username, password = data["Username"], data["Password"]
        self._cache[service, username] = password
        return keyring.credentials.SimpleCredential(username, password)

    def get_credential(self, service, username):
        try:
            parsed = urllib.parse.urlsplit(service)
        except Exception as exc:
            warnings.warn(str(exc))
            return None

        if parsed.netloc not in self.SUPPORTED_NETLOC:
            return None

        if sys.platform == "win32":
            return self._get_win32(service)

        warnings.warn("Unsupported platform: " + sys.platform)
        return None

    def get_password(self, service, username):
        password = self._cache.get((service, username), None)
        if password is not None:
            return password

        actual_username, password = self.get_username_and_password(service, None)
        if username == actual_username:
            return password

        return None

    def set_password(self, service, username, password):
        pass
