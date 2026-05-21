from chshgame import classical_strategy, estimate_win_rate, play_game, winning_condition


def test_winning_condition_matches_chsh_rule():
    assert winning_condition(0, 0, 0, 0)
    assert winning_condition(0, 1, 1, 1)
    assert winning_condition(1, 0, 1, 1)
    assert winning_condition(1, 1, 0, 1)
    assert not winning_condition(1, 1, 0, 0)


def test_classical_strategy_has_expected_exact_win_rate_for_all_inputs():
    wins = [
        winning_condition(x, y, *classical_strategy(x, y))
        for x in (0, 1)
        for y in (0, 1)
    ]

    assert sum(wins) / len(wins) == 0.75


def test_estimate_win_rate_uses_seeded_randomness():
    def always_zero_strategy(x, y):
        return 0, 0

    first_run = estimate_win_rate(always_zero_strategy, games=20, seed=1)
    second_run = estimate_win_rate(always_zero_strategy, games=20, seed=1)

    assert first_run == second_run


def test_play_game_returns_binary_score():
    assert play_game(classical_strategy) in (0, 1)
