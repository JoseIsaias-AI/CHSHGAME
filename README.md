# CHSH Game

This repository contains a compact Python/Qiskit implementation of the CHSH
game, comparing a deterministic classical strategy with the standard entangled
quantum strategy.

The CHSH game is a two-player nonlocal game. Alice and Bob receive random bits
`x` and `y`, answer with bits `a` and `b`, and win when:

```text
a XOR b = x AND y
```

A classical deterministic strategy can win at most 75% of the time. With a
shared entangled state and the right measurements, the quantum strategy wins
with probability close to 85.4%.

## Repository Layout

```text
.
|-- examples/
|   `-- run_chsh_game.py        # Command-line simulation
|-- notebooks/
|   `-- chsh-game.ipynb         # Exploratory notebook
|-- src/
|   `-- chshgame/
|       |-- __init__.py
|       `-- game.py             # Core CHSH logic and Qiskit circuit
|-- tests/
|   `-- test_game.py
|-- pyproject.toml
|-- requirements.txt
`-- README.md
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project:

```bash
pip install -e ".[dev]"
```

## Run the Simulation

```bash
python examples/run_chsh_game.py
```

Expected output will be similar to:

```text
Classical strategy win rate: 0.750
Quantum strategy win rate:   0.850
```

The exact quantum value may vary slightly because the simulation samples one
measurement per game.

## Run Tests

```bash
pytest
```

## Notebook

Open the notebook for a step-by-step exploration:

```bash
jupyter notebook notebooks/chsh-game.ipynb
```

The notebook mirrors the code in `src/chshgame/game.py` and includes circuit
drawings for each input pair.
