import requests

# two random monsters
monster1 = requests.get("http://localhost:8080/new").json()
monster2 = requests.get("http://localhost:8080/new").json()

# Print parents
print("Parent 1:", monster1)
print("Parent 2:", monster2)

# Send to /breed route
response = requests.post("http://localhost:8080/breed", json=[monster1, monster2])

# Check and print the child
if response.status_code == 200:
    child = response.json()
    print("\nChild Monster:", child)
else:
    print("Breeding failed with status:", response.status_code)
