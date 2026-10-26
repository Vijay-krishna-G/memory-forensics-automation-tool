import re

# === Paths to plugin outputs ===
pslist_path = "D:\\MemoryForensicsTool\\plugin_outputs\\windows_pslist.txt"
cmdline_path = "D:\\MemoryForensicsTool\\plugin_outputs\\windows_cmdline.txt"
output_path = "D:\\MemoryForensicsTool\\plugin_outputs\\ioc_report.txt"

# === IOCs to detect ===
suspicious_processes = ["mimikatz.exe", "DumpIt.exe", "powershell.exe", "cmd.exe"]
suspicious_cmd_keywords = ["EncodedCommand", "Base64", "bypass", "downloadstring", "iex", "Invoke-Expression"]

ioc_hits = []

# === Analyze pslist ===
with open(pslist_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()
    for line in lines:
        for proc in suspicious_processes:
            if proc.lower() in line.lower():
                ioc_hits.append(f"[pslist] Suspicious process found: {proc} --> {line.strip()}")

# === Analyze cmdline ===
with open(cmdline_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()
    for line in lines:
        for keyword in suspicious_cmd_keywords:
            if keyword.lower() in line.lower():
                ioc_hits.append(f"[cmdline] Suspicious command-line pattern ({keyword}): --> {line.strip()}")

# === Write IOC report ===
with open(output_path, "w", encoding="utf-8") as out:
    if ioc_hits:
        out.write("=== Suspicious Activity Detected ===\n\n")
        for hit in ioc_hits:
            out.write(hit + "\n")
    else:
        out.write("No suspicious processes or command-line patterns found.\n")

print(f"[+] IOC detection completed. Report saved to: {output_path}")
