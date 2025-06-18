package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
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
		Strength:   rand.Intn(100) + 1, // 1–100
		Speed:      rand.Intn(100) + 1,
		Rarity:     rarities[rand.Intn(len(rarities))],
		Generation: 1,
	}
}

func main() {
	monster := generateRandomMonster()

	monsterJSON, err := json.MarshalIndent(monster, "", "  ")
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println(string(monsterJSON))
}
