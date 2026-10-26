from datetime import datetime 

# Define plugin output paths
plugins = {
    "pslist": "plugin_outputs/windows_pslist.txt",
    "cmdline": "plugin_outputs/windows_cmdline.txt",
    "netscan": "plugin_outputs/windows_netscan.txt",
    "malfind": "plugin_outputs/windows_malfind.txt",
    "filescan": "plugin_outputs/windows_filescan.txt",
    "ioc": "plugin_outputs/ioc_report.txt"
}

# Start HTML with date formatting included immediately
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Memory Forensics Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #ccc; padding-bottom: 5px; margin-top: 40px; }}
        pre {{ background-color: #fff; padding: 10px; border: 1px solid #ccc; overflow-x: auto; white-space: pre-wrap; }}
        .section {{ margin-bottom: 30px; }}
        .summary {{ font-size: 14px; color: #555; margin-bottom: 10px; }}
    </style>
</head>
<body>
    <h1>🧠 Memory Forensics Analysis Report</h1>
    <p><strong>Generated on:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
"""

# Add plugin contents
for plugin, path in plugins.items():
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            lines = content.splitlines()
            count = len(lines) - 2 if len(lines) > 2 else 0
            html_content += f"""
    <div class="section">
        <h2>{plugin.capitalize()} Results</h2>
        <div class="summary">📝 Total entries: {count}</div>
        <pre>{content}</pre>
    </div>
"""
    except FileNotFoundError:
        html_content += f"""
    <div class="section">
        <h2>{plugin.capitalize()} Results</h2>
        <div class="summary">⚠️ File not found: {path}</div>
    </div>
"""

# End HTML
html_content += """
</body>
</html>
"""

# Save the final HTML report
with open("plugin_outputs/forensics_report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("[+] HTML report generated: plugin_outputs/forensics_report.html")
