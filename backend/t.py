import requests

# Set up authentication
token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IjkwVlBkS04zQjB2NXMxMHpsX2J4Z3loZlY3UkREZXpuX1hESUNEQ3J0aEkiLCJhbGciOiJSUzI1NiIsIng1dCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCIsImtpZCI6IkwxS2ZLRklfam5YYndXYzIyeFp4dzFzVUhIMCJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8xNDRjOWUyZS0yYjdkLTQ3MWQtOTZjOC03ZGMyOGVhZTY5MDYvIiwiaWF0IjoxNzE1NjIwNTg2LCJuYmYiOjE3MTU2MjA1ODYsImV4cCI6MTcxNTcwNzI4NiwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFUUUF5LzhXQUFBQWQ4LzVvWkZnVzlRelRpRlRvemFkWTZSeUVBS1g2cmRiS0N3U05iRkVoY3V4MExhVS9Hc2ZvTWR1M0YzQytSd3ciLCJhbXIiOlsicHdkIl0sImFwcF9kaXNwbGF5bmFtZSI6IkdyYXBoIEV4cGxvcmVyIiwiYXBwaWQiOiJkZThiYzhiNS1kOWY5LTQ4YjEtYThhZC1iNzQ4ZGE3MjUwNjQiLCJhcHBpZGFjciI6IjAiLCJmYW1pbHlfbmFtZSI6Ik1hcmluIiwiZ2l2ZW5fbmFtZSI6Ik1hbnVlbCIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjE1Mi4zMi4xMTIuNjEiLCJuYW1lIjoiTWFudWVsIE1hcmluIiwib2lkIjoiMTAzNjgxMjEtNTA3MC00ZTFhLTg5YWQtMDk0OThkNmE5NzYyIiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMyMDAxODVFMDc3N0UiLCJyaCI6IjAuQVhJQUxwNU1GSDBySFVlV3lIM0NqcTVwQmdNQUFBQUFBQUFBd0FBQUFBQUFBQUJ5QUEwLiIsInNjcCI6Im9wZW5pZCBwcm9maWxlIFRlYW0uUmVhZEJhc2ljLkFsbCBVc2VyLlJlYWQgZW1haWwgVGVhbS5DcmVhdGUiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiJocXRJa1RkTXNDT3NFM21vdGZIOGo3cnhPMDN5eFY0MERRSEYxYjVaX3hZIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkFTIiwidGlkIjoiMTQ0YzllMmUtMmI3ZC00NzFkLTk2YzgtN2RjMjhlYWU2OTA2IiwidW5pcXVlX25hbWUiOiJtYW51ZWwubWFyaW5AdHVwLmVkdS5waCIsInVwbiI6Im1hbnVlbC5tYXJpbkB0dXAuZWR1LnBoIiwidXRpIjoiOWFuMVlfVkNqVUNUV0x2Sk5zZVlBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19jYyI6WyJDUDEiXSwieG1zX3NzbSI6IjEiLCJ4bXNfc3QiOnsic3ViIjoiaG11YXVMWVVwMTl2Sm10MFJDUGJBODR4V3hVN0c2eXJXa19vc19RTHJBVSJ9LCJ4bXNfdGNkdCI6MTQ4OTc0NzQ0Mn0.CBWXI4dgHY-twf6M_frvnU70Hxg-gmPgfsUd-5sMVIj6gtjtBXGSSEx3h3Lw1oznPpuwI9hAn09S7KjflWXADI04J73mtRBuvdQxf22bpb4tkxSvQdyG9bfiWwRECgVoPxjGZxRuMxpsCSpnPvmogDCFDpjoLAZM2o8xCWbFAEO89qBq8P5p1k7aqYqgPqh3cQIJwzd4p5htsrYA-rNAO0CrusFHBP_nQNe0Kx1CmFumYwBvB2P-C9ShdzYbFCWlbKuma4m0ZXRQ7UqiFMbppvPdXtg-zkbbhiRf0BFJkWs6Gvm7F0couJoDjD11yUNtI3S5vNnj5Xl1-0AxTSVIpw"  # Replace with your actual access token

# # Make request to get user's profile
# url = "https://graph.microsoft.com/v1.0/teams"
# headers = {
#     "Authorization": "Bearer " + token,
#     "Content-Type": "application/json"
# }
# response = requests.get(url, headers=headers)

# # Handle response
# if response.status_code == 200:
#     user_profile = response.json()
#     print("User profile:", user_profile)
# else:
#     print("Failed to retrieve user profile. Status code:", response.status_code)

# Define the team ID
team_id = "49c40f6b-30cc-4545-8817-7aaf56dd8654"  # Replace with the ID of the team you want to update

# Define the URL and headers
url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/schedule"
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"
}

# Define the payload (schedule data)
payload = {
    "enabled": True,
    "timeZone": "America/Chicago"
}

# Make the PUT request
response = requests.put(url, headers=headers, json=payload)

# Handle response
if response.status_code == 204:
    print("Schedule settings updated successfully.")
else:
    print("Failed to update schedule settings. Status code:", response.status_code)
    print("Error message:", response.text)