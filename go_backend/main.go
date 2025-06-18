package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"time"
)

type Monster struct {
	Name       string
	Color      string
	Strength   int
	Speed      int
	Rarity     string
	Generation int
}

func generateRandomMonster() Monster {
	names := []string{"Grizzle", "Zaptoad", "Blazefang", "Nibbler", "Frostjaw"}
	colors := []string{"Red", "Blue", "Green", "Purple", "Black"}
	rarities := []string{"Common", "Uncommon", "Rare", "Epic", "Legendary"}

	rand.Seed(time.Now().UnixNano())

	return Monster{
		Name:       names[rand.Intn(len(names))],
		Color:      colors[rand.Intn(len(colors))],
		Strength:   rand.Intn(100) + 1,
		Speed:      rand.Intn(100) + 1,
		Rarity:     rarities[rand.Intn(len(rarities))],
		Generation: 1,
	}
}

func newMonsterHandler(w http.ResponseWriter, r *http.Request) {
	monster := generateRandomMonster()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(monster)
}

func main() {
	http.HandleFunc("/new", newMonsterHandler)

	fmt.Println("Server running at http://localhost:8080")
	http.ListenAndServe(":8080", nil)
}
