import requests

def fetch_api(url):
    response = requests.get(url)
    data = response.json()
    print(data)

url = "https://api.genderize.io?name=luc"
result = fetch_api(url)