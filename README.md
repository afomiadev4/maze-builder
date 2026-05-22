# Pathfinder Studio: Maze Builder & Solver

An interactive, real-time visualization tool built with Pygame that demonstrates maze generation and pathfinding algorithms over a customized grid system.

---

## 🚀 Features

### 1. Interactive Customization UI
* **Dynamic Grid Sizing:** Modify rows and columns dynamically between $5 \times 5$ and $50 \times 50$ directly from the visual panel.
* **Real-time Speed Adjustments:** Drag a custom configuration slider to scale animation delays from 0ms up to 500ms per algorithmic step.
* **Flexible Execution Modes:** Switch between automated continuous visualization and a manual **Step-by-Step Mode** using simple interactive controls.
* **Manual Endpoint Placement:** Directly left-click on the canvas grid to place your starting position (🐁) and destination point (🧀).

### 2. Generation Algorithms
* **DFS (Stack-based):** Generates winding, deeply tortuous mazes with fewer branching intersections and long corridors.
* **BFS (Queue-based):** Generates radial, uniformly spreading layouts across the canvas grid.
* **Challenge Mode:** An optional setting that injects cyclic pathways by randomly breaking down additional walls during generation, creating imperfect mazes with loops.

### 3. Traversal and Solving Systems
* **Backtracking (DFS solver):** Explores corridors and systematically marks dead ends visually, tracking its execution pathway dynamically.
* **Wall Follower:** Employs a right-hand rule priority framework (`Right ➔ Straight ➔ Left ➔ Back`) to hug maze boundaries until it encounters the exit.

---

## 🛠️ Project Architecture

The workspace is organized into modular Python modules following clear object-oriented guidelines:

* **`main.py`** – The application coordinator managing the primary visualization update loop, Pygame input event parsing, asset scaling, and the rendering cascade.
* **`maze.py`** – Maintains structural matrix data handling for cell parameters, tracking active walls, and exposing validation wrappers to algorithms.
* **`generators.py`** – Implements the underlying yielding generator functions for DFS and BFS layout builders.
* **`solvers.py`** – Houses pathfinding execution generators providing incremental frame states back to the application loop.
* **`ui.py`** – Defines layout widgets such as abstract elements, buttons, drop-down menus, checkboxes, numeric boxes, and sliders.
* **`config.py`** – Declares layout configurations, interface dimensions, frame rate upper boundaries, and a unified dark theme color scheme palette.

---

## 🎨 Under-the-Hood Data Structures

To prevent rendering redundancy, the layout eliminates standard four-sided cell mapping. Instead, each individual grid element tracks only its **North** and **East** wall configurations. 
* An intact wall is denoted as `1`, whereas an empty pathway is denoted as `0`.
* An extra row at the upper boundary acts as a bounding anchor to close off the grid safely.

---

## 💻 How to Run the Project

### Prerequisites
Make sure you have Python 3 and the Pygame library installed on your computer. If you don't have Pygame, install it via your terminal/command prompt:

```bash
pip install pygame