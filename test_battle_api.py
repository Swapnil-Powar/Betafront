import unittest
from unittest.mock import patch
from app import FlaskApp, CeleryTask, DataFrame, BattleResults

class TestBattleAPI(unittest.TestCase):
    def setUp(self):
        self.flask_app = FlaskApp()
        self.celery_task = CeleryTask()
        self.data_frame = DataFrame()
        self.battle_results = BattleResults()

    @patch('app.DataFrame.get_pokemon_stats')
    @patch('app.DataFrame.get_against_stats')
    def test_battle_round(self, mock_get_against_stats, mock_get_pokemon_stats):
        # Setup mock returns
        mock_get_pokemon_stats.side_effect = [
            {'type1': 'grass', 'type2': 'poison', 'attack': 49},
            {'type1': 'fire', 'type2': None, 'attack': 52}
        ]
        mock_get_against_stats.side_effect = [
            {'against_grass': 1.0},
            {'against_fire': 0.5}
        ]
        
        # Test the battle round
        result = self.data_frame.battle_round('bulbasaur', 'charmander')
        expected_result = {
            'pokemon_a': {'type1': 'grass', 'type2': 'poison', 'attack': 49},
            'pokemon_b': {'against_type1': 1.0, 'against_type2': None}
        }
        self.assertEqual(result, expected_result)

    @patch('app.CeleryTask.run_battle')
    @patch('app.BattleResults.set')
    def test_battle_api(self, mock_set, mock_run_battle):
        # Test the battle API
        mock_run_battle.return_value = None
        mock_set.return_value = None
        
        response = self.flask_app.battle('bulbasaur', 'charmander')
        self.assertIn('battle_id', response)
        self.assertEqual(response['status'], 'BATTLE_STARTED')

    @patch('app.BattleResults.get')
    def test_battle_status_api(self, mock_get):
        # Setup mock returns
        mock_get.return_value = {
            'status': 'BATTLE_COMPLETED',
            'result': {
                'winnerName': 'charmander',
                'wonByMargin': '10'
            }
        }
        
        # Test the battle status API
        response = self.flask_app.battle_status('some-battle-id')
        expected_response = {
            'status': 'BATTLE_COMPLETED',
            'result': {
                'winnerName': 'charmander',
                'wonByMargin': '10'
            }
        }
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()
