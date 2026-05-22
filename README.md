# Pathfinder Studio: Interactive Maze Builder & Solver

An interactive, real-time visualization tool built with Pygame that demonstrates advanced maze generation and pathfinding (solving) algorithms over a customized grid coordinate system.

---

## 🛠️ Implementation Logic & Algorithm Breakdown

This project utilizes Python's memory-efficient **generator functions (`yield`)** to decouple the algorithmic calculation steps from Pygame's rendering frame rate. Instead of calculating a maze instantly, each step yields data frames back to the main loop, allowing smooth, real-time visualization animations.

### 1. Generation Systems (`generators.py`)
* **Depth-First Search (DFS / Stack-Based):** Chooses a random starting cell and utilizes a stack array to keep track of its historical path. It aggressively carves deep corridors by choosing random unvisited neighbors until hitting a dead end, where it pops elements off the stack to backtrack. This results in highly winding mazes with long corridors.
* **Breadth-First Search (BFS / Queue-Based):** Operates via a first-in, first-out queue mechanism. It expands systematically outwards from its starting hub, creating broader, more concentric and radially expanding pathways across the canvas layout.
* **Challenge Mode Implementation:** To add complexity, we implemented a custom flag that injects cyclic loops into our perfect mazes. During generation, it checks a random float boundary ($< 5\%$ probability); if triggered, it intentionally breaks down an adjacent wall, giving users multiple paths to the exit.

### 2. Solving Systems (`solvers.py`)
* **Backtracking Solver:** Re-initializes a stack tracking array starting from the designated user coordinates. As it searches for the end cell, it visually markers dead-ends with a distinct code identifier (`2`), telling the rendering engine to paint them as explored but incorrect routes.
* **Wall Follower (Right-Hand Rule):** Simulates a physical traversal strategy by prioritizing movement directions in a fixed rotational order relative to current heading direction indices: `Right ➔ Straight ➔ Left ➔ Backward`. It handles complex collision conditions across our distinct North and East coordinate walls to track continuous loops.

---

## 🎨 Architectural Design Choices

To keep this project highly performance-optimized and lightweight, we made critical structural decisions:

### Minimalist Wall Structure
Standard grids track 4 independent walls per cell, creating double redundancy (e.g., Cell A's East wall is Cell B's West wall). We eliminated this entirely. Each coordinate only stores a **North** and an **East** wall array. 
* **0** indicates an open path, and **1** indicates a solid wall.
* To prevent index errors at boundaries, we engineered a dedicated **Phantom Row** at index `rows` to naturally seal the bottom grid margins without extra layout objects.

### Custom-Built UI Architecture (`ui.py`)
Instead of bloated external layout libraries, we built lightweight object-oriented widgets from scratch using basic Pygame surfaces:
* **`UIElement` Framework:** The abstract baseline class tracking mouse hover intersections (`self.hovered`) and bounding rect collision layouts.
* **`Slider` Component:** Normalizes mouse coordinates dynamically relative to the screen offset to calculate value ratios on a scale (0ms–500ms for speed delay control).
* **`InputNumber` Box & `Dropdown` Selection:** Captures direct user input and tracks expanded visibility toggles for runtime parameter adaptation.

---

## ⚠️ Challenges Faced & Solutions Engineered

### 1. The Challenge: Decoupling Computations from Frame Rendering Upper Boundaries
* **The Problem:** Standard loops freeze the entire display canvas during heavy recursive calculation loops, preventing step-by-step canvas visualization.
* **The Solution:** We migrated all logic inside `generators.py` and `solvers.py` to use Python state generators (`yield`). `main.py` can now process a single algorithmic calculation step per game clock tick while keeping the GUI responsive to user window resize updates or dragging actions.

### 2. The Challenge: Infinite Loops in Wall Follower Tracking
* **The Problem:** On cyclic layouts (Challenge Mode), the wall follower algorithm could easily get trapped running in an infinite circular corridor loop.
* **The Solution:** We implemented an upper boundary calculation matrix framework (`max_steps = rows * cols * 10`). If execution steps cross this cap threshold, the state machine yields a `"loop"` event type, updating the interface status banner safely instead of crashing the system application thread.

---

## 💻 Technical Setup & Project Architecture

* `config.py` – Global colors palette scheme and dimensional aspect parameters.
* `ui.py` – Structural blueprint objects for interactive sliders, buttons, and text fields.
* `maze.py` – The coordinate grid matrix maps holding structural configurations.
* `main.py` – The core executable engine coordinating rendering cycles and user input events.

### Execution
Ensure you have Pygame installed, and launch the primary runner module:
```bash
pip install pygame
python main.py