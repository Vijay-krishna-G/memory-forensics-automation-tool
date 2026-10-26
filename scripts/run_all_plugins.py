import os
import sys
import contextlib
from volatility3.cli import main

# === Paths ===
dump_path = "D:\\MemoryForensicsTool\\dumps\\Challenges.raw"
output_dir = "D:\\MemoryForensicsTool\\plugin_outputs"

# === Plugins to Run ===
plugins = {
    "windows.pslist": "windows_pslist.txt",
    "windows.cmdline": "windows_cmdline.txt",
    "windows.netscan": "windows_netscan.txt",
    "windows.malfind": "windows_malfind.txt",
    "windows.filescan": "windows_filescan.txt"
}

# === Run Each Plugin ===
for plugin, filename in plugins.items():
    output_path = os.path.join(output_dir, filename)

    print(f"[*] Running plugin: {plugin}")
    
    with open(output_path, "w", encoding="utf-8") as f:
        with contextlib.redirect_stdout(f):
            sys.argv = ["volatility3", "-f", dump_path, plugin]
            try:
                main()
            except Exception as e:
                print(f"[!] Error running {plugin}: {str(e)}")
    
    print(f"[+] Output saved to: {output_path}")

print("\n✅ All plugins completed. Report ready.")
