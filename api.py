from __future__ import print_function

import os
import base64
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import fitz  # PyMuPDF library

# Define the SCOPES for Gmail and Google Sheets APIs
# If modifying these scopes, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/spreadsheets']

def main():
    creds = get_credentials()
    list_gmail_messages(creds, 'percyblack.jnj@gmail.com')
    

def get_credentials():
    creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token1.json'):
        creds = Credentials.from_authorized_user_file('token1.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials1.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token1.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def list_gmail_messages(creds, query):
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me',q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return
        
        for message in messages:
            get_gmail_message(creds, message['id'])

    except HttpError as error:
        # Handle errors from gmail API.
        print(f'An error occurred: {error}')

def get_gmail_message(creds, message_id):
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        message = service.users().messages().get(userId='me',id=message_id).execute()

        if not message:
            print('No message found.')
            return
        
        parts = message['payload']['parts']
        for part in parts:
            mime_type = part['mimeType']
            file_name = part['filename']
            body = part['body']
            
            if mime_type == 'application/pdf' and not file_name == '' and 'attachmentId' in body:
                attachment_id = body['attachmentId']
                get_gmail_attachment(creds, message_id, attachment_id, file_name)
            
    except HttpError as error:
        # Handle errors from gmail API.
        print()
        print(f'An error occurred: {error}')

def get_gmail_attachment(creds, message_id, attachment_id, file_name):
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        attachment = service.users().messages().attachments().get(userId='me',messageId=message_id,id=attachment_id).execute()
        
        data = attachment['data']
        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        
        path = os.path.join(message_id, file_name)
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as file:
            file.write(file_data)
            print(f'File saved at {path}')

    except HttpError as error:
        # Handle errors from gmail API.
        print()
        print(f'An error occurred: {error}')


# Specify the directory where the downloaded PDFs are stored
downloaded_pdfs_directory = 'C:\\Users\\njiru\\VS Projects\\189a143cb3804de3'

# Get a list of all files in the directory
pdf_files = [f for f in os.listdir(downloaded_pdfs_directory) if f.lower().endswith('.pdf')]

if pdf_files:
    # Get the first PDF file from the list
    first_pdf_file = pdf_files[0]

    # Construct the full path to the PDF file
    pdf_path = os.path.join(downloaded_pdfs_directory, first_pdf_file)

    # Call PHP script to extract relevant information
    url = 'https://readpdf.plinytest.com/view/readFileF.php'
    files = {'pdf_file': open(pdf_path, 'rb')}
    response = requests.post(url, files=files, data={'readpdf': 'true'})

    # Process response from PHP script
    if response.status_code == 200:
        print('Relevant information extracted:', response.text)
    else:
        print('Error extracting information:', response.status_code)
else:
    print('No PDF files found in the directory.')


if __name__ == '__main__':
    main()

