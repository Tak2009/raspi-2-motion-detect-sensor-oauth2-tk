import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText
from apiclient import errors
import json
def getSettings(_jsonPath):
   _json = json.loads(open(_jsonPath, 'r').read())
   return _json
def createMessage(sender, to, subject, message_text):
   message = MIMEText(message_text)
   message['to'] = to
   message['from'] = sender
   message['subject'] = subject
   encode_message = base64.urlsafe_b64encode(message.as_bytes())
   return {'raw': encode_message.decode()}
def sendMessage(service, user_id, message):
   try:
       message = (service.users().messages().send(userId=user_id, body=message).execute())
       print('Message Id: %s' % message['id'])
       return message
   except errors.HttpError as error:
       print('An error occurred: %s' % error)
def getAccessToken(_scopes, _token, _credentialJson):
   creds = None
   if os.path.exists(_token):
       with open(_token, 'rb') as token:
           creds = pickle.load(token)
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(_credentialJson, _scopes)
           creds = flow.run_local_server()
       with open(_token, 'wb') as token:
           pickle.dump(creds, token)
   _service = build('gmail', 'v1', credentials=creds)
   return _service
def mainProcess():
   json = getSettings("settings.json")
   service = getAccessToken(json["scopes"], json["gglToken"], json["gglJson"])
   message = createMessage(json["sender"], json["to"], json["subject"], json["message"])
   sendMessage(service, 'me', message)
# ===================================================
#if __name__ == '__main__':
#   mainProcess()
