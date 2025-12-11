import requests

url = "your-chall-url/api/admin"
token = "admin_token_here"
payload = {
    "token": token
}
r = requests.post(url, json=payload)
print(r.text)
