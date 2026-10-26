import os
import subprocess
import sys

# Define base path
base_path = "D:\\MemoryForensicsTool"

# Define subfolders
folders = [
    "volatility3",
    "dumps",
    "plugin_outputs",
    "scripts"
]

# Step 1: Create folders
print("[*] Creating project folders...")
for folder in folders:
    path = os.path.join(base_path, folder)
    os.makedirs(path, exist_ok=True)
    print(f"[+] Created: {path}")

# Step 2: Install Volatility3 using pip
print("\n[*] Installing Volatility3 from PyPI...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "volatility3"])
    print("[+] Volatility3 installed successfully!")
except subprocess.CalledProcessError:
    print("[-] Failed to install Volatility3. Please check your pip configuration.")

# Step 3: Confirm everything
print("\n[*] Setup complete.")
print(f"Your project base folder: {base_path}")
