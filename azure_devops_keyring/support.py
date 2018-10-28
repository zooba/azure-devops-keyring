# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""Helper imports for the Azure DevOps Keyring module.
"""

# *********************************************************
# Import the correct urlsplit function

try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit


# *********************************************************
# Import (and possible update) subprocess.Popen

from subprocess import Popen

if not hasattr(Popen, "__enter__"):
    # Handle Python 2.x not making Popen a context manager
    class Popen(Popen):
        def __enter__(self):
            return self

        def __exit__(self, ex_type, ex_value, ex_tb):
            pass

# *********************************************************
# Import (or possibly define) path_in_package

def _make_path_in_package_from_pkgutil():
    try:
        from importlib_resources import path as path_in_package
        return path_in_package
    except ImportError:
        pass

    try:
        from importlib.resources import path as path_in_package
        return path_in_package
    except ImportError:
        pass

    import contextlib
    import os
    import pkgutil
    import tempfile

    @contextlib.contextmanager
    def path_in_package(package, resource):
        data = pkgutil.get_data(package, resource)
        tmp = tempfile.mkdtemp()
        pth = os.path.join(tmp, resource)
        try:
            with open(pth, "wb") as f:
                f.write(data)
            yield pth
        finally:
            try:
                os.path.unlink(pth)
                os.path.rmdir(tmp)
            except:
                pass

    return path_in_package


path_in_package = _make_path_in_package_from_pkgutil()
