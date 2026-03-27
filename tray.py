import pystray
from PIL import Image, ImageDraw
import threading

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
    # open the settings window (settings.py)
    import settings
    # run it in a way that doesn't block the tray
    threading.Thread(target=settings.open, daemon=True).start()

def get_menu(root):
    # return a pystray.Menu with two items:
    return pystray.Menu(
        # "Settings" -> calls open_settings
        pystray.MenuItem("Settings", open_settings),
        # "Quit" -> calls quit_app
        pystray.MenuItem("Quit", lambda icon, item: quit_app(icon, item, root))
    )

def run_tray(root):
    # create the icon image
    image = create_icon_image()
    # create the pystray.Icon with the image and menu
    icon = pystray.Icon(
        "inbox-summarizer",
        image,
        "Inbox Summarizer",
        menu=get_menu(root)
    )
    # run the icon in a background thread so it doesn't block tkinter
    threading.Thread(target=icon.run, daemon=True).start()