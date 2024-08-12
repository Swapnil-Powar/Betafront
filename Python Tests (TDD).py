# test_main.py

import unittest
from unittest.mock import patch
from main import Pokemon, Battle, BasicBattleStrategy, BattleFactory

class TestPokemonBattle(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'name': ['bulbasaur', 'charmander'],
            'type1': ['grass', 'fire'],
            'type2': ['poison', ''],
            'attack': [49, 52]
        })

    def test_pokemon_initialization(self):
        pokemon = Pokemon.from_dataframe('bulbasaur', self.df)
        self.assertEqual(pokemon.name, 'bulbasaur')
        self.assertEqual(pokemon.attack, 49)

    def test_battle(self):
        battle = BattleFactory.create_battle('bulbasaur', 'charmander', self.df)
        result = battle.execute()
        self.assertIn('wins', result)

if __name__ == '__main__':
    unittest.main()
