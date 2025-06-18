package main

import "fmt"

type Monster struct {
	Name       string
	Color      string
	Strength   int
	Speed      int
	Rarity     string
	Generation int
}

func main() {
	fmt.Println("Monster struct defined.")
}
