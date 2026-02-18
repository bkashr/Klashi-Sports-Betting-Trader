import unittest

from src.models.soccer_poisson import fair_over_probability


class SoccerPoissonTests(unittest.TestCase):
    def test_fair_over_probability_range(self) -> None:
        p = fair_over_probability(2.5, current_goals=1, t_remaining_min=45, pregame_total=2.6)
        self.assertGreaterEqual(p, 0)
        self.assertLessEqual(p, 1)


if __name__ == "__main__":
    unittest.main()
