# main.py

import pandas as pd
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Union, Tuple

# Load Pokémon data
df = pd.read_csv('pokemon.csv')

# Abstract Strategy for Battle
class BattleStrategy(ABC):
    @abstractmethod
    def calculate_damage(self, attacker_stats: Dict[str, Union[str, float]], defender_stats: Dict[str, float]) -> float:
        pass

class BasicBattleStrategy(BattleStrategy):
    def calculate_damage(self, attacker_stats: Dict[str, Union[str, float]], defender_stats: Dict[str, float]) -> float:
        attack = attacker_stats['attack']
        against_type1 = defender_stats.get('against_' + attacker_stats['type1'], 1)
        against_type2 = defender_stats.get('against_' + attacker_stats['type2'], 1)
        damage = (attack / 200) * 100 - (((against_type1 / 4) * 100) + ((against_type2 / 4) * 100))
        return damage

# Pokemon class
class Pokemon:
    def __init__(self, name: str, type1: str, type2: str, attack: float):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.attack = attack

    @classmethod
    def from_dataframe(cls, name: str, df: pd.DataFrame) -> 'Pokemon':
        row = df[df['name'] == name].iloc[0]
        return cls(name, row['type1'], row['type2'], row['attack'])

# Battle class
class Battle:
    def __init__(self, pokemon_a: Pokemon, pokemon_b: Pokemon, strategy: BattleStrategy):
        self.pokemon_a = pokemon_a
        self.pokemon_b = pokemon_b
        self.strategy = strategy
        self.result = None

    def execute(self) -> str:
        stats_a = {'type1': self.pokemon_a.type1, 'type2': self.pokemon_a.type2, 'attack': self.pokemon_a.attack}
        stats_b = {'against_' + self.pokemon_a.type1: 1, 'against_' + self.pokemon_a.type2: 1}  # Replace with real stats

        damage_a = self.strategy.calculate_damage(stats_a, stats_b)
        damage_b = self.strategy.calculate_damage(stats_b, {'against_' + self.pokemon_b.type1: 1, 'against_' + self.pokemon_b.type2: 1})

        if damage_a > damage_b:
            return f"{self.pokemon_a.name} wins"
        elif damage_b > damage_a:
            return f"{self.pokemon_b.name} wins"
        else:
            return "Draw"

# Factory for creating Battles
class BattleFactory:
    @staticmethod
    def create_battle(pokemon_a_name: str, pokemon_b_name: str, df: pd.DataFrame) -> Battle:
        pokemon_a = Pokemon.from_dataframe(pokemon_a_name, df)
        pokemon_b = Pokemon.from_dataframe(pokemon_b_name, df)
        return Battle(pokemon_a, pokemon_b, BasicBattleStrategy())

if __name__ == "__main__":
    battle = BattleFactory.create_battle("bulbasaur", "charmander", df)
    result = battle.execute()
    print(result)
