import imaplib
import email
from email import policy
from bs4 import BeautifulSoup
import time

def connect(host, port, username, password):
    # open SSL connection to the server
    client = imaplib.IMAP4_SSL(host, port)
    
    # log in with credentials
    client.login(username, password)
    client.select("INBOX")
    
    # return the connection object
    return client

def wait_for_new_email(client):
    line = client.readline()
    print(f"Server said: {line}")
    # tell the server to notify us when something changes (IMAP IDLE)
    client.send(b"a001 IDLE\r\n")
    # wait for a response from the server
    client.readline()
    
    while True:
        # when notified, search for unseen emails
        line = client.readline()
        # fetch the first unseen email
        if b"EXISTS" in line:
            break

    # parse it into subject + body
    client.send(b"a001 DONE\r\n")
    client.readline()
    _, unseen = client.search(None, "UNSEEN")
    uid = unseen[0].split()[-1]
    _, data = client.fetch(uid, "(RFC822)")
    raw = data[0][1]

    msg = email.message_from_bytes(raw, policy=policy.default)
    subject = msg["subject"]
    body = parse_body(msg)

    # mark it as seen
    client.store(uid, "+FLAGS", "\\Seen")
    
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
    client.copy(email["uid"], "[Gmail]/All Mail")
    client.store(email["uid"], "+FLAGS", "\\Deleted")
    client.expunge()

def worker(host, username, password, email_queue):
    # connect
    client = connect(host, 933, username, password)

    while True:
        try:
            email = wait_for_new_email(client)
            email_queue.put(email)
        
        # if ConnectionError:
        except Exception as e:
            print(f"IMAP error: {e}")
            time.sleep(5)
            # reconnect
            client = connect(host, 933, username, password)