import unittest
from classes.score_manager import ScoreManager
from util.constants import (
    ASTEROID_MIN_RADIUS,
    ASTEROID_MAX_RADIUS,
    SCORE_SMALL_ASTEROID,
    SCORE_MEDIUM_ASTEROID,
    SCORE_LARGE_ASTEROID,
    COMBO_WINDOW_SECONDS,
    SCORE_MAX
)


class TestScoreManagerInitialization(unittest.TestCase):
    
    def test_initialization_sets_score_to_zero(self):
        manager = ScoreManager()
        self.assertEqual(manager.get_current_score(), 0)
    
    def test_initialization_sets_combo_multiplier_to_one(self):
        manager = ScoreManager()
        self.assertEqual(manager.get_combo_multiplier(), 1)
    
    def test_initialization_sets_combo_timer_to_zero(self):
        manager = ScoreManager()
        self.assertEqual(manager._ScoreManager__combo_timer, 0.0)


class TestScoreCalculation(unittest.TestCase):
    
    def setUp(self):
        self.manager = ScoreManager()
    
    def test_calculate_base_points_for_small_asteroid(self):
        points = self.manager._calculate_base_points(ASTEROID_MIN_RADIUS)
        self.assertEqual(points, SCORE_SMALL_ASTEROID)
    
    def test_calculate_base_points_for_medium_asteroid(self):
        points = self.manager._calculate_base_points(ASTEROID_MIN_RADIUS * 2)
        self.assertEqual(points, SCORE_MEDIUM_ASTEROID)
    
    def test_calculate_base_points_for_large_asteroid(self):
        points = self.manager._calculate_base_points(ASTEROID_MAX_RADIUS)
        self.assertEqual(points, SCORE_LARGE_ASTEROID)
    
    def test_calculate_base_points_for_unknown_radius_returns_medium(self):
        points = self.manager._calculate_base_points(35)
        self.assertEqual(points, SCORE_MEDIUM_ASTEROID)


class TestAddScore(unittest.TestCase):
    
    def setUp(self):
        self.manager = ScoreManager()
    
    def test_add_score_small_asteroid_with_1x_multiplier(self):
        self.manager.add_score(ASTEROID_MIN_RADIUS)
        self.assertEqual(self.manager.get_current_score(), SCORE_SMALL_ASTEROID)
    
    def test_add_score_medium_asteroid_with_1x_multiplier(self):
        self.manager.add_score(ASTEROID_MIN_RADIUS * 2)
        self.assertEqual(self.manager.get_current_score(), SCORE_MEDIUM_ASTEROID)
    
    def test_add_score_large_asteroid_with_1x_multiplier(self):
        self.manager.add_score(ASTEROID_MAX_RADIUS)
        self.assertEqual(self.manager.get_current_score(), SCORE_LARGE_ASTEROID)
    
    def test_add_score_accumulates_over_multiple_hits(self):
        self.manager.add_score(ASTEROID_MIN_RADIUS)
        self.manager.add_score(ASTEROID_MIN_RADIUS)
        self.manager.add_score(ASTEROID_MIN_RADIUS)
        expected = SCORE_SMALL_ASTEROID * (1 + 2 + 3)
        self.assertEqual(self.manager.get_current_score(), expected)
    
    def test_add_score_with_2x_combo_multiplier(self):
        self.manager._ScoreManager__combo_multiplier = 2
        self.manager.add_score(ASTEROID_MIN_RADIUS)
        expected = SCORE_SMALL_ASTEROID * 2
        self.assertEqual(self.manager.get_current_score(), expected)
    
    def test_add_score_with_3x_combo_multiplier(self):
        self.manager._ScoreManager__combo_multiplier = 3
        self.manager.add_score(ASTEROID_MIN_RADIUS)
        expected = SCORE_SMALL_ASTEROID * 3
        self.assertEqual(self.manager.get_current_score(), expected)
    
    def test_add_score_large_asteroid_with_5x_multiplier(self):
        self.manager._ScoreManager__combo_multiplier = 5
        self.manager.add_score(ASTEROID_MAX_RADIUS)
        expected = SCORE_LARGE_ASTEROID * 5
        self.assertEqual(self.manager.get_current_score(), expected)
    
    def test_add_score_mixed_asteroids_and_multipliers(self):
        self.manager.add_score(ASTEROID_MIN_RADIUS)
        self.manager._ScoreManager__combo_multiplier = 2
        self.manager.add_score(ASTEROID_MIN_RADIUS * 2)
        expected = SCORE_SMALL_ASTEROID + (SCORE_MEDIUM_ASTEROID * 2)
        self.assertEqual(self.manager.get_current_score(), expected)


class TestComboSystem(unittest.TestCase):
    
    def setUp(self):
        self.manager = ScoreManager()
    
    def test_update_combo_increases_multiplier_by_one(self):
        initial = self.manager.get_combo_multiplier()
        self.manager._update_combo()
        self.assertEqual(self.manager.get_combo_multiplier(), initial + 1)
    
    def test_update_combo_multiple_times(self):
        self.manager._update_combo()
        self.manager._update_combo()
        self.manager._update_combo()
        self.assertEqual(self.manager.get_combo_multiplier(), 4)
    
    def test_reset_combo_sets_multiplier_to_one(self):
        self.manager._ScoreManager__combo_multiplier = 5
        self.manager._reset_combo()
        self.assertEqual(self.manager.get_combo_multiplier(), 1)


class TestTimerUpdate(unittest.TestCase):
    
    def setUp(self):
        self.manager = ScoreManager()
    
    def test_update_decrements_timer_by_dt(self):
        self.manager._ScoreManager__combo_timer = 2.0
        self.manager.update(0.5)
        self.assertEqual(self.manager._ScoreManager__combo_timer, 1.5)
    
    def test_update_with_multiple_small_dt_values(self):
        self.manager._ScoreManager__combo_timer = 1.0
        self.manager.update(0.1)
        self.manager.update(0.2)
        self.manager.update(0.3)
        self.assertAlmostEqual(self.manager._ScoreManager__combo_timer, 0.4, places=5)
    
    def test_update_timer_reaches_zero(self):
        self.manager._ScoreManager__combo_timer = 0.5
        self.manager.update(0.5)
        self.assertEqual(self.manager._ScoreManager__combo_timer, 0.0)
    
    def test_update_timer_does_not_go_negative(self):
        self.manager._ScoreManager__combo_timer = 0.3
        self.manager.update(0.5)
        self.assertEqual(self.manager._ScoreManager__combo_timer, 0.0)
    
    def test_update_resets_combo_when_timer_expires(self):
        self.manager._ScoreManager__combo_multiplier = 5
        self.manager._ScoreManager__combo_timer = 0.5
        self.manager.update(1.0)
        self.assertEqual(self.manager.get_combo_multiplier(), 1)
    
    def test_update_maintains_combo_when_timer_is_positive(self):
        self.manager._ScoreManager__combo_multiplier = 3
        self.manager._ScoreManager__combo_timer = 1.0
        self.manager.update(0.5)
        self.assertEqual(self.manager.get_combo_multiplier(), 3)
    
    def test_update_with_zero_dt(self):
        self.manager._ScoreManager__combo_timer = 1.0
        self.manager.update(0.0)
        self.assertEqual(self.manager._ScoreManager__combo_timer, 1.0)
    
    def test_update_exactly_at_combo_window_boundary(self):
        self.manager._ScoreManager__combo_multiplier = 3
        self.manager._ScoreManager__combo_timer = COMBO_WINDOW_SECONDS
        self.manager.update(COMBO_WINDOW_SECONDS)
        self.assertEqual(self.manager._ScoreManager__combo_timer, 0.0)
        self.assertEqual(self.manager.get_combo_multiplier(), 3)
    
    def test_update_past_combo_window_resets_combo(self):
        self.manager._ScoreManager__combo_multiplier = 3
        self.manager._ScoreManager__combo_timer = COMBO_WINDOW_SECONDS
        self.manager.update(COMBO_WINDOW_SECONDS + 0.01)
        self.assertEqual(self.manager.get_combo_multiplier(), 1)


class TestReset(unittest.TestCase):
    
    def test_reset_clears_score(self):
        manager = ScoreManager()
        manager.add_score(ASTEROID_MAX_RADIUS)
        manager.reset()
        self.assertEqual(manager.get_current_score(), 0)
    
    def test_reset_clears_combo_multiplier(self):
        manager = ScoreManager()
        manager._ScoreManager__combo_multiplier = 5
        manager.reset()
        self.assertEqual(manager.get_combo_multiplier(), 1)
    
    def test_reset_clears_combo_timer(self):
        manager = ScoreManager()
        manager._ScoreManager__combo_timer = 1.5
        manager.reset()
        self.assertEqual(manager._ScoreManager__combo_timer, 0.0)
    
    def test_reset_restores_initial_state(self):
        manager = ScoreManager()
        manager.add_score(ASTEROID_MAX_RADIUS)
        manager._ScoreManager__combo_multiplier = 7
        manager._ScoreManager__combo_timer = 1.8
        manager.reset()
        self.assertEqual(manager.get_current_score(), 0)
        self.assertEqual(manager.get_combo_multiplier(), 1)
        self.assertEqual(manager._ScoreManager__combo_timer, 0.0)


class TestGetters(unittest.TestCase):
    
    def test_get_current_score_returns_zero_initially(self):
        manager = ScoreManager()
        self.assertEqual(manager.get_current_score(), 0)
    
    def test_get_current_score_returns_correct_value_after_scoring(self):
        manager = ScoreManager()
        manager.add_score(ASTEROID_MIN_RADIUS)
        manager.add_score(ASTEROID_MIN_RADIUS * 2)
        expected = SCORE_SMALL_ASTEROID * 1 + SCORE_MEDIUM_ASTEROID * 2
        self.assertEqual(manager.get_current_score(), expected)
    
    def test_get_combo_multiplier_returns_one_initially(self):
        manager = ScoreManager()
        self.assertEqual(manager.get_combo_multiplier(), 1)
    
    def test_get_combo_multiplier_returns_updated_value(self):
        manager = ScoreManager()
        manager._update_combo()
        manager._update_combo()
        self.assertEqual(manager.get_combo_multiplier(), 3)


class TestEdgeCases(unittest.TestCase):
    
    def test_large_score_accumulation(self):
        manager = ScoreManager()
        for _ in range(100):
            manager.add_score(ASTEROID_MAX_RADIUS)
        expected = SCORE_MAX
        self.assertEqual(manager.get_current_score(), expected)
    
    def test_high_combo_multiplier(self):
        manager = ScoreManager()
        for _ in range(20):
            manager._update_combo()
        self.assertEqual(manager.get_combo_multiplier(), 21)
    
    def test_score_with_very_high_multiplier(self):
        manager = ScoreManager()
        manager._ScoreManager__combo_multiplier = 10
        manager.add_score(ASTEROID_MAX_RADIUS)
        expected = SCORE_LARGE_ASTEROID * 10
        self.assertEqual(manager.get_current_score(), expected)
    
    def test_rapid_updates_with_small_dt(self):
        manager = ScoreManager()
        manager._ScoreManager__combo_timer = 1.0
        for _ in range(100):
            manager.update(0.01)
        self.assertEqual(manager._ScoreManager__combo_timer, 0.0)
    
    def test_timer_with_large_dt_value(self):
        manager = ScoreManager()
        manager._ScoreManager__combo_timer = 1.0
        manager.update(10.0)
        self.assertEqual(manager._ScoreManager__combo_timer, 0.0)
    
    def test_multiple_resets(self):
        manager = ScoreManager()
        manager.add_score(ASTEROID_MAX_RADIUS)
        manager.reset()
        manager.add_score(ASTEROID_MIN_RADIUS)
        manager.reset()
        self.assertEqual(manager.get_current_score(), 0)
        self.assertEqual(manager.get_combo_multiplier(), 1)
    
    def test_score_capped_at_score_max(self):
        manager = ScoreManager()
        manager._ScoreManager__current_score = SCORE_MAX - 100
        manager._ScoreManager__combo_multiplier = 10
        manager.add_score(ASTEROID_MAX_RADIUS)
        self.assertEqual(manager.get_current_score(), SCORE_MAX)


class TestStateManagement(unittest.TestCase):
    
    def test_score_persists_across_combo_changes(self):
        manager = ScoreManager()
        manager.add_score(ASTEROID_MIN_RADIUS)
        initial_score = manager.get_current_score()
        manager._update_combo()
        self.assertEqual(manager.get_current_score(), initial_score)
    
    def test_combo_persists_across_score_changes(self):
        manager = ScoreManager()
        manager._ScoreManager__combo_multiplier = 3
        manager.add_score(ASTEROID_MIN_RADIUS)
        self.assertEqual(manager.get_combo_multiplier(), 4)
    
    def test_timer_independent_of_score(self):
        manager = ScoreManager()
        manager._ScoreManager__combo_timer = 1.5
        manager.add_score(ASTEROID_MAX_RADIUS)
        self.assertEqual(manager._ScoreManager__combo_timer, COMBO_WINDOW_SECONDS)
    
    def test_state_isolation_between_instances(self):
        manager1 = ScoreManager()
        manager2 = ScoreManager()
        manager1.add_score(ASTEROID_MAX_RADIUS)
        manager1._ScoreManager__combo_multiplier = 5
        self.assertEqual(manager2.get_current_score(), 0)
        self.assertEqual(manager2.get_combo_multiplier(), 1)


class TestScoreCalculationAccuracy(unittest.TestCase):
    
    def test_score_calculation_with_different_asteroid_sizes(self):
        manager = ScoreManager()
        manager.add_score(ASTEROID_MIN_RADIUS)
        manager.add_score(ASTEROID_MIN_RADIUS * 2)
        manager.add_score(ASTEROID_MAX_RADIUS)
        expected = (
            SCORE_SMALL_ASTEROID * 1
            + SCORE_MEDIUM_ASTEROID * 2
            + SCORE_LARGE_ASTEROID * 3
        )
        self.assertEqual(manager.get_current_score(), expected)
    
    def test_score_calculation_maintains_integer_precision(self):
        manager = ScoreManager()
        manager.add_score(ASTEROID_MIN_RADIUS)
        self.assertIsInstance(manager.get_current_score(), int)
    
    def test_multiplier_applied_correctly_to_each_hit(self):
        manager = ScoreManager()
        manager._ScoreManager__combo_multiplier = 2
        manager.add_score(ASTEROID_MIN_RADIUS)
        score_after_first = manager.get_current_score()
        
        manager._ScoreManager__combo_multiplier = 3
        manager.add_score(ASTEROID_MIN_RADIUS)
        score_after_second = manager.get_current_score()
        
        expected_first = SCORE_SMALL_ASTEROID * 2
        expected_second = expected_first + (SCORE_SMALL_ASTEROID * 3)
        
        self.assertEqual(score_after_first, expected_first)
        self.assertEqual(score_after_second, expected_second)


if __name__ == '__main__':
    unittest.main()
