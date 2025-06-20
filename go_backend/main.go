package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"sort"
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

var monsterTemplates = []Monster{
	{Name: "skeleton", Color: "Gray", Strength: 35, Speed: 20, Rarity: "Common", Generation: 1},
	{Name: "goblin", Color: "Green", Strength: 40, Speed: 30, Rarity: "Uncommon", Generation: 1},
	{Name: "slime", Color: "Blue", Strength: 25, Speed: 40, Rarity: "Common", Generation: 1},
	{Name: "orc", Color: "Red", Strength: 60, Speed: 25, Rarity: "Rare", Generation: 1},
	{Name: "wraith", Color: "Purple", Strength: 45, Speed: 45, Rarity: "Epic", Generation: 1},
}

var hybridMap = map[string]string{
	"goblin skeleton":   "bone_raider",
	"skeleton slime":    "gelatin_ghoul",
	"slime goblin":      "muck_bandit",
	"goblin orc":        "grunt_commander",
	"orc skeleton":      "warlord_remnant",
	"orc slime":         "gore_ooze",
	"slime slime":       "king_slime",
	"slime orc":         "king_slime",
	"goblin goblin":     "goblin_bomber",
	"wraith goblin":     "shade_stabber",
	"skeleton goblin":   "shade_stabber",
	"skeleton skeleton": "skeleton_king",
	"wraith slime":      "echo_slime",
	"orc wraith":        "hellreaver",
	"skeleton wraith":   "phantom_lich",
	"orc orc":           "bloodfang",
	"wraith wraith":     "void_walker",
}

func generateRandomMonster() Monster {
	return monsterTemplates[rand.Intn(len(monsterTemplates))]
}

func breedMonsters(parent1, parent2 Monster) Monster {
	names := []string{parent1.Name, parent2.Name}
	sort.Strings(names)
	joined := names[0] + " " + names[1]

	name := joined
	if hybridName, ok := hybridMap[joined]; ok {
		name = hybridName
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

	// Mutation chance: 10%
	if rand.Float64() < 0.10 {
		strength += rand.Intn(10) + 1
		fmt.Println("Mutation! Strength increased.")
	}

	if rand.Float64() < 0.10 {
		speed += rand.Intn(10) + 1
		fmt.Println("Mutation! Speed increased.")
	}

	if rand.Float64() < 0.05 {
		rarity = "Legendary"
		fmt.Println("Mutation! Monster became Legendary.")
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

func rankToRarity(rank int) string {
	switch rank {
	case 1:
		return "Common"
	case 2:
		return "Uncommon"
	case 3:
		return "Rare"
	case 4:
		return "Epic"
	case 5:
		return "Legendary"
	default:
		return "Common"
	}
}

func newMonsterHandler(w http.ResponseWriter, r *http.Request) {
	monster := generateRandomMonster()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(monster)
}

func breedHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST allowed", http.StatusMethodNotAllowed)
		return
	}

	var parents [2]Monster
	err := json.NewDecoder(r.Body).Decode(&parents)
	if err != nil {
		http.Error(w, "Invalid input", http.StatusBadRequest)
		return
	}

	child := breedMonsters(parents[0], parents[1])

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(child)
}

func evolveMonster(m Monster) Monster {
	m.Strength += rand.Intn(5) + 1
	m.Speed += rand.Intn(5) + 1

	if rand.Float64() < 0.20 && rarityRank(m.Rarity) < 5 {
		nextRank := rarityRank(m.Rarity) + 1
		m.Rarity = rankToRarity(nextRank)
		fmt.Println("Evolution! Rarity increased.")
	}

	return m
}

func evolveHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST allowed", http.StatusMethodNotAllowed)
		return
	}

	var monster Monster
	err := json.NewDecoder(r.Body).Decode(&monster)
	if err != nil {
		http.Error(w, "Invalid input", http.StatusBadRequest)
		return
	}

	evolved := evolveMonster(monster)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(evolved)
}

func battleHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST allowed", http.StatusMethodNotAllowed)
		return
	}

	var monsters [2]Monster
	err := json.NewDecoder(r.Body).Decode(&monsters)
	if err != nil {
		http.Error(w, "Invalid input", http.StatusBadRequest)
		return
	}

	winner, loser, log := battleMonsters(monsters[0], monsters[1])

	response := map[string]interface{}{
		"winner": winner,
		"loser":  loser,
		"log":    log,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func battleMonsters(m1, m2 Monster) (winner Monster, loser Monster, log []string) {
	log = append(log, fmt.Sprintf("%s (STR: %d, SPD: %d) VS %s (STR: %d, SPD: %d)", m1.Name, m1.Strength, m1.Speed, m2.Name, m2.Strength, m2.Speed))

	m1Score := m1.Strength + m1.Speed + rand.Intn(20)
	m2Score := m2.Strength + m2.Speed + rand.Intn(20)

	log = append(log, fmt.Sprintf("%s score: %d", m1.Name, m1Score))
	log = append(log, fmt.Sprintf("%s score: %d", m2.Name, m2Score))

	if m1Score > m2Score {
		log = append(log, fmt.Sprintf("%s wins the battle!", m1.Name))
		return m1, m2, log
	}
	log = append(log, fmt.Sprintf("%s wins the battle!", m2.Name))
	return m2, m1, log
}

func main() {
	rand.Seed(time.Now().UnixNano())

	fmt.Println("Starting the monster server with /new and /breed")

	http.HandleFunc("/new", newMonsterHandler)
	http.HandleFunc("/breed", breedHandler)
	http.HandleFunc("/evolve", evolveHandler)
	http.HandleFunc("/battle", battleHandler)

	fmt.Println("Server running at http://localhost:8080")
	fmt.Println("🔥 You are running the CORRECT Go file") //test
	http.ListenAndServe(":8080", nil)
}
