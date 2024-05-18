from flask import Flask, redirect, request, session, jsonify, url_for
import requests
import json
from requests.auth import HTTPBasicAuth
import os.path
import time
from datetime import datetime
import nltk
import urllib.parse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2

app = Flask(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']
app.secret_key = 'this is a secret'

client_id = 'boKvRRPiSiaMXXx4EBEALg'
client_secret = 'nF9CJ8G23lk2VTpNE0yous1ZMVLtu5rs'
redirect_uri = 'http://localhost:4000/redirect'


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
    return any(token.lower() in ["what", "when", "why", "where", "how"] for token in tokens)


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
def main():    
    data = request.get_json()

    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided in the request body"}), 400

    prompt = data['prompt']
    sessionID = data['sessionID']

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
                response = f"I am sorry, I don't understand your task: {prompt}"
            else:
                response = "\n".join([str(tree) for tree in trees])
        except ValueError as e:
            response = f"I am sorry, I don't understand your task: {prompt}"
    else:
        response = f"Unfortunately, I do not understand your request, but the web says https://www.google.com/search?q={urllib.parse.quote(prompt.lower())}"

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
