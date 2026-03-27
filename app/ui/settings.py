import tkinter as tk
from tkinter import messagebox
import yaml
import os
from imapclient import IMAPClient

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

def load_current_config():
    # open config.yaml
    config_path = os.path.join(REPO_DIR, "config.yaml")
    with open(config_path) as f:
    # return the config dictionary
        return yaml.safe_load(f)
    
# Tries connecting with the new credentials before saving
def validate_credentials(email, password):
    client = IMAPClient("imap.gmail.com", ssl=True)
    client.login(email, password)
    client.logout()

# Validates, connects, writes config, shows confirmation
def save_config(email, password, api_key, window):
    # validate nothing is blank
    if not email or not password or not api_key:
        messagebox.showerror("Error", "All fields are required.")
        return
    
    # try connecting to IMAP with new credentials
    try:
        validate_credentials(email, password)
        # catch specific errors same as setup.py
    except Exception as e:
        error = str(e).lower()
        if "application-specific password required" in error:
            messagebox.showerror("Error", "Gmail requires an App Password, not your real password.\nGenerate one at myaccount.google.com/apppasswords")
        elif "invalid credentials" in error:
            messagebox.showerror("Error", "Could not connect. Double check your email and App Password.")
        elif "web login required" in error or "managed" in error:
            messagebox.showerror("Error", "This looks like a managed Google account.\nPlease use a personal Gmail account.")
        else:
            messagebox.showerror("Error", f"Connection failed: {e}")
        return
    
    # if successful write the new values to config.yaml
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

    # show success message
    messagebox.showinfo("Saved", "Settings saved. Restart the app for changes to take effect.")
    window.destroy()

def build_gui(root):
    # open config.yaml and pre-fill the fields with current values
    config = load_current_config()

    window = tk.Toplevel(root)
    window.title("Settings")
    window.resizable(False, False)

    # show a window with three fields:
        # gmail address (pre-filled)
    tk.Label(window, text="Gmail address").grid(row=0, column=0, padx=16, pady=8, sticky="w")
    email_var = tk.StringVar(value=config["email"]["username"])
    tk.Entry(window, textvariable=email_var, width=35).grid(row=0, column=1, padx=16)

        # app password (pre-filled, masked)
    tk.Label(window, text="App Password").grid(row=1, column=0, padx=16, pady=8, sticky="w")
    password_var = tk.StringVar(value=config["email"]["password"])
    tk.Entry(window, textvariable=password_var, show="*", width=35).grid(row=1, column=1, padx=16)

        # gemini api key (pre-filled, masked)
    tk.Label(window, text="Gemini API key").grid(row=2, column=0, padx=16, pady=8, sticky="w")
    api_key_var = tk.StringVar(value=config["gemini"]["api_key"])
    tk.Entry(window, textvariable=api_key_var, show="*", width=35).grid(row=2, column=1, padx=16)

    btn_frame = tk.Frame(window)
    btn_frame.grid(row=3, column=0, columnspan=2, pady=16)

    # save button calls save_config()
    tk.Button(
        btn_frame,
        text="Save",
        command=lambda: save_config(
            email_var.get(),
            password_var.get(),
            api_key_var.get(),
            window
        )
    ).pack(side="left", padx=8)

    # cancel button closes the window
    tk.Button(
        btn_frame,
        text="Cancel",
        command=window.destroy
    ).pack(side="left", padx=8)

    window.mainloop()

def open():
    build_gui()