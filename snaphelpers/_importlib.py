# Copyright Alberto Donato 2019, 2026
# SPDX-License-Identifier: LGPL-3.0-or-later

# Compatibility wrapper for importlib.metadata

import sys

if sys.version_info < (3, 10):
    from importlib_metadata import (
        entry_points,
        EntryPoint,
        EntryPoints,
    )
else:
    from importlib.metadata import (
        entry_points,
        EntryPoint,
        EntryPoints,
    )

__all__ = ["entry_points", "EntryPoint", "EntryPoints"]
