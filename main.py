import pygame
import sys
from config import *
from ui import Button, Dropdown, Slider, InputNumber, Checkbox
from maze import Maze

class MazeApp:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.win_w = min(VIRTUAL_WIDTH, info.current_w - 50)
        self.win_h = min(900, info.current_h - 100)
        self.screen = pygame.display.set_mode((self.win_w, self.win_h), pygame.RESIZABLE)
        pygame.display.set_caption("Pathfinder Studio")
        self.virtual_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        self.clock = pygame.time.Clock()
        self.scroll_y = 0
        
        # Typography configuration
        self.font_h1 = pygame.font.SysFont("Arial", 42, bold=True)
        self.font_h2 = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_label = pygame.font.SysFont("Arial", 14, bold=True)
        self.font_ui = pygame.font.SysFont("Arial", 16)
        self.font_stat_val = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_mono = pygame.font.SysFont("Courier New", 14)
        self.font_emoji = pygame.font.SysFont("notocoloremoji", 32)
        
        # State variables
        self.rows, self.cols = 20, 20
        self.gen_type, self.solver_type = "dfs", "backtrack"
        self.challenge_mode, self.step_mode = False, False
        self.speed = 250
        self.maze = Maze(self.rows, self.cols)
        self.is_animating = False
        self.current_algo, self.algo_state = None, None
        self.status_text = "Ready"
        self.stats = {"path": 0, "visited": 0, "backtracks": 0}
        
        # Layout metrics
        self.sidebar_width, self.padding, self.canvas_size = 300, 30, 640
        self.elements = []
        self.setup_ui()
        self.calculate_grid()

    def calculate_grid(self):
        self.cell_size = min(self.canvas_size / self.cols, self.canvas_size / self.rows)
        mx, my = CONTENT_OFFSET_X, 140
        self.x_offset = mx + 10 + (self.canvas_size - (self.cols * self.cell_size)) / 2
        self.y_offset = my + 10 + (self.canvas_size - (self.rows * self.cell_size)) / 2