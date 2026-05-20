# maze-builder
# Building and Running Mazes (Python implementation)

## Project Architecture
- `main.py`: Core application entry and visualization loop.
- `maze.py`: Grid data structures handling `north_wall` and `east_wall` configurations.
- `generator.py`: DFS Stack-based algorithm for maze generation.
- `solver.py`: Backtracking algorithm for pathfinding.

## Core Data Structure
The maze is represented cleanly using only North and East walls for each cell to eliminate redundancy. 
- A value of `1` represents an intact wall.
- A value of `0` represents a broken/eaten pathway.
- **Phantom Row Logic**: Row 0 represents a phantom row below the maze, where its north walls make up the bottom edge.
- **Left Edge Logic**: A specific boundary tracking array handles leftmost edge wall configurations.