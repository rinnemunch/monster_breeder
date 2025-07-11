# 🧬 Monster Breeder (Python + Go)

A desktop monster breeding app powered by a **Python (Tkinter)** frontend and a **Go backend**.
Generate monsters, breed them, evolve them, and even battle—all with sprite support and JSON-based communication between two languages.

---

## 🚀 Features

- Generate random monsters from Go backend
- Breed two monsters and create unique offspring
- Evolve saved monsters with a single click
- Battle any two saved monsters
- Save and load monster data locally (`.json`)
- Display custom 8-bit styled sprites per monster
- Connects via clean RESTful HTTP endpoints

---

## 🧠 What I Learned

- Connecting Python and Go using HTTP requests
- Handling JSON data across two languages
- Designing a modular API to separate backend logic from the UI
- Managing sprite assets dynamically based on monster names

---

## 🐍 Python (Frontend)

- Built with `tkinter` for the UI
- Displays monster info, images, and action buttons
- Handles interactions like breed, evolve, save, battle
- Stores saved monsters in `saved_monsters.json`

---

## 🦍 Go (Backend)

- Hosts a simple HTTP server
- Routes:
  - `GET /new` → returns a random monster
  - `POST /breed` → accepts two parents, returns child
  - `POST /evolve` → evolves a given monster
  - `POST /battle` → simulates a fight and returns winner/log

---

## 🖼 Sprites

Place monster sprite images in the `sprites/` folder.
Image filenames should match the monster’s name (lowercase, underscores instead of spaces).
Example:

sprites/phantom_lich.png
sprites/king_slime.png

---

## 📦 How to Run

### Backend (Go)

```bash
go run main.go
```

## 🐍 Python

```bash
python app.py
```

Make sure both are running in the same environment. Python will send requests to http://localhost:8080.

# MEDIUM DEVLOGS

part 1: https://medium.com/@fulton_shaun/part-1-python-go-project-exploring-multi-language-development-986f208fa6ac
part 2: (Scheduled post)
part 3: (Scheduled post)
