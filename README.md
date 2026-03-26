# Inbox Summarizer

Watches your inbox and summarizes incoming emails with Gemini. A popup appears with the summary and two buttons — archive it or leave it in your inbox.

---

## Before You Start

You will need:
- Python 3.8+
- A personal Gmail account (`.edu` accounts block the required access)
- A Gemini API key — get one free at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- A Gmail App Password — generate one at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) (requires 2FA enabled)
- IMAP enabled in Gmail → Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP

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

**3. Create your config file**

Linux / macOS:
```bash
cp config.example.yaml config.yaml
```

Windows:
```bash
copy config.example.yaml config.yaml
```

Open `config.yaml` and fill in your details:
```yaml
email:
  host: imap.gmail.com
  port: 993
  username: you@gmail.com
  password: your_app_password

gemini:
  api_key: YOUR_GEMINI_API_KEY
```

**4. Lock down the config (Linux / macOS only)**
```bash
chmod 600 config.yaml
```

---

## Running Manually

Linux / macOS:
```bash
source .venv/bin/activate
python main.py
```

Windows:
```bash
.venv\Scripts\activate
python main.py
```

Send yourself an email — a popup should appear within a few seconds.

---

## Run on Startup

### Linux (systemd)

Create the service file:
```bash
mkdir -p ~/.config/systemd/user/
nano ~/.config/systemd/user/inbox-summarizer.service
```

Paste this in, replacing `YOUR_USERNAME` with your actual username:
```ini
[Unit]
Description=Inbox Summarizer

[Service]
ExecStart=/home/YOUR_USERNAME/Documents/coding/inbox-summarizer/.venv/bin/python /home/YOUR_USERNAME/Documents/coding/inbox-summarizer/main.py
WorkingDirectory=/home/YOUR_USERNAME/Documents/coding/inbox-summarizer
Environment="DISPLAY=:0"
Environment="XAUTHORITY=%h/.Xauthority"
Restart=on-failure

[Install]
WantedBy=default.target
```

Enable it:
```bash
systemctl --user enable inbox-summarizer
systemctl --user start inbox-summarizer
```

Check it's running:
```bash
systemctl --user status inbox-summarizer
```

### macOS (launchd)

Your `.plist` must include `LimitLoadToSessionType` set to `Aqua`, otherwise macOS blocks the popup from rendering:
```xml
<key>LimitLoadToSessionType</key>
<string>Aqua</string>
```

Then load it:
```bash
cp com.inboxsummarizer.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.inboxsummarizer.plist
```

### Windows (Task Scheduler)

Run the included setup script:
```bash
python setup_windows_task.py
```

When setting up the task, make sure it is set to "Run only when user is logged on" — otherwise Windows will hide the popup.

---

## Project Structure

```
inbox-summarizer/
├── main.py                    # Entry point
├── imap_client.py             # IMAP connection, IDLE, fetch, archive
├── summarizer.py              # Gemini API integration
├── popup.py                   # Desktop popup (tkinter)
├── config.yaml                # Your local config (gitignored)
├── config.example.yaml        # Template for config
├── setup_windows_task.py      # Windows autostart setup
├── inbox-summarizer.service   # Linux systemd unit file
├── com.inboxsummarizer.plist  # macOS launchd plist
└── requirements.txt
```

---

## License

MIT
