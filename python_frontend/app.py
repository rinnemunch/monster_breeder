import tkinter as tk
import requests
import json
import os

SAVE_FILE = "saved_monsters.json"

if not os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "w") as f:
        json.dump([], f)

def save_monster(monster):
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    data.append(monster)

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)



# ''' Console testing
# # two random monsters
# monster1 = requests.get("http://localhost:8080/new").json()
# monster2 = requests.get("http://localhost:8080/new").json()

# # Print parents
# print("Parent 1:", monster1)
# print("Parent 2:", monster2)

# # Send to /breed route
# response = requests.post("http://localhost:8080/breed", json=[monster1, monster2])

# # Check and print the child
# if response.status_code == 200:
#     child = response.json()
#     print("\nChild Monster:", child)
# else:
#     print("Breeding failed with status:", response.status_code)
# '''

parent1 = None
parent2 = None

def generate_monsters():
    global parent1, parent2
    parent1 = requests.get("http://localhost:8080/new").json()
    parent2 = requests.get("http://localhost:8080/new").json()

    display.delete("1.0", tk.END)
    display.insert(tk.END, "Parent 1:\n" + json.dumps(parent1, indent=2) + "\n\n")
    display.insert(tk.END, "Parent 2:\n" + json.dumps(parent2, indent=2))

def breed_monsters():
    if parent1 and parent2:
        response = requests.post("http://localhost:8080/breed", json=[parent1, parent2])
        display.delete("1.0", tk.END)
        if response.status_code == 200:
            child = response.json()
            display.insert(tk.END, "Child Monster:\n" + json.dumps(child, indent=2))
        else:
            display.insert(tk.END, "Breeding failed.")
    else:
        display.delete("1.0", tk.END)
        display.insert(tk.END, "Please generate two parents first.")

# GUI (tkinter)
root = tk.Tk()
root.title("Monster Breeder")

def save_last_monster():
    content = display.get("1.0", tk.END).strip()
    if content.startswith("Child Monster:") or content.startswith("Parent 1:"):
        try:
            json_data = content.split(":\n", 1)[1]
            monster = json.loads(json_data)
            save_monster(monster)
            display.insert(tk.END, "\n\n✅ Monster saved!")
        except Exception as e:
            display.insert(tk.END, f"\n\n❌ Failed to save: {e}")
    else:
        display.insert(tk.END, "\n\n⚠️ No valid monster to save.")


# Buttons
generate_btn = tk.Button(root, text="Generate Parents", command=generate_monsters)
generate_btn.pack(pady=5)

breed_btn = tk.Button(root, text="Breed Monsters", command=breed_monsters)
breed_btn.pack(pady=5)

save_btn = tk.Button(root, text="Save Monster", command=save_last_monster)
save_btn.pack(pady=5)

display = tk.Text(root, width=50, height=20)
display.pack()

root.mainloop()
