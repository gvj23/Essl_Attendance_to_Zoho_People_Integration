import requests

CLIENT_ID = "1000.22RMIEUJD3GZVEVDIUVPWQPV4Q52DN"
CLIENT_SECRET = "9fccf7b52e3f9ae3303a47c11cdf6f930ac1bcd55d"
REFRESH_TOKEN = "1000.7c4f65209f5e80e34ed5380f24558979.93f69d5716b40c3097790a05e2f6858c"

url = "https://accounts.zoho.in/oauth/v2/token"

data = {
    "refresh_token": REFRESH_TOKEN,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "refresh_token"
}

response = requests.post(url, data=data)

print(response.text)
