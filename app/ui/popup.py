import tkinter as tk
from tkinter import messagebox
from app.core import summarizer, imap_client

# time until window dissapears
TIMEOUT = 15

# has a window open but be minimized
def init_tkinter():
    root = tk.Tk()
    root.withdraw()
    return root

# 
def show(summary):
    # defaults to keep email
    result = tk.StringVar(value="keep") 
    
    # child window
    window = tk.Toplevel()
    window.title("New Email")
    window.resizable(False, False)
    
    # displays the summary text
    tk.Label(window, text=summary, wraplength=400, justify="left", padx=16, pady=16).pack()
    
    # add countdown label showing "Keeping in 15s"
    countdown_label = tk.Label(window, text=f"Keeping in {TIMEOUT}s...")
    countdown_label.pack(pady=(0, 8))
    
    # actions
    def on_archive():
        result.set("archive")
        window.destroy()

    def on_keep():
        result.set("keep")
        window.destroy()

    # shows buttons
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=(0, 16))
    tk.Button(btn_frame, text="Read + Archive", command=on_archive).pack(side="left", padx=8)
    tk.Button(btn_frame, text="Keep in Inbox", command=on_keep).pack(side="left", padx=8)

    # every second:
    remaining = TIMEOUT
    def tick():
        nonlocal remaining
        # Critical Fix: Stop the timer if the user already clicked a button
        if not window.winfo_exists():
            return
            
        remaining -= 1
        countdown_label.config(text=f"Keeping in {remaining}s...")
        
        if remaining <= 0:
            on_archive("keep")
        else:
            window.after(1000, tick)

    # wait for button click or timeout then return
    window.wait_window()
    return result.get()

# built in error box
def show_error(message):
    messagebox.showerror("Inbox Summarizer", message)


def check_queue(email_queue, config, root):
    # if queue has an email:
    if not email_queue.empty():
        email = email_queue.get()
        # summarize it
        try:
            summary = summarizer.summarize(email, config["gemini"]["api_key"])
            
            # show the popup with countdown
            action = show(summary)
            
            # if action == "archive": archive it
            if action == "archive":
                imap_client.archive(email)
        # if there is some failure
        except Exception as e:
            print(f"Error processing email: {e}")
            show_error("Failed to process email.")
    # schedule itself to run again in 1 second
    root.after(1000, lambda: check_queue(email_queue, config, root))