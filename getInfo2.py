import requests

#okta authentication
okta_auth_url = "https://your-okta-domain.com/oauth2/v1/token"
client_id = "your-client-id"
client_secret = "your-client-secret"
okta_username = "your-okta-username" #if does not work try with bitbucket username password
okta_password = "your-okta-password"

payload = {
    "grant_type": "password",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "openid",
    "username": okta_username,
    "password": okta_password,
}

response = requests.post(okta_auth_url, data=payload)
if response.status_code == 200:
    okta_access_token = response.json().get("access_token")
else:
    print("Error authenticating with Okta")
    exit(0)


#get info from bitbucket repository
username = 'chirag220401'
repository = 'chirag-demo-project1/demo-repo1'
bitbucket_url = f'https://api.bitbucket.org/2.0/repositories/{username}/{repository}'

headers = {
    "Authorization": f"Bearer {okta_access_token}",
}

response = requests.get(bitbucket_url, headers=headers)

if response.status_code == 200:
    # Successfully accessed Bitbucket repository
    print(response.json())
else:
    print(f"Error accessing Bitbucket: {response.status_code} - {response.text}")

