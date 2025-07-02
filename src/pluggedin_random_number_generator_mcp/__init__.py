"""Plugged.in Random Number Generator MCP Server (Python).

A cryptographically secure random number generator implementing the Model Context Protocol.
"""

__version__ = "1.0.0"
__author__ = "VeriTeknik"
__email__ = "cem@plugged.in"

from .server import RandomNumberGeneratorMCP, main

__all__ = ["RandomNumberGeneratorMCP", "main", "__version__"]