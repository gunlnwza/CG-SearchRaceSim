# CG-SearchRaceSim

A local simulator and agent framework for **Search Race**, a Codingame optimization problem where we must program a racing car to drive through checkpoints as fast as possible

### What this repository contains
- A lightweight physics simulator
- A clean environment / agent separation
- A heuristic-based racing agent
- Batch evaluation across multiple tracks (provided by the original problem)
- Optional visualization via `pygame`

### Why this repo exists

This project was built to:
- Experiment with agent design and control heuristics
- Recreate a CodinGame-style judge locally
- Enable fast iteration with visualization + metrics
- Serve as a clean reference for simulation-based problems

## Running

```bash
# run a simulator on all tests
python3 test_all.py

# run a visualizer on a test
python3 visualize.py [-h] [-s] [test]
```

## Goal

Given the car’s initial state, the car must drive through `N` checkpoints in order, repeating the sequence for `L` laps, while minimizing the total number of turns.

### Test Input Format

```
x y vx vy angle
N L
x_1 y_1
x_2 y_2
...
x_n y_n
```

### Description
- `(x, y)` — car position
- `(vx, vy)` — car velocity
- `angle` — car facing angle (degrees)
- `N` — number of checkpoints
- `L` — number of laps
- `(x_i, y_i)` — checkpoint positions

A checkpoint is considered reached when the car enters its radius.

## Notes

This is not a perfect solver — it is a deliberately simple, readable, and extensible baseline meant for experimentation and iteration.
