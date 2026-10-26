import os
import sys
from volatility3.cli import main

# Set path to memory dump
memory_path = "D:\\MemoryForensicsTool\\dumps\\Challenges.raw"

# Plugin to run
plugin_name = "windows.pslist"

# Set sys.argv to simulate command line
sys.argv = [
    "volatility3",             # Script name (required placeholder)
    "-f", memory_path,         # Memory dump file
    plugin_name                # Volatility plugin
]

# Run the plugin
if __name__ == "__main__":
    main()
