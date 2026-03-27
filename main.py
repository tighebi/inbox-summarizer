import threading, queue, yaml, sys, os
from app.core import imap_client
from app.ui import popup, tray


if not os.path.exists("config.yaml"):
    print("No config.yaml found. Please run setup.py first.")
    sys.exit(1)

with open("config.yaml") as f:
    config = yaml.safe_load(f)

# user details
EMAIL_HOST = config["email"]["host"]
EMAIL_USER = config["email"]["username"]
EMAIL_PASS = config["email"]["password"]
GEMINI_KEY = config["gemini"]["api_key"]

# connects user to inbox
email_queue = queue.Queue()

# runs the threading
threading.Thread(
    target=imap_client.worker,
    args=(EMAIL_HOST, EMAIL_USER, EMAIL_PASS, email_queue),
    daemon=True
).start()

# holds the reference to the tkinter popup window
root = popup.init_tkinter()

# tkinter method that ties the queue from main and the popup logic
root.after(1000, lambda: popup.check_queue(email_queue, GEMINI_KEY, root))

#display in the tray
tray.run_tray(root)

# tkinter wakes up every second to run check_queue, and sleeps the rest of the time
root.mainloop()
