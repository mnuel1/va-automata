from flask import Flask, redirect, request, session, jsonify, url_for
import requests
import json
from requests.auth import HTTPBasicAuth
import os.path
import time
from nltk import Tree
from datetime import datetime
import nltk
import urllib.parse
import webbrowser
import random
import os
import asyncio
import subprocess
import base64
import pickle
from email.mime.text import MIMEText


from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2

app = Flask(__name__)
# CORS(app, origins='http://localhost:5173')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/meetings.space.created','https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
app.secret_key = 'this is a secret'

client_id = 'boKvRRPiSiaMXXx4EBEALg'
client_secret = 'nF9CJ8G23lk2VTpNE0yous1ZMVLtu5rs'
redirect_uri = 'http://localhost:4000/redirect'


i_dont_understand_wtf_u_saying = [
    "I'm sorry, but I couldn't understand your request: '{prompt}'.",
    "I apologize, I didn't catch that: '{prompt}'.",
    "Hmm, I'm not sure what you mean by: '{prompt}'.",
    "I couldn't quite grasp what you were asking: '{prompt}'.",
    "Sorry, but I'm not sure I understand: '{prompt}'.",
    "I'm having trouble understanding your request: '{prompt}'.",
    "It seems I didn't understand your task: '{prompt}'.",
    "I didn't get that: '{prompt}'.",
    "I'm afraid I don't understand: '{prompt}'.",
    "Apologies, but I couldn't comprehend your request: '{prompt}'."
]

def generate_response(prompt):
    # Randomly select a template
    response_template = random.choice(i_dont_understand_wtf_u_saying)
    # Format the template with the provided prompt
    response = response_template.format(prompt=prompt)
    return response

def getAccessToken(authorization_code):
    token_url = 'https://zoom.us/oauth/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri
    }

    response = requests.post(token_url, headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get access token. Status code: {response.status_code}")
        print("Response:", response.json())
        return None

def refreshAccessToken(refresh_token):
    token_url = 'https://zoom.us/oauth/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(token_url, headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to refresh access token. Status code: {response.status_code}")
        print("Response:", response.json())
        return None

def isQuestion(tokens):  # Added self parameter
    return any(token.lower() in ["what", "when", "why", "where", "how",] for token in tokens)

def extract_verbs_and_programs_and_email_nouns(tree):
    verb = None
    program = None
    email_nouns = None
    
    if isinstance(tree, nltk.Tree):
        if tree.label() == "VERB":
            verb = tree[0]
        elif tree.label() == "PROGRAM":
            program = tree[0]
        elif tree.label() == "EMAIL_NOUNS":
            email_nouns = tree[0]
        else:
            for subtree in tree:
                sub_verb, sub_program, sub_email_nouns = extract_verbs_and_programs_and_email_nouns(subtree)
                if sub_verb:
                    verb = sub_verb
                if sub_program:
                    program = sub_program
                if sub_email_nouns:
                    email_nouns = sub_email_nouns
    
    return verb, program, email_nouns


def read_apps_file(file_path):
    programs = {}
    with open(file_path, 'r') as file:
        for line in file:
            name = line.strip().split(' || ')[0]
            path = line.strip().split(' || ')[1]
            programs[name.lower()] = path            
    return programs

def search_program(programs, keyword):    
    matches = [name for name in programs.keys() if keyword.lower() in name]
    return matches

async def run_program(program_path):
     # Run the program asynchronously
     subprocess.Popen(program_path, shell=True)

def authenticate_gmail():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def send_email(service, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {'raw': raw_message}
    try:
        message = service.users().messages().send(userId="me", body=message).execute()
        return message
    except Exception as error:
        return None

def list_messages(service, query='', max_results=7):
    try:
        response = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        messages_info = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            headers = msg['payload']['headers']
            sender = next(header['value'] for header in headers if header['name'] == 'From')
            date = next(header['value'] for header in headers if header['name'] == 'Date')
            messages_info.append({
                'sender': sender,
                'date': date,
                'snippet': msg['snippet']
            })
        return messages_info
    except Exception as error:
        print(f'An error occurred: {error}')
        return None


    
@app.route('/send_email', methods=['POST'])
def api_send_email():
    data = request.get_json()
    to = data.get('to')
    subject = data.get('subject')
    message_text = data.get('message_text')
    
    if not to or not subject or not message_text:
        return jsonify({"error": "Missing 'to', 'subject', or 'message_text'"}), 400
    
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    
    result = send_email(service, to, subject, message_text)
    
    if result:
        return jsonify({"status": "Email sent", "message_id": result['id']}), 200
    else:
        return jsonify({"error": "Failed to send email"}), 500

@app.route('/list_emails', methods=['GET'])
def api_list_emails():
    query_parts = []

    if request.args.get('unread', 'false').lower() == 'true':
        query_parts.append('is:unread')
    if request.args.get('starred', 'false').lower() == 'true':
        query_parts.append('is:starred')
    if request.args.get('important', 'false').lower() == 'true':
        query_parts.append('is:important')
    if request.args.get('snooze', 'false').lower() == 'true':
        query_parts.append('label:snoozed')
    if request.args.get('sent', 'false').lower() == 'true':
        query_parts.append('in:sent')
    if request.args.get('drafts', 'false').lower() == 'true':
        query_parts.append('in:drafts')
    if request.args.get('spam', 'false').lower() == 'true':
        query_parts.append('in:spam')
    if request.args.get('bin', 'false').lower() == 'true':
        query_parts.append('in:trash')

    query = ' '.join(query_parts)
    
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    
    messages = list_messages(service, query)
    
    if messages is not None:
        return jsonify({"messages": messages}), 200
    else:
        return jsonify({"error": "Failed to retrieve emails"}), 500

@app.route('/')
def redirect_to_zoom():    
    return "Hello, World"

@app.route('/authorize')
def authorizeZoom():
    zoom_oauth_url = f"https://zoom.us/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}"
    return redirect(zoom_oauth_url)

@app.route('/redirect')
def zoomRedirect():
    authorization_code = request.args.get('code')
    if not authorization_code:
        return "Error: No authorization code provided."

    tokens = getAccessToken(authorization_code)
    if tokens:
        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens['refresh_token']
        session['token_expires_at'] = time.time() + tokens['expires_in']  # Store the expiration time
        return redirect(url_for('create_meeting'))
    else:
        return "Error: Failed to obtain access token."

@app.route('/get/windows/apps')
def get_installed_apps():
    apps = []
    file_path = 'apps.txt'
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if 'Number of installed apps' in line:
                    continue  # Skip the summary line
                parts = line.strip().split(' || ')
                if len(parts) >= 2:
                    app_info = {'name': parts[0], 'install_location': parts[1]}
                    if len(parts) == 3:
                        app_info['executable_file'] = parts[2]
                    apps.append(app_info)            
    except FileNotFoundError:
        return jsonify({"error": "apps.txt file not found"}), 404

    # Extract individual words from application names
    app_words = []
    for app in apps:
        words = app["name"].split()
        app_words.extend([f'"{word}"' for word in words])

    # Remove duplicates
    app_words = list(set(app_words))

    # Update cfg_rules.txt
    cfg_rules_path = 'cfg_rules.txt'
    try:
        with open(cfg_rules_path, 'r') as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            if line.startswith('PROGRAM ->'):
                program_rule = 'PROGRAM -> ' + ' | '.join(app_words) + '\n'
                new_lines.append(program_rule)
            elif line.startswith('ADJECTIVE ->'):
                adjective_rule = 'ADJECTIVE -> ' + ' | '.join(app_words) + '\n'
                new_lines.append(adjective_rule)
            else:
                new_lines.append(line)

        with open(cfg_rules_path, 'w') as file:
            file.writelines(new_lines)
    except FileNotFoundError:
        return jsonify({"error": "cfg_rules.txt file not found"}), 404

    return jsonify({'installedApps': apps}),200

@app.route('/create/meeting/gmeet')
def createGoogleMeeting():
    """Shows basic usage of the Google Meet API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        client = meet_v2.SpacesServiceClient(credentials=creds)
        request = meet_v2.CreateSpaceRequest()
        response = client.create_space(request=request)
        print(f'Space created: {response.meeting_uri}')
    except Exception as error:        
        return jsonify({'error': error}),500

@app.route('/create/meeting/zoom')
def createZoomMeeting():
    # Check if the access token is available and still valid
    if 'access_token' not in session or time.time() >= session.get('token_expires_at', 0):
        if 'refresh_token' in session:
            tokens = refreshAccessToken(session['refresh_token'])
            if tokens:
                session['access_token'] = tokens['access_token']
                session['refresh_token'] = tokens['refresh_token']
                session['token_expires_at'] = time.time() + tokens['expires_in']
            else:
                return redirect(url_for('authorize_zoom'))
        else:
            return redirect(url_for('authorize_zoom'))

    access_token = session['access_token']

    start_time = request.args.get('start_time')
    if not start_time:
        start_time = datetime.now(datetime.timezone.utc).isoformat()

    # Zoom API endpoint for creating a meeting
    url = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "topic": "Meeting",
        "type": 2,  # Scheduled meeting
        "start_time": start_time,  # UTC time in ISO 8601 format
        "duration": 120,  # duration in minutes
        "timezone": "UTC",
        "agenda": "Normal Meeting",
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": False,
            "mute_upon_entry": True,
            "watermark": False,
            "use_pmi": False,
            "approval_type": 1,  # Automatically approve
            "registration_type": 1,
            "audio": "voip",
            "auto_recording": "none"
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        print("Meeting created successfully!")
        print("Meeting details:", response.json())
        return jsonify(response.json())
    else:
        print(f"Failed to create meeting. Status code: {response.status_code}")
        print("Response:", response.json())
        return "Error: Failed to create meeting."

@app.route('/chats')
def getChatSessions():
    json_objects = []
    try:
        for filename in os.listdir('msgs'):
            if filename.endswith(".json"):
                filepath = os.path.join('msgs', filename)
                with open(filepath, "r") as file:
                    data = json.load(file)
                    json_objects.append(data)
        return jsonify({'chats': json_objects}),200
    except Exception as error:        
        return jsonify({'error': error}),500


@app.route('/prompt', methods=["POST"])
async def main():
    data = request.get_json()

    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided in the request body"}), 400

    prompt = data['prompt']
    sessionID = data['sessionID']
    max_results = 7
    try:
        with open('cfg_rules.txt', 'r') as file:
            cfg_rules = file.read()
    except FileNotFoundError:
        return jsonify({"error": "CFG rules file not found"}), 500

    grammar = nltk.CFG.fromstring(cfg_rules)
    parser = nltk.ChartParser(grammar)

    tokens = nltk.word_tokenize(prompt.lower())
    if not isQuestion(tokens):
        try:
            trees = list(parser.parse(tokens))
            if not trees:
                response = generate_response(prompt)
            else:
                cfg_values = "\n".join([str(tree) for tree in trees])
                tree = Tree.fromstring(cfg_values)
                verb, program, email_nouns= extract_verbs_and_programs_and_email_nouns(tree)
                if verb == 'open':
                    programs_file_path = 'apps.txt'
                    all_programs = read_apps_file(programs_file_path)
                    matches = search_program(all_programs, program)
                    if len(matches) == 1:
                        program_path = all_programs[matches[0]]
                        asyncio.create_task(run_program(program_path))
                        response = f"Opening {matches[0]}..."
                    elif len(matches) == 0:
                        response = "Sorry, I couldn't find the {program} on this computer."
                    else:
                        response = f"Multiple matches found: {', '.join(matches)}"
                    pass
                elif verb == 'search':
                    response = f"Let me look that up for you..."
                    link = f"https://www.google.com/search?q={urllib.parse.quote(prompt.lower())}"
                    webbrowser.open(link)
                    pass
                elif verb == 'schedule':
                    # Perform task for 'schedule' verb
                    pass
                elif verb == 'create':
                    # Perform task for 'create' verb
                    pass
                elif verb == 'send' and email_nouns == 'email':
                    # Handle 'send email' action
                    recipients = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == 'GMAIL_FORMAT')]
                    subject = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == 'SUBJECT')]
                    body = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == 'BODY')]

                    if recipients and subject and body:
                        to = ''.join(recipients[0])
                        subject_text = ' '.join(subject[0])
                        message_text = ' '.join(body[0])
                        print(f"{to} {subject_text} {message_text}")

                        creds = authenticate_gmail()
                        service = build('gmail', 'v1', credentials=creds)

                        result = send_email(service, to, subject_text, message_text)

                        if result:
                            response = f"Email sent successfully to {to}"
                        else:
                            response = "Failed to send email"
                    else:
                        response = "Invalid email structure. Please provide recipients, subject, and body."

                elif verb == 'read' and email_nouns == 'emails':
                    # Handle 'read emails' action
                    filters = [subtree.leaves() for subtree in tree.subtrees(filter=lambda t: t.label() == 'FILTER')]
                    filter_queries = []
                    for filter_list in filters:
                        for filter_item in filter_list:
                            if filter_item == 'unread':
                                filter_queries.append('is:unread')
                            elif filter_item == 'starred':
                                filter_queries.append('is:starred')
                            elif filter_item == 'important':
                                filter_queries.append('is:important')
                            elif filter_item == 'snoozed':
                                filter_queries.append('label:snoozed')
                            elif filter_item == 'sent':
                                filter_queries.append('in:sent')
                            elif filter_item == 'drafts':
                                filter_queries.append('in:drafts')
                            elif filter_item == 'spam':
                                filter_queries.append('in:spam')
                            elif filter_item == 'bin':
                                filter_queries.append('in:trash')

                    query = ' '.join(filter_queries)

                    creds = authenticate_gmail()
                    service = build('gmail', 'v1', credentials=creds)

                    messages = list_messages(service, query, max_results)

                    if messages:
                        response = "Here are the filtered emails:\n\n"
                        for message in messages:
                            response += (
                                f"From: {message['sender']}\n"
                                f"Date: {message['date']}\n"
                                f"Snippet: {message['snippet']}\n\n"
                                f"-------------------------------------------------------------\n\n"
                            )
                    else:
                        response = "No emails found with the specified filters."
                
                else:
                    # Handle unknown verbs
                    response = generate_response(prompt)
        except ValueError as e:
            print(e)
            response = generate_response(prompt)
    else:
        response = f"Unfortunately, I do not understand your request, but the web says https://www.google.com/search?q={urllib.parse.quote(prompt.lower())}"
        link = f"https://www.google.com/search?q={urllib.parse.quote(prompt.lower())}"
        webbrowser.open(link)

    # Save the prompt and response in a session-specific file
    session_file_path = os.path.join('msgs', f'{sessionID}.json')
    entry = {"message": prompt, "response": response}

    if not os.path.exists('msgs'):
        os.makedirs('msgs')

    if os.path.exists(session_file_path):
        with open(session_file_path, 'r') as file:
            session_data = json.load(file)
    else:
        session_data = []

    session_data.append(entry)

    with open(session_file_path, 'w') as file:
        json.dump(session_data, file, indent=4)

    return jsonify({"response": response}), 200      
        


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)
