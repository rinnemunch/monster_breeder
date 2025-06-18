import requests

response = requests.get("http://localhost:8080/new")

if response.status_code == 200:
    monster = response.json()
    print("Got a monster from Go!")
    print(monster)
else:
    print("Failed to get monster:", response.status_code)
