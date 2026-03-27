# Inbox Summarizer

Watches your inbox and summarizes incoming emails with Gemini. A popup appears with the summary and two buttons — archive it or leave it in your inbox.

---

## Before You Start

You will need:
- Python 3.8+
- A personal Gmail account (`.edu` accounts block the required access)
- A Gemini API key — get one free at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- A Gmail App Password — generate one at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) (requires 2FA enabled)
- IMAP enabled in Gmail → Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP (should be by default)

---

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/tighebi/inbox-summarizer
cd inbox-summarizer
```

**2. Create a virtual environment**

Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**3. Configuration**
```bash
python setup.py
```

---

## Project Structure

```
inbox-summarizer/
├── app/
│   ├── core/                  # Background Logic & AI
│   │   ├── imap_client.py     # Thread-safe IMAP connection & archiving
│   │   └── summarizer.py      # Gemini API integration & rate-limit handling
│   └── ui/                    # User Interface
│       ├── popup.py           # Tkinter auto-closing desktop notifications
│       ├── settings.py        # Configuration management GUI
│       └── tray.py            # System tray icon and background lifecycle
├── main.py                    # Application Entry Point
├── setup.py                   # Initial Setup/Installation Wizard
├── config.example.yaml        # Template for user configuration
└── requirements.txt           # Python dependencies
```

---

### Running in the Background

Linux (systemd)
Check it's running via:

```bash
systemctl --user status inbox-summarizer
```

macOS (launchd)

Your .plist must include LimitLoadToSessionType set to Aqua, otherwise macOS blocks the popup from rendering.

```bash
cp com.inboxsummarizer.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.inboxsummarizer.plist
```


---

**Make those two quick parameter fixes to `popup.py` and `tray.py`, and you should be fully ready to run `python main.py` and test it.

---

## License

MIT
