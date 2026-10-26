import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os
import sys
import csv


import fitz  # PyMuPDF (currently unused, kept for future internal viewer)
from PIL import Image, ImageTk

# =========================
#  HARD-CODED LOGIN CREDS
# =========================
from dotenv import load_dotenv

load_dotenv()

VALID_USERNAME = os.getenv("VALID_USERNAME")
VALID_PASSWORD = os.getenv("VALID_PASSWORD")

# Path to your fixed dump file
DUMP_PATH = os.path.join("dumps", "Challenges.raw")


# =========================
#  CORE ANALYSIS FUNCTIONS
# =========================

def run_all_plugins():
    """Run all Volatility plugins via helper script."""
    try:
        subprocess.run(
    [sys.executable, "scripts/run_all_plugins.py"],
    check=True
)
        messagebox.showinfo("Success", "All plugins executed and outputs saved.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to run plugins.")


def run_ioc_detector():
    """Run custom IOC detector."""
    try:
        subprocess.run(["python", "scripts/ioc_detector.py"], check=True)
        messagebox.showinfo("Success", "IOC detection completed.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to run IOC detector.")


def generate_pdf():
    """Generate PDF report from HTML using html_to_pdf.py."""
    try:
        subprocess.run(
    [sys.executable, "scripts/html_to_pdf.py"],
    check=True
)
        messagebox.showinfo("Success", "PDF report generated successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to generate PDF report.")


def open_pdf_external():
    """Open the generated PDF in the system's default PDF viewer."""
    pdf_path = r"D:\MemoryForensicsTool\plugin_outputs\forensics_report.pdf"

    if not os.path.exists(pdf_path):
        messagebox.showerror("Error", "PDF report not found. Please generate it first.")
        return

    try:
        os.startfile(pdf_path)  # Windows default PDF viewer
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open PDF externally: {e}")


def view_output_file(file_path, title):
    """Open a new window and show the content of a text output file."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        output_win = tk.Toplevel()
        output_win.title(title)

        text_area = scrolledtext.ScrolledText(output_win, wrap=tk.WORD, width=100, height=30)
        text_area.pack(padx=10, pady=10)
        text_area.insert(tk.END, content)
        text_area.config(state="disabled")

    except FileNotFoundError:
        messagebox.showerror("Error", f"{title} file not found.")


def export_txt_to_csv(txt_path, csv_path):
    """Simple TXT → CSV conversion: each line becomes one cell/row."""
    if not os.path.exists(txt_path):
        print(f"[!] Skipping, not found: {txt_path}")
        return

    with open(txt_path, "r", encoding="utf-8", errors="ignore") as f_in:
        lines = [ln.strip() for ln in f_in.readlines()]

    with open(csv_path, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        for line in lines:
            writer.writerow([line])

    print(f"[+] Exported: {csv_path}")


def export_csv_from_gui():
    """Export all main TXT outputs to CSV in plugin_outputs folder."""
    try:
        mapping = {
            "plugin_outputs/windows_pslist.txt": "plugin_outputs/windows_pslist.csv",
            "plugin_outputs/windows_cmdline.txt": "plugin_outputs/windows_cmdline.csv",
            "plugin_outputs/windows_netscan.txt": "plugin_outputs/windows_netscan.csv",
            "plugin_outputs/windows_malfind.txt": "plugin_outputs/windows_malfind.csv",
            "plugin_outputs/windows_filescan.txt": "plugin_outputs/windows_filescan.csv",
            "plugin_outputs/ioc_report.txt": "plugin_outputs/ioc_report.csv",
        }

        for txt_path, csv_path in mapping.items():
            export_txt_to_csv(txt_path, csv_path)

        messagebox.showinfo("Success", "All TXT outputs exported to CSV.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export CSV: {e}")


# =========================
#  MAIN ANALYSIS GUI
# =========================

def build_main_gui(root):
    """Build the main Cyber Forensics Analysis Tool interface."""
    # Clear previous widgets (case manager)
    for widget in root.winfo_children():
        widget.destroy()

    root.title("🔍 Memory Forensics GUI Tool")
    root.geometry("500x650")
    root.config(bg="#e8f0fe")

    title_label = tk.Label(
        root,
        text="🔬 Cyber Forensics Analysis Tool",
        font=("Helvetica", 16, "bold"),
        bg="#e8f0fe",
        pady=20,
    )
    title_label.pack()

    buttons = [
        ("▶️ Run All Plugins", run_all_plugins),
        ("🚨 Run IOC Detector", run_ioc_detector),
        ("📜 View pslist", lambda: view_output_file("plugin_outputs/windows_pslist.txt", "Process List")),
        ("📜 View cmdline", lambda: view_output_file("plugin_outputs/windows_cmdline.txt", "Command Line")),
        ("📜 View netscan", lambda: view_output_file("plugin_outputs/windows_netscan.txt", "Network Scan")),
        ("📜 View IOC Report", lambda: view_output_file("plugin_outputs/ioc_report.txt", "IOC Report")),
        ("📝 Generate PDF Report", generate_pdf),
        ("📄 Report View", open_pdf_external),
        ("📥 Export CSV", export_csv_from_gui),
    ]

    for text, command in buttons:
        tk.Button(
            root,
            text=text,
            command=command,
            width=40,
            height=2,
            bg="#007acc",
            fg="white",
            font=("Helvetica", 10, "bold"),
        ).pack(pady=5)


# =========================
#  AUTOPSY-STYLE CASE MANAGER
# =========================

def open_single_case(root):
    """Handle 'Open Case' – here we always use the fixed Challenges.raw."""
    if not os.path.exists(DUMP_PATH):
        messagebox.showerror(
            "Error",
            f"Memory dump not found at:\n{os.path.abspath(DUMP_PATH)}\n\n"
            "Please ensure Challenges.raw is in the dumps/ folder."
        )
        return

    # Optional: show simple info for viva
    info = (
        f"Using memory dump:\n{os.path.abspath(DUMP_PATH)}\n\n"
        "This tool will run Volatility3 plugins on this file."
    )
    messagebox.showinfo("Case Loaded", info)

    # Now go to main analysis GUI
    build_main_gui(root)


def build_case_manager(root):
    """Autopsy-style case manager with New / Open Recent / Open Case."""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("🧠 Memory Forensics Case Manager")
    root.geometry("500x400")
    root.config(bg="#e8f0fe")

    title_label = tk.Label(
        root,
        text="🧠 Memory Forensics Case Manager",
        font=("Helvetica", 16, "bold"),
        bg="#e8f0fe",
        pady=20,
    )
    title_label.pack()

    # Center container
    frame = tk.Frame(root, bg="#e8f0fe")
    frame.pack(expand=True)

    # Autopsy-style large buttons
    btn_new = tk.Button(
        frame,
        text="🆕 New Case (Disabled)",
        width=30,
        height=2,
        bg="#b0c4de",
        fg="white",
        font=("Helvetica", 11, "bold"),
        state=tk.DISABLED,  # feature not implemented yet
    )
    btn_new.pack(pady=10)

    btn_recent = tk.Button(
        frame,
        text="🕘 Open Recent Case (Disabled)",
        width=30,
        height=2,
        bg="#b0c4de",
        fg="white",
        font=("Helvetica", 11, "bold"),
        state=tk.DISABLED,  # feature not implemented yet
    )
    btn_recent.pack(pady=10)

    btn_open = tk.Button(
        frame,
        text="📂 Open Case (Challenges.raw)",
        width=30,
        height=2,
        bg="#007acc",
        fg="white",
        font=("Helvetica", 11, "bold"),
        command=lambda: open_single_case(root),
    )
    btn_open.pack(pady=10)

    # Small note at bottom
    note = tk.Label(
        root,
        text="Note: This prototype uses a fixed memory image: dumps/Challenges.raw",
        bg="#e8f0fe",
        fg="#555555",
        font=("Helvetica", 9),
    )
    note.pack(pady=(0, 10))


# =========================
#  LOGIN SCREEN
# =========================

def build_login_screen(root):
    root.title("🔐 Memory Forensics - Login")
    root.geometry("400x260")
    root.config(bg="#e8f0fe")

    login_frame = tk.Frame(root, bg="#e8f0fe")
    login_frame.pack(expand=True)

    title = tk.Label(
        login_frame,
        text="🔐 Investigator Login",
        font=("Helvetica", 16, "bold"),
        bg="#e8f0fe",
        pady=10,
    )
    title.pack()

    user_label = tk.Label(login_frame, text="Username:", font=("Helvetica", 11), bg="#e8f0fe")
    user_label.pack(pady=(20, 5))
    user_entry = tk.Entry(login_frame, width=30)
    user_entry.pack()

    pass_label = tk.Label(login_frame, text="Password:", font=("Helvetica", 11), bg="#e8f0fe")
    pass_label.pack(pady=(15, 5))
    pass_entry = tk.Entry(login_frame, width=30, show="*")
    pass_entry.pack()

    def attempt_login(event=None):
        username = user_entry.get().strip()
        password = pass_entry.get().strip()

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            # On successful login, go to Case Manager (Autopsy-style)
            build_case_manager(root)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    login_button = tk.Button(
        login_frame,
        text="Sign In",
        command=attempt_login,
        width=15,
        height=2,
        bg="#007acc",
        fg="white",
        font=("Helvetica", 10, "bold"),
    )
    login_button.pack(pady=20)

    # Press Enter to sign in
    root.bind("<Return>", attempt_login)


# =========================
#  APP START
# =========================

if __name__ == "__main__":
    root = tk.Tk()
    build_login_screen(root)
    root.mainloop()
