"""Public API surface for :mod:`plant_layout`.

This package provides utilities for generating plant placement layouts. The
primary entry point is :func:`run_layout` which is re-exported here for
convenient access.
"""

from .service import run_layout

__all__ = ["run_layout"]
