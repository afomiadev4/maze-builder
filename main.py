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

        def setup_ui(self):
        self.elements = []
        sx, sy = CONTENT_OFFSET_X + self.canvas_size + 40, 140
        
        # Grid dimensions inputs
        self.elements.append(InputNumber(sx + 100, sy + 60, 60, 32, self.rows, "rows"))
        self.elements.append(Button(sx + 175, sy + 60, 32, 32, "-", "rows_dec", "surface_hover"))
        self.elements.append(Button(sx + 215, sy + 60, 32, 32, "+", "rows_inc", "surface_hover"))
        
        self.elements.append(InputNumber(sx + 100, sy + 110, 60, 32, self.cols, "cols"))
        self.elements.append(Button(sx + 175, sy + 110, 32, 32, "-", "cols_dec", "surface_hover"))
        self.elements.append(Button(sx + 215, sy + 110, 32, 32, "+", "cols_inc", "surface_hover"))
        
        # Algorithm selection
        self.drop_gen = Dropdown(sx + 20, sy + 180, 260, 38, ["DFS (Stack) - Tortuous", "BFS (Queue) - Spreading"], 0, "gen_drop")
        self.drop_solve = Dropdown(sx + 20, sy + 250, 260, 38, ["Backtracking (Stack)", "Shoulder-to-Wall"], 0, "solve_drop")
        self.elements.append(self.drop_gen)
        self.elements.append(self.drop_solve)
        
        # Animation & Mode options
        self.elements.append(Slider(sx + 20, sy + 325, 260, 8, 0, 500, self.speed, "Animation Delay", "speed_slider"))
        self.elements.append(Checkbox(sx + 20, sy + 365, "Challenge Mode (Cycles)", "challenge", self.challenge_mode))
        self.elements.append(Checkbox(sx + 20, sy + 415, "Step-by-Step Mode", "step_mode", self.step_mode))
        
        # Action Triggers
        self.btn_next = Button(sx + 20, sy + 465, 260, 45, "Next Step", "next_step", "secondary", enabled=False)
        self.btn_generate = Button(sx + 20, sy + 525, 260, 45, "Generate Maze", "generate", "primary")
        self.btn_solve = Button(sx + 20, sy + 585, 260, 45, "Solve Maze", "solve", "primary", enabled=True)
        self.elements.append(self.btn_next)
        self.elements.append(self.btn_generate)
        self.elements.append(self.btn_solve)

    def draw_rounded_panel(self, rect, title=""):
        pygame.draw.rect(self.virtual_screen, (0, 0, 0, 120), rect.move(0, 4), border_radius=16)
        pygame.draw.rect(self.virtual_screen, COLOR_SURFACE, rect, border_radius=16)
        pygame.draw.rect(self.virtual_screen, COLOR_BORDER, rect, 1, border_radius=16)
        if title:
            surf = self.font_h2.render(title, True, COLOR_TEXT)
            self.virtual_screen.blit(surf, (rect.x + 20, rect.y + 15))
            pygame.draw.line(self.virtual_screen, COLOR_BORDER, (rect.x + 20, rect.y + 45), (rect.right - 20, rect.y + 45), 1)