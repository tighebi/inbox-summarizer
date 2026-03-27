import tkinter as tk
from tkinter import messagebox
import yaml
import subprocess
import sys
import os
import platform
from imapclient import IMAPClient

# path to where repo is clone
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = sys.executable

# information
def validate_and_submit(email, password, api_key, window):
    if not email or not password or not api_key:
        messagebox.showerror("Error", "All fields are required.")
        return
    # connecting to Gmail with details and error catches
    try:
        client = IMAPClient("imap.gmail.com", ssl=True)
        client.login(email, password)
        client.logout()
    except Exception as e:
        error = str(e).lower()
        if "application-specific password required" in error:
            messagebox.showerror("Error", "Gmail requires an App Password, not your real password.\nGenerate one at myaccount.google.com/apppasswords")
        elif "invalid credentials" in error:
            messagebox.showerror("Error", "Could not connect. Double check your email and App Password.")
        elif "web login required" in error or "managed" in error:
            messagebox.showerror("Error", "This looks like a managed Google account (e.g. .edu).\nPlease use a personal Gmail account.")
        else:
            messagebox.showerror("Error", f"Connection failed: {e}")
        return
    # success means writing config  and install service
    write_config(email, password, api_key)
    install_service()
    window.destroy()
    messagebox.showinfo("All done", "Inbox Summarizer is now running.\nYou'll see a popup when new emails arrive.")

# writes the yaml file with its values and chmod for safety if needed
def write_config(email, password, api_key):
    config = {
        "email": {
            "host": "imap.gmail.com",
            "port": 993,
            "username": email,
            "password": password
        },
        "gemini": {
            "api_key": api_key
        }
    }
    config_path = os.path.join(REPO_DIR, "config.yaml")
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    
    # lock down the file on Linux/macOS
    if platform.system() != "Windows":
        os.chmod(config_path, 0o600)

# detect OS and install
def install_service():
    system = platform.system()
    # one for Linux, mac, and windows
    if system == "Linux":
        install_linux()
    elif system == "Darwin":
        install_macos()
    elif system == "Windows":
        install_windows()

# process for linux
def install_linux():
    # creates file in system
    service_dir = os.path.expanduser("~/.config/systemd/user/")
    os.makedirs(service_dir, exist_ok=True)

    # writes to file in system 
    service_content = f"""[Unit]
Description=Inbox Summarizer

[Service]
ExecStart={VENV_PYTHON} {os.path.join(REPO_DIR, "main.py")}
WorkingDirectory={REPO_DIR}
Environment="DISPLAY=:0"
Environment="XAUTHORITY=%h/.Xauthority"
Restart=on-failure

[Install]
WantedBy=default.target
"""
    
    # enables
    service_path = os.path.join(service_dir, "inbox-summarizer.service")
    with open(service_path, "w") as f:
        f.write(service_content)

    # running the program
    subprocess.run(["systemctl", "--user", "enable", "inbox-summarizer"])
    subprocess.run(["systemctl", "--user", "start", "inbox-summarizer"])

# same as linux but matching macos system
def install_macos():
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.inboxsummarizer</string>
    <key>ProgramArguments</key>
    <array>
        <string>{VENV_PYTHON}</string>
        <string>{os.path.join(REPO_DIR, "main.py")}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{REPO_DIR}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>LimitLoadToSessionType</key>
    <string>Aqua</string>
</dict>
</plist>"""
    plist_dir = os.path.expanduser("~/Library/LaunchAgents/")
    plist_path = os.path.join(plist_dir, "com.inboxsummarizer.plist")
    with open(plist_path, "w") as f:
        f.write(plist_content)

    subprocess.run(["launchctl", "load", plist_path])

# same as previous two but for windows
def install_windows():
    task_name = "InboxSummarizer"
    subprocess.run([
        "schtasks", "/create",
        "/tn", task_name,
        "/tr", f"{VENV_PYTHON} {os.path.join(REPO_DIR, 'main.py')}",
        "/sc", "onlogon",
        "/rl", "limited",
        "/f"
    ])
    subprocess.run([VENV_PYTHON, os.path.join(REPO_DIR, "main.py")])


# fields and submit button to enter details
def build_gui():
    #return if there is already a file
    if os.path.exists(os.path.join(REPO_DIR, "config.yaml")):
        messagebox.showinfo("Already configured", "config.yaml already exists. Delete it and re-run setup to reconfigure.")
        return

    root = tk.Tk()
    root.title("Inbox Summarizer Setup")
    root.resizable(False, False)

    # grid layout of fields
    tk.Label(root, text="Gmail address").grid(row=0, column=0, padx=16, pady=8, sticky="w")
    email_var = tk.StringVar()
    tk.Entry(root, textvariable=email_var, width=35).grid(row=0, column=1, padx=16)

    tk.Label(root, text="App Password").grid(row=1, column=0, padx=16, pady=8, sticky="w")
    password_var = tk.StringVar()
    tk.Entry(root, textvariable=password_var, show="*", width=35).grid(row=1, column=1, padx=16)

    tk.Label(root, text="Gemini API key").grid(row=2, column=0, padx=16, pady=8, sticky="w")
    api_key_var = tk.StringVar()
    tk.Entry(root, textvariable=api_key_var, show="*", width=35).grid(row=2, column=1, padx=16)
    
    # button to submit
    tk.Button(
        root,
        text="Set up",
        command=lambda: validate_and_submit(
            email_var.get(),
            password_var.get(),
            api_key_var.get(),
            root
        )
    ).grid(row=3, column=0, columnspan=2, pady=16)

    root.mainloop()

build_gui()