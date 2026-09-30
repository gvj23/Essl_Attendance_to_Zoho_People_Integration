import requests

CLIENT_ID = "1000.22RMIEUJD3GZVEVDIUVPWQPV4Q52DN"
CLIENT_SECRET = "9fccf7b52e3f9ae3303a47c11cdf6f930ac1bcd55d"
AUTH_CODE = "1000.e332c3e4f23d41424b0482befa93fb04.82783989db5a9c67a2d0f166bee5e9a4"

url = "https://accounts.zoho.in/oauth/v2/token"

data = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": "http://localhost",
    "code": AUTH_CODE
}

response = requests.post(url, data=data)

print(response.text)
