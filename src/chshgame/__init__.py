"""Utilities for simulating the CHSH game with classical and quantum strategies."""

from .game import (
    build_chsh_circuit,
    classical_strategy,
    estimate_win_rate,
    play_game,
    quantum_strategy,
    winning_condition,
)

__all__ = [
    "build_chsh_circuit",
    "classical_strategy",
    "estimate_win_rate",
    "play_game",
    "quantum_strategy",
    "winning_condition",
]
