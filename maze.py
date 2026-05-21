from enum import Enum
from generators import generate_dfs, generate_bfs
from solvers import solve_backtracking, solve_wall_follower

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.north_wall = [[1 for _ in range(cols)] for _ in range(rows + 1)]
        self.east_wall = [[1 for _ in range(cols + 1)] for _ in range(rows)]
        self.visited = [[0 for _ in range(cols)] for _ in range(rows)]
        self.start_cell = (0, 0)
        self.end_cell = (rows - 1, cols - 1)

    def reset_visited(self):
        self.visited = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_unvisited_neighbors(self, r, c):
        neighbors = []
        if r > 0 and self.visited[r - 1][c] == 0:
            neighbors.append((r - 1, c, Direction.NORTH))
        if r < self.rows - 1 and self.visited[r + 1][c] == 0:
            neighbors.append((r + 1, c, Direction.SOUTH))
        if c > 0 and self.visited[r][c - 1] == 0:
            neighbors.append((r, c - 1, Direction.WEST))
        if c < self.cols - 1 and self.visited[r][c + 1] == 0:
            neighbors.append((r, c + 1, Direction.EAST))
        return neighbors

    def remove_wall(self, r, c, direction):
        if direction == Direction.NORTH:
            self.north_wall[r][c] = 0
        elif direction == Direction.SOUTH:
            self.north_wall[r + 1][c] = 0
        elif direction == Direction.WEST:
            self.east_wall[r][c] = 0
        elif direction == Direction.EAST:
            self.east_wall[r][c + 1] = 0

    def get_valid_moves(self, r, c):
        moves = []
        if r > 0 and self.north_wall[r][c] == 0:
            moves.append((r - 1, c, Direction.NORTH))
        if r < self.rows - 1 and self.north_wall[r + 1][c] == 0:
            moves.append((r + 1, c, Direction.SOUTH))
        if c > 0 and self.east_wall[r][c] == 0:
            moves.append((r, c - 1, Direction.WEST))
        if c < self.cols - 1 and self.east_wall[r][c + 1] == 0:
            moves.append((r, c + 1, Direction.EAST))
        return moves

    def generate_dfs(self, challenge_mode=False):
        return generate_dfs(self, challenge_mode)

    def generate_bfs(self, challenge_mode=False):
        return generate_bfs(self, challenge_mode)
        
    def solve_backtracking(self):
        return solve_backtracking(self)

    def solve_wall_follower(self):
        return solve_wall_follower(self)
