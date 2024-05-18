Replace with your values
    client_id = 'boKvRRPiSiaMXXx4EBEALg'
    client_secret = 'nF9CJ8G23lk2VTpNE0yous1ZMVLtu5rs'
    redirect_uri = 'http://localhost:4000/redirect'
    authorization_code = request.args.get('code')

    # Zoom token endpoint
    token_url = 'https://zoom.us/oauth/token'

    # Headers and data for the token request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri
    }

    # Make the request to get the access token
    response = requests.post(
        token_url,
        headers=headers,
        data=data,
        auth=HTTPBasicAuth(client_id, client_secret)
    )

    # Check the response
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)
    else:
        print(f"Failed to get access token. Status code: {response.status_code}")
        print("Response:", response.json())