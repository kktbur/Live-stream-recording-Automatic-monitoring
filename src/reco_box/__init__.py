"""Reco Box desktop application."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as distribution_version

try:
    __version__ = distribution_version("reco-box")
except PackageNotFoundError:
    __version__ = "0+unknown"
