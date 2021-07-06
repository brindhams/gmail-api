from __future__ import print_function
import os.path
import base64,email
import json
import sqlalchemy as db
from sqlalchemy import Table, Column, Integer, String, VARCHAR , MetaData
from requests import Session
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

engine = db.create_engine('sqlite:///gmail.db', echo=True)
meta = db.MetaData()
mail = Table(
    'mail', meta,
    Column('id', Integer, primary_key=True),
    Column('mail_to',String),
    Column('mail_from', VARCHAR),
    Column('mail_subject', String),
    Column('mail_date', String)
)
session = Session()
meta.create_all(engine)



def get_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service
   


def get_email_list():
    service=get_gmail_service()
    results=service.users().messages().list(userId='me',maxResults=5).execute()
    # print(results)
    return results.get('messages',[])

def get_email_content(message_id):
    service = get_gmail_service()
    results = service.users().messages().get(userId='me', id=message_id, format='raw').execute()
    msg_str = base64.urlsafe_b64decode(results['raw'].encode('ASCII'))
    mine_msg = email.message_from_bytes(msg_str)
    data = {'to': mine_msg['To'], 'from': mine_msg['From'], 'date': mine_msg['Date'], 'subject': mine_msg['Subject']}
    # print (data)
    return data

def store():
    engine = db.create_engine('sqlite:///gmail.db', echo=True)
    conn = engine.connect()
    result= get_email_content('17a6a71e8a30e051')
    conn.execute('INSERT INTO mail(mail_from,mail_to,mail_subject,mail_date) VALUES (:mail_from,:mail_to,:mail_subject,:mail_date)',
                 result['from'], result['to'], result['subject'], result['date'])
    print('logged successfully')
    conn.close()

def mark_as_unread():
    engine = db.create_engine('sqlite:///gmail.db', echo=True)
    conn = engine.connect()
    rules = json.load(open('rules.json'))
    for rule in rules["rule1"]["fields"]:
        print(rule['name'],rule['value'])
        service=get_gmail_service()
        service.users().messages().modify(userId='me',id='17a6a71e8a30e051' , body={
        'removeLabelIds': ['UNREAD']
    }
    )


def mark_as_read():
    engine = db.create_engine('sqlite:///gmail.db', echo=True)
    conn = engine.connect()
    rules = json.load(open('rules.json'))
    for rule in rules["rule1"]["fields"]:
        print(rule['name'],rule['value'])
        service=get_gmail_service()
        service.users().messages().modify(userId='me',id ='17a6a71e8a30e051',body={
        'removeLabelIds': ['UNREAD']
    }
    )

def archive_message():
    engine = db.create_engine('sqlite:///gmail.db', echo=True)
    conn = engine.connect()
    rules = json.load(open('rules.json'))
    for rule in rules["rule1"]["fields"]:
        print(rule['name'],rule['value'])
        service=get_gmail_service()
        service.users().messages().modify(userId='me',id ='17a6a71e8a30e051',body={
        'removeLabelIds': ['INBOX']
    }
    )








if __name__ == '__main__':
    # get_email_list()
    # get_email_content('17a6a71e8a30e051') 
    # store()
    mark_as_unread()
    # mark_as_read()
    # archive_message()
    
