# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import absolute_import

__author__ = "Steve Dower <steve.dower@microsoft.com>"
__version__ = "0.1.0"

import json
import subprocess
import sys
import warnings

from .support import urlsplit
from .plugin import CredentialProvider

import keyring.backend
import keyring.credentials


class AzureDevOpsKeyring(keyring.backend.KeyringBackend):
    SUPPORTED_NETLOC = frozenset(("dev.azure.com", "pkgs.dev.azure.com"))
    priority = 10

    def __init__(self):
        # In-memory cache of user-pass combination, to allow
        # fast handling of applications that insist on querying
        # username and password separately. get_password will
        # pop from this cache to avoid keeping the value
        # around for longer than necessary.
        self._cache = {}

    def get_credential(self, service, username):
        try:
            parsed = urlsplit(service)
        except Exception as exc:
            warnings.warn(str(exc))
            return None

        netloc = parsed.netloc.rpartition("@")[-1]
        if netloc not in self.SUPPORTED_NETLOC:
            return None

        with CredentialProvider() as provider:
            username, password = provider.get_credentials(service)

        if username and password:
            self._cache[service, username] = password
            return keyring.credentials.SimpleCredential(username, password)

    def get_password(self, service, username):
        password = self._cache.get((service, username), None)
        if password is not None:
            return password

        actual_username, password = self.get_username_and_password(service, None)
        if username == actual_username:
            return password

        return None

    def set_password(self, service, username, password):
        raise NotImplementedError()

    def delete_password(self, service, username):
        raise NotImplementedError()
