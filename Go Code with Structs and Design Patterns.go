// main.go

package main
import (
    "fmt"
    "math/rand"
    "time"
)

type Pokemon struct {
    Name   string
    Type1  string
    Type2  string
    Attack float64
}

type BattleStrategy interface {
    CalculateDamage(attacker Pokemon, defender Pokemon) float64
}

type BasicBattleStrategy struct{}

func (b BasicBattleStrategy) CalculateDamage(attacker Pokemon, defender Pokemon) float64 {
    damage := (attacker.Attack / 200) * 100 - (0.5 * 100) // Simplified
    return damage
}

type Battle struct {
    PokemonA  Pokemon
    PokemonB  Pokemon
    Strategy  BattleStrategy
}

func (b Battle) Execute() string {
    damageA := b.Strategy.CalculateDamage(b.PokemonA, b.PokemonB)
    damageB := b.Strategy.CalculateDamage(b.PokemonB, b.PokemonA)

    if damageA > damageB {
        return fmt.Sprintf("%s wins", b.PokemonA.Name)
    } else if damageB > damageA {
        return fmt.Sprintf("%s wins", b.PokemonB.Name)
    }
    return "Draw"
}

func NewBattle(pokemonA Pokemon, pokemonB Pokemon) Battle {
    return Battle{
        PokemonA: pokemonA,
        PokemonB: pokemonB,
        Strategy: BasicBattleStrategy{},
    }
}

func main() {
    rand.Seed(time.Now().UnixNano())
    pokemonA := Pokemon{Name: "Bulbasaur", Type1: "Grass", Type2: "Poison", Attack: 49}
    pokemonB := Pokemon{Name: "Charmander", Type1: "Fire", Type2: "", Attack: 52}

    battle := NewBattle(pokemonA, pokemonB)
    result := battle.Execute()
    fmt.Println(result)
}
