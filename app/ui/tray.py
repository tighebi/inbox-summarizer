import pystray
from PIL import Image, ImageDraw
import threading
from app.ui import settings


def create_icon_image():
    # load or generate a small image for the tray icon
    img = Image.new("RGB", (64,64), color=(99,102,241))
    draw = ImageDraw.Draw(img)
    draw.ellipse((16,16,48,48), fill = (255,255,255))

    # return the image object
    return img

def quit_app(icon, item, root):
    # stop the tray icon
    icon.stop()
    # destroy the tkinter root window
    root.after(0,root.destroy)

def open_settings(icon, item, root):
    # run it in a way that doesn't block the tray
    threading.Thread(target=settings.open, daemon=True).start()

def run_tray(root):
    icon = pystray.Icon(
        "inbox-summarizer",
        create_icon_image(),
        "Inbox Summarizer",
        menu=pystray.Menu(
            # Notice the 'icon, item' added here to prevent TypeErrors
            pystray.MenuItem("Settings", lambda icon, item: root.after(0, settings.open_settings(icon,item,root), root)),
            pystray.MenuItem("Quit", lambda icon, item: quit_app(icon, item, root))
        )
    )
    threading.Thread(target=icon.run, daemon=True).start()