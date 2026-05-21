"""Core logic for the CHSH game.

The CHSH game is a two-player nonlocal game involving Alice and Bob. They each
receive one random bit, cannot communicate after receiving it, and must return
one bit each. They win when ``a XOR b == x AND y``.
"""

from __future__ import annotations

from math import pi
from random import Random
from typing import Any, Callable, Protocol


Bit = int | str
Strategy = Callable[[int, int], tuple[Bit, Bit]]
_DEFAULT_SIMULATOR: Any | None = None


class QuantumBackend(Protocol):
    """Minimal backend protocol used by the quantum strategy."""

    def run(self, circuit: Any, shots: int = 1): ...


def _as_bit(value: Bit) -> int:
    bit = int(value)
    if bit not in (0, 1):
        raise ValueError(f"Expected a bit value, got {value!r}.")
    return bit


def winning_condition(x: Bit, y: Bit, a: Bit, b: Bit) -> bool:
    """Return whether the answers win the CHSH game."""

    x_bit = _as_bit(x)
    y_bit = _as_bit(y)
    a_bit = _as_bit(a)
    b_bit = _as_bit(b)
    return (a_bit ^ b_bit) == (x_bit & y_bit)


def play_game(strategy: Strategy, rng: Random | None = None) -> int:
    """Play one CHSH round and return 1 for a win or 0 for a loss."""

    random_source = rng or Random()
    x = random_source.randint(0, 1)
    y = random_source.randint(0, 1)
    a, b = strategy(x, y)
    return int(winning_condition(x, y, a, b))


def estimate_win_rate(
    strategy: Strategy,
    games: int = 1000,
    seed: int | None = None,
) -> float:
    """Estimate a strategy's win rate over many independent CHSH rounds."""

    if games <= 0:
        raise ValueError("games must be a positive integer.")

    rng = Random(seed)
    score = sum(play_game(strategy, rng) for _ in range(games))
    return score / games


def build_chsh_circuit(x: Bit, y: Bit) -> Any:
    """Build the quantum circuit for a CHSH round with inputs ``x`` and ``y``."""

    from qiskit import QuantumCircuit

    x_bit = _as_bit(x)
    y_bit = _as_bit(y)

    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.barrier()

    if x_bit == 1:
        circuit.ry(-pi / 2, 0)
    circuit.measure(0, 0)

    if y_bit == 0:
        circuit.ry(-pi / 4, 1)
    else:
        circuit.ry(pi / 4, 1)
    circuit.measure(1, 1)

    return circuit


def quantum_strategy(
    x: Bit,
    y: Bit,
    backend: QuantumBackend | None = None,
) -> tuple[int, int]:
    """Run the quantum CHSH strategy once and return Alice and Bob's answers."""

    global _DEFAULT_SIMULATOR

    if backend is None and _DEFAULT_SIMULATOR is None:
        from qiskit_aer import AerSimulator

        _DEFAULT_SIMULATOR = AerSimulator()

    simulator = backend or _DEFAULT_SIMULATOR
    result = simulator.run(build_chsh_circuit(x, y), shots=1).result()
    counts = result.get_counts()
    measured_bits = next(iter(counts))

    # Qiskit returns classical bits as a string. With the circuit above, the
    # first character is Bob's bit and the second character is Alice's bit.
    bob, alice = (int(bit) for bit in measured_bits)
    return alice, bob


def classical_strategy(x: Bit, y: Bit) -> tuple[int, int]:
    """A simple deterministic classical strategy for comparison."""

    return _as_bit(x), 1 - _as_bit(y)
