import tkinter as tk
import requests
import json
import os
from PIL import Image, ImageDraw, ImageTk


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

    img1 = ImageTk.PhotoImage(load_monster_sprite(parent1["Name"]))
    img2 = ImageTk.PhotoImage(load_monster_sprite(parent2["Name"]))
    parent1_sprite.config(image=img1)
    parent1_sprite.image = img1
    parent2_sprite.config(image=img2)
    parent2_sprite.image = img2



def breed_monsters():
    if parent1 and parent2:
        response = requests.post("http://localhost:8080/breed", json=[parent1, parent2])
        display.delete("1.0", tk.END)

        if response.status_code == 200:
            child = response.json()
            display.insert(tk.END, "Child Monster:\n" + json.dumps(child, indent=2))

            child_name = child["Name"].replace(" ", "_")
            image_path = f"sprites/{child_name}.png"

            try:
                img = Image.open(image_path).resize((100, 100))
                img = ImageTk.PhotoImage(img)
                if 'child_image_label' in globals():
                    child_image_label.configure(image=img)
                    child_image_label.img = img
                child_image_label.image = img
            except Exception as e:
                print(f"[ERROR] Child sprite not found for {child_name}: {e}")
                child_image_label.configure(image=None)
        else:
            display.insert(tk.END, "Breeding failed.")
    else:
        display.delete("1.0", tk.END)
        display.insert(tk.END, "Please generate two parents first.")


# GUI (tkinter)
root = tk.Tk()
root.title("Monster Breeder")

# Parent display
parent_sprite_frame = tk.Frame(root)
parent_sprite_frame.pack(pady=5)

parent1_label = tk.Label(parent_sprite_frame)
parent1_label.pack(side="left", padx=10)

parent2_label = tk.Label(parent_sprite_frame)
parent2_label.pack(side="left", padx=10)

# Functions
def save_last_monster():
    content = display.get("1.0", tk.END).strip()
    if content.startswith("Child Monster:"):
        try:
            json_data = content.split("Child Monster:\n", 1)[1]
            monster = json.loads(json_data)
            save_monster(monster)
            display.insert(tk.END, "\n\n✅ Monster saved!")
        except Exception as e:
            display.insert(tk.END, f"\n\n❌ Failed to save: {e}")
    else:
        display.insert(tk.END, "\n\n⚠️ Only Child Monsters can be saved.")

def load_saved_monsters():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def load_monster_sprite(name):
    try:
        img_path = f"sprites/{name.lower()}.png"
        print(f"[INFO] Trying to load: {img_path}")
        img = Image.open(img_path).resize((64, 64))
        return img
    except FileNotFoundError:
        print(f"[ERROR] Sprite not found for: {img_path}")
        return Image.new("RGBA", (64, 64), (0, 0, 0, 0))


def refresh_monster_list():
    monster_listbox.delete(0, tk.END)
    monsters = load_saved_monsters()
    for i, monster in enumerate(monsters):
        display_name = f"{i+1}. {monster['Name']} (Gen {monster['Generation']})"
        monster_listbox.insert(tk.END, display_name)

def show_selected_monster(event):
    selection = monster_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    monsters = load_saved_monsters()
    selected = monsters[index]
    display.delete("1.0", tk.END)
    display.insert(tk.END, json.dumps(selected, indent=2))

    img = load_monster_sprite(selected["Name"])
    tk_img = ImageTk.PhotoImage(img)
    sprite_label.configure(image=tk_img)
    sprite_label.image = tk_img

def evolve_selected_monster():
    selection = monster_listbox.curselection()
    if not selection:
        display.insert(tk.END, "\n\n⚠️ No monster selected to evolve.")
        return

    index = selection[0]
    monsters = load_saved_monsters()
    selected = monsters[index]

    try:
        response = requests.post("http://localhost:8080/evolve", json=selected)
        if response.status_code == 200:
            evolved = response.json()
            display.delete("1.0", tk.END)
            display.insert(tk.END, "Evolved Monster:\n" + json.dumps(evolved, indent=2))
        else:
            display.insert(tk.END, "\n\n❌ Evolution failed.")
    except Exception as e:
        display.insert(tk.END, f"\n\n❌ Error: {e}")

def save_evolved_monster():
    content = display.get("1.0", tk.END).strip()
    if content.startswith("Evolved Monster:"):
        try:
            json_data = content.split("Evolved Monster:\n", 1)[1]
            monster = json.loads(json_data)
            save_monster(monster)
            display.insert(tk.END, "\n\n✅ Evolved monster saved!")
            refresh_monster_list()
        except Exception as e:
            display.insert(tk.END, f"\n\n❌ Failed to save: {e}")
    else:
        display.insert(tk.END, "\n\n⚠️ No evolved monster to save.")

def battle_selected_monsters():
    selection = monster_listbox.curselection()
    if len(selection) != 2:
        display.insert(tk.END, "\n\n⚠️ Please select exactly two monsters to battle.")
        return

    monsters = load_saved_monsters()
    m1 = monsters[selection[0]]
    m2 = monsters[selection[1]]

    try:
        response = requests.post("http://localhost:8080/battle", json=[m1, m2])
        display.delete("1.0", tk.END)
        if response.status_code == 200:
            result = response.json()
            display.insert(tk.END, "🏆 Battle Result:\n")
            display.insert(tk.END, f"Winner: {result['winner']['Name']}\n")
            display.insert(tk.END, f"Loser: {result['loser']['Name']}\n\n")
            display.insert(tk.END, "📜 Battle Log:\n" + "\n".join(result['log']))
        else:
            display.insert(tk.END, "❌ Battle failed.")
    except Exception as e:
        display.insert(tk.END, f"\n\n❌ Error: {e}")


# Buttons
button_frame = tk.Frame(root)
button_frame.pack(side="bottom", pady=10)

generate_btn = tk.Button(button_frame, text="Generate Parents", command=generate_monsters)
generate_btn.pack(side="left", padx=5)

breed_btn = tk.Button(button_frame, text="Breed Monsters", command=breed_monsters)
breed_btn.pack(side="left", padx=5)

save_btn = tk.Button(button_frame, text="Save Monster", command=save_last_monster)
save_btn.pack(side="left", padx=5)

evolve_btn = tk.Button(button_frame, text="Evolve Monster", command=evolve_selected_monster)
evolve_btn.pack(side="left", padx=5)

save_evolved_btn = tk.Button(button_frame, text="Save Evolved", command=save_evolved_monster)
save_evolved_btn.pack(side="left", padx=5)

battle_btn = tk.Button(button_frame, text="Battle", command=battle_selected_monsters)
battle_btn.pack(side="left", padx=5)


btn_style = {"font": ("Consolas", 10), "bg": "#222", "fg": "#fff", "activebackground": "#444"}

generate_btn.config(**btn_style)
breed_btn.config(**btn_style)
save_btn.config(**btn_style)
evolve_btn.config(**btn_style)
save_evolved_btn.config(**btn_style)
battle_btn.config(**btn_style)

# List box
monster_listbox = tk.Listbox(root, width=50, selectmode=tk.MULTIPLE)
monster_listbox.pack(pady=5)
monster_listbox.bind("<<ListboxSelect>>", show_selected_monster)

sprite_row = tk.Frame(root)
sprite_row.pack(pady=10)

parent1_sprite = tk.Label(sprite_row)
parent1_sprite.pack(side="left", padx=10)

plus_label = tk.Label(sprite_row, text="+", font=("Consolas", 16))
plus_label.pack(side="left")

parent2_sprite = tk.Label(sprite_row)
parent2_sprite.pack(side="left", padx=10)

equals_label = tk.Label(sprite_row, text="=", font=("Consolas", 16))
equals_label.pack(side="left")

child_image_label = tk.Label(sprite_row)
child_image_label.pack(side="left", padx=10)

display = tk.Text(root, width=50, height=20)
display.pack()

sprite_label = tk.Label(root)
sprite_label.pack(pady=5)

refresh_monster_list()
root.mainloop()
