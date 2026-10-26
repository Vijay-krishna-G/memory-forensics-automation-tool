import os
import sys
from volatility3.cli import main
import contextlib

# Paths
memory_path = "D:\\MemoryForensicsTool\\dumps\\Challenges.raw"
output_path = "D:\\MemoryForensicsTool\\plugin_outputs\\windows_pslist.txt"
plugin_name = "windows.pslist"

# Redirect output to file
with open(output_path, "w", encoding="utf-8") as f:
    with contextlib.redirect_stdout(f):
        # Simulate CLI args
        sys.argv = [
            "volatility3",
            "-f", memory_path,
            plugin_name
        ]
        main()

print(f"[+] Plugin output saved to: {output_path}")
