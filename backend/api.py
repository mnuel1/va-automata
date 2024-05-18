from flask import Flask, redirect, request
import requests
import json
from requests.auth import HTTPBasicAuth
app = Flask(__name__)

@app.route('/')
def redirect_to_zoom():    
    
    # zoom_oauth_url = "https://zoom.us/oauth/authorize?client_id=boKvRRPiSiaMXXx4EBEALg&response_type=code&redirect_uri=http://localhost:4000/redirect"
    zoom_oauth_url = "http://localhost:4000/redirect"
    return redirect(zoom_oauth_url)

@app.route('/redirect')
def printhello():    
    
    # # Replace with your values
    # client_id = 'boKvRRPiSiaMXXx4EBEALg'
    # client_secret = 'nF9CJ8G23lk2VTpNE0yous1ZMVLtu5rs'
    # redirect_uri = 'http://localhost:4000/redirect'
    # authorization_code = request.args.get('code')

    # # Zoom token endpoint
    # token_url = 'https://zoom.us/oauth/token'

    # # Headers and data for the token request
    # headers = {
    #     'Content-Type': 'application/x-www-form-urlencoded'
    # }

    # data = {
    #     'grant_type': 'authorization_code',
    #     'code': authorization_code,
    #     'redirect_uri': redirect_uri
    # }

    # # Make the request to get the access token
    # response = requests.post(
    #     token_url,
    #     headers=headers,
    #     data=data,
    #     auth=HTTPBasicAuth(client_id, client_secret)
    # )

    # # Check the response
    # if response.status_code == 200:
    #     tokens = response.json()
    #     access_token = tokens['access_token']
    #     refresh_token = tokens['refresh_token']
    #     # print(access_token)
    #     # Zoom API endpoint for creating a meeting
    url = "https://api.zoom.us/v2/users/me/meetings"

    # Headers for the request
    headers = {
        'Authorization': f'Bearer eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6IjYyMjU0Mzc3LTdkNTItNDk3Mi1hNzFhLTRjN2QzYWRlM2FkMSJ9.eyJ2ZXIiOjksImF1aWQiOiIwN2FjMjc3YzQxOGVmODYzYzA0YjU4ZThlZDAxZTY1NCIsImNvZGUiOiJWS0VRQjJuaUlGZmROYkNsa01UU05DWHdEckVmU3QyRXciLCJpc3MiOiJ6bTpjaWQ6Ym9LdlJSUGlTaWFNWFh4NEVCRUFMZyIsImdubyI6MCwidHlwZSI6MCwidGlkIjowLCJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiJFNjU4VGJQc1MzcVZQSU5XTzFRelNnIiwibmJmIjoxNzE1OTg2NjU1LCJleHAiOjE3MTU5OTAyNTUsImlhdCI6MTcxNTk4NjY1NSwiYWlkIjoiRkpucmZsSHhSS0NiMklOaTZ1NjJTUSJ9.tGENWeLH17og79tQsONurx8ut_Pwk5PmdYhedoEWis-jJQL7LljfXbOTW1KdG8JmLx2r6brCoreXQGSZl7cLpQ',
        'Content-Type': 'application/json'
    }

    # Payload for creating a meeting
    payload = {
        "topic": "Example Meeting",
        "type": 2,  # Scheduled meeting
        "start_time": "2024-05-18T10:00:00Z",  # UTC time in ISO 8601 format
        "duration": 30,  # duration in minutes
        "timezone": "UTC",
        "agenda": "Discuss project updates",
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

    # Make the request to create the meeting
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check the response
    if response.status_code == 201:
        print("Meeting created successfully!")
        print("Meeting details:", response.json())
    else:
        print(f"Failed to create meeting. Status code: {response.status_code}")
        print("Response:", response.json())
    return response.text
    # else:
    #     print(f"Failed to get access token. Status code: {response.status_code}")
    #     print("Response:", response.json())
    # return 'success'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)
