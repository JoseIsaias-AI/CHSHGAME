"""Run a small CHSH game simulation from the command line."""

from chshgame import classical_strategy, estimate_win_rate, quantum_strategy


def main() -> None:
    games = 1000
    classical_rate = estimate_win_rate(classical_strategy, games=games, seed=7)
    quantum_rate = estimate_win_rate(quantum_strategy, games=games, seed=7)

    print(f"Classical strategy win rate: {classical_rate:.3f}")
    print(f"Quantum strategy win rate:   {quantum_rate:.3f}")


if __name__ == "__main__":
    main()
