// main_test.go

package main
import (
    "testing"
)

func TestBasicBattleStrategy(t *testing.T) {
    strategy := BasicBattleStrategy{}
    pokemonA := Pokemon{Name: "Bulbasaur", Type1: "Grass", Type2: "Poison", Attack: 49}
    pokemonB := Pokemon{Name: "Charmander", Type1: "Fire", Type2: "", Attack: 52}
    damageA := strategy.CalculateDamage(pokemonA, pokemonB)
    damageB := strategy.CalculateDamage(pokemonB, pokemonA)

    if damageA <= 0 || damageB <= 0 {
        t.Errorf("Damage calculation failed, got %f and %f", damageA, damageB)
    }
}

func TestBattle(t *testing.T) {
    pokemonA := Pokemon{Name: "Bulbasaur", Type1: "Grass", Type2: "Poison", Attack: 49}
    pokemonB := Pokemon{Name: "Charmander", Type1: "Fire", Type2: "", Attack: 52}

    battle := NewBattle(pokemonA, pokemonB)
    result := battle.Execute()

    if result != "Charmander wins" && result != "Draw" {
        t.Errorf("Battle result is incorrect, got %s", result)
    }
}
