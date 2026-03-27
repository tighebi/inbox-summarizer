import threading
import queue
import yaml
import os
import sys

# Reach into the folders
from app.core import imap_client
from app.ui import popup, tray

# Ensure config.yaml is found in the root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("Error: config.yaml not found. Run setup.py first.")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

config = load_config()

# Setup logic 
email_queue = queue.Queue()

threading.Thread(
    target=imap_client.worker,
    args=(
        config["email"]["host"], 
        config["email"]["username"], 
        config["email"]["password"], 
        email_queue
    ),
    daemon=True
).start()

root = popup.init_tkinter()
# Pass the GEMINI_KEY and the email login info
root.after(1000, lambda: popup.check_queue(email_queue, config, root))

tray.run_tray(root)
root.mainloop()