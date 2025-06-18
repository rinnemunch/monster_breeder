import tkinter as tk
import requests
import json

'''
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
'''  # Console testing

def generate_monster():
    response = requests.get("http://localhost:8080/new")
    if response.status_code == 200:
        monster = response.json()
        display.delete("1.0", tk.END)
        display.insert(tk.END, json.dumps(monster, indent=2))
    else:
        display.insert(tk.END, "Failed to generate monster.\n")

# GUI setup
root = tk.Tk()
root.title("Monster Viewer")

generate_btn = tk.Button(root, text="Generate Monster", command=generate_monster)
generate_btn.pack(pady=10)

display = tk.Text(root, width=40, height=15)
display.pack()

root.mainloop()
