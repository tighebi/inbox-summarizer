# Inbox Summarizer

A background process that watches your inbox, summarizes incoming emails with Gemini, and lets you archive or keep them — without ever opening your mail client.

---

## How It Works

1. A background process connects to your email via IMAP
2. When a new email arrives, it extracts the subject and body
3. The email is sent to the Gemini API for summarization
4. A desktop popup appears with the summary and two buttons:
   - **Read + Archive** — marks read and moves to archive
   - **Keep in Inbox** — leaves the email untouched

---

## Features

- IMAP IDLE support (event-driven, no constant polling)
- Runs as a background service
- Simple YAML config file

---

## Requirements

- Windows, macOS, or Linux
- Python 3.8+
- A [Gemini API key](https://aistudio.google.com/apikey)

---

## Installation

```bash
git clone https://github.com/yourusername/inbox-summarizer
cd inbox-summarizer
pip install -r requirements.txt
```

---

## Configuration

Copy the example config and fill in your details:

```bash
cp config.example.yaml config.yaml
```

```yaml
email:
  host: imap.gmail.com
  port: 993
  username: you@gmail.com
  password: your_app_password   # Gmail: use an App Password, not your real password

gemini:
  api_key: YOUR_GEMINI_API_KEY
```

Then lock down the file so only you can read it:

```bash
chmod 600 config.yaml
```

> **Gmail users:** You'll need to generate an [App Password](https://myaccount.google.com/apppasswords) — Gmail does not allow plain password authentication.

---

## Running

### Manually
```bash
python main.py
```

### As a background service (recommended)

**Linux (systemd)**

Add these two lines to your `inbox-summarizer.service` file so the service can access your display:

```ini
Environment="DISPLAY=:0"
Environment="XAUTHORITY=%h/.Xauthority"
```

Then install the service:

```bash
cp inbox-summarizer.service ~/.config/systemd/user/
systemctl --user enable inbox-summarizer
systemctl --user start inbox-summarizer
```

**macOS (launchd)**

Your `.plist` must include `LimitLoadToSessionType` set to `Aqua`, otherwise macOS will block the popup window from rendering:

```xml
<key>LimitLoadToSessionType</key>
<string>Aqua</string>
```

Then load it:

```bash
cp com.inboxsummarizer.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.inboxsummarizer.plist
```

**Windows (Task Scheduler)**

Run the included setup script:
```bash
python setup_windows_task.py
```

The task must be set to "Run only when user is logged on" — if set to run whether the user is logged on or not, Windows hides all GUI elements.

---

## Project Structure

```
inbox-summarizer/
├── main.py                        # Entry point
├── imap_client.py                 # IMAP connection, IDLE, fetch, archive
├── summarizer.py                  # Gemini API integration
├── popup.py                       # Desktop popup (tkinter)
├── config.yaml                    # Your local config (gitignored)
├── config.example.yaml            # Template for config
├── setup_windows_task.py          # Windows autostart setup
├── inbox-summarizer.service       # Linux systemd unit file
├── com.inboxsummarizer.plist      # macOS launchd plist
└── requirements.txt
```

---

## Contributing

PRs welcome. If you add support for a new LLM provider or popup backend, keep it behind the same config interface so the rest of the code doesn't need to change.

---

## License

MIT
