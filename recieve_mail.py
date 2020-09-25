import imaplib,email
import urllib.request
import urllib.parse
import json

results = []
ip_address = []

username = 'pytester.py@gmail.com' #server email address
password = 'pypypy12' #server email password
imap_url = 'imap.gmail.com'

def auth(username,password,imap_url):
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(username,password)
    return con

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)

def search(key,value,con):
    result, data  = con.search(None,key,'"{}"'.format(value))
    return data

def get_emails(result_bytes):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)
    return (msgs)

def receivemail():
    global con
    print("Recieving Mail...")
    results = []
    ip_address = []

    username = 'pytester.py@gmail.com' #server email address
    password = 'pypypy12' #server email password
    imap_url = 'imap.gmail.com'
    con = auth(username,password,imap_url)
    con.select('INBOX')

    result, data = con.fetch(b'1','(RFC822)')
    raw = email.message_from_bytes(data[0][1])
    msgs = get_emails(search('FROM','aakashguru6898@gmail.com',con)) #authority email address
    #print("date : " + raw['Date'])
    #print(raw)
        
    for i in msgs:
        results.append(get_body(email.message_from_bytes(i[0][1])).decode('utf-8'))
        
    #print(results)
    if results != []:
        bata = search('FROM','aakashguru6898@gmail.com',con)
        bata = bata[0].decode("utf-8").split()
        #print(bata)
        for num in bata:
            #print(num)
            con.store(num, '+FLAGS', '\\Deleted')
    #con.store(msgs, '+FLAGS', '\\Deleted')
        
    con.expunge()
    con.close()
    con.logout()
    
    if results == []:
        return None

    return results[-1][0]

    """for i in range(0,4):
        print(result[-1][i])"""
#receivemail()
