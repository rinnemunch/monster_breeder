package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"time"
)

// no built in for max
func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

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

func breedMonsters(parent1, parent2 Monster) Monster {
	// Randomly inherit Name and Color
	var name string
	if rand.Intn(2) == 0 {
		name = parent1.Name
	} else {
		name = parent2.Name
	}

	var color string
	if rand.Intn(2) == 0 {
		color = parent1.Color
	} else {
		color = parent2.Color
	}

	// Blend strength and speed
	strength := (parent1.Strength + parent2.Strength) / 2
	speed := (parent1.Speed + parent2.Speed) / 2

	// Rarity
	var rarity string
	if rarityRank(parent1.Rarity) > rarityRank(parent2.Rarity) {
		rarity = parent1.Rarity
	} else {
		rarity = parent2.Rarity
	}

	return Monster{
		Name:       name,
		Color:      color,
		Strength:   strength,
		Speed:      speed,
		Rarity:     rarity,
		Generation: max(parent1.Generation, parent2.Generation) + 1,
	}
}

func rarityRank(r string) int {
	switch r {
	case "Common":
		return 1
	case "Uncommon":
		return 2
	case "Rare":
		return 3
	case "Epic":
		return 4
	case "Legendary":
		return 5
	default:
		return 0
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
