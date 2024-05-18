import requests

# Replace 'yourtokenhere' with your actual JWT token
jwt_token = 'SgTud2znHDxqYu8-rR3QsWJj6PKyVNBkA'

# Zoom API endpoint to get user information
url = 'https://zoom.us/oauth/token'

# Headers for the request
headers = {
    'Authorization': f'Bearer {jwt_token}',
    'Content-Type':	'application/x-www-form-urlencoded'
}

# Options for the request
options = {
    'method': 'GET',
    'url': url,
    'headers': headers
}

# Make the request
response = requests.get(url, headers=headers)

# Check for errors
if response.status_code != 200:
    raise Exception(f"Request failed: {response.status_code}, {response.text}")

# Print the response body
print(response.text)
