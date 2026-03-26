from imapclient import IMAPClient
import email
from email import policy
from bs4 import BeautifulSoup
import time

def connect(host, username, password):
    # open SSL connection to the server
    client = IMAPClient(host, ssl=True)

    # log in with credentials
    client.login(username, password)
    client.select_folder("INBOX")    
    # return the connection object
    return client

def wait_for_new_email(client):
    client.idle()
    print("Waiting for email...")

    while True:
        responses = client.idle_check(timeout=30)
        print(f"Server sent: {responses}")
        if responses:
            break

    client.idle_done()
    
    messages = client.search("UNSEEN")
    if not messages:
        return None

    # parse it into subject + body
    uid = messages[-1]
    raw_data = client.fetch([uid], ["RFC822"])
    raw = raw_data[uid][b"RFC822"]

    msg = email.message_from_bytes(raw, policy=policy.default)
    subject = msg["subject"]
    body = parse_body(msg)

    # mark it as seen
    client.set_flags([uid], [b"\\Seen"])
    # return {"uid": ..., "subject": ..., "body": ...}
    return {"uid": uid, "subject": subject, "body": body, "client": client}

def parse_body(msg):
    if msg.is_multipart():
        # walk through the MIME parts
        for part in msg.walk():
            # ignore attachments and ind the text/plain part
            if part.get_content_type() == "text/plain":
                return part.get_content()
            if part.get_content_type() == "text/html":
                soup = BeautifulSoup(part.get_content(), "html.parser")
                return soup.get_text()
    # if no plain text, fall back to text/html and strip tags
    else:
        return msg.get_content()

def archive(email):
    # move the email to the archive folder
    client = email["client"]
    client.copy([email["uid"]], "[Gmail]/All Mail")
    client.delete_messages([email["uid"]])
    client.expunge()

def worker(host, username, password, email_queue):
    # connect
    client = connect(host, username, password)

    while True:
        try:
            email = wait_for_new_email(client)
            if email:
                email_queue.put(email)
        
        # if ConnectionError:
        except Exception as e:
            print(f"IMAP error: {e}")
            time.sleep(5)
            client = connect(host, username, password)