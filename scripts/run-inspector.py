#!/usr/bin/env python3
"""Simple wrapper to run the MCP server for the inspector."""
import os
import sys

os.environ["MCP_NO_BANNER"] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pluggedin_random_number_generator_mcp.server import main
main()