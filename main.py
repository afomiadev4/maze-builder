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

    def draw_ui(self):
        self.virtual_screen.fill(COLOR_BG)
        t_surf = self.font_h1.render("Pathfinder Studio", True, COLOR_TEXT)
        self.virtual_screen.blit(t_surf, (VIRTUAL_WIDTH//2 - t_surf.get_width()//2, 10))
        p_surf = self.font_ui.render("Interactive algorithmic generation and traversal visualizer.", True, COLOR_TEXT_MUTED)
        self.virtual_screen.blit(p_surf, (VIRTUAL_WIDTH//2 - p_surf.get_width()//2, 85))
        
        sx, sy = CONTENT_OFFSET_X + self.canvas_size + 40, 140
        self.draw_rounded_panel(pygame.Rect(sx, sy, 300, 640), "Configuration")
        self.virtual_screen.blit(self.font_label.render("Rows:", True, COLOR_TEXT_MUTED), (sx + 20, sy + 68))
        self.virtual_screen.blit(self.font_label.render("Columns:", True, COLOR_TEXT_MUTED), (sx + 20, sy + 118))
        self.virtual_screen.blit(self.font_label.render("Generation Algorithm:", True, COLOR_TEXT_MUTED), (sx + 20, sy + 155))
        self.virtual_screen.blit(self.font_label.render("Solver Algorithm:", True, COLOR_TEXT_MUTED), (sx + 20, sy + 225))
        
        mx, my = CONTENT_OFFSET_X, 140
        self.draw_rounded_panel(pygame.Rect(mx, my, self.canvas_size + 20, self.canvas_size + 20))
        pygame.draw.rect(self.virtual_screen, (10, 10, 10), pygame.Rect(mx + 10, my + 10, self.canvas_size, self.canvas_size), border_radius=12)
        sr = pygame.Rect(mx, my + self.canvas_size + 40, self.canvas_size + 20, 100)
        self.draw_rounded_panel(sr)
        
        ls, vs = ["PATH LENGTH", "CELLS VISITED", "BACKTRACKS / TURNS"], [self.stats["path"], self.stats["visited"], self.stats["backtracks"]]
        for i in range(3):
            x = mx + (i + 0.5) * (sr.w / 3)
            self.virtual_screen.blit(self.font_label.render(ls[i], True, COLOR_TEXT_MUTED), (x - 60, sr.y + 25))
            self.virtual_screen.blit(self.font_stat_val.render(str(vs[i]), True, COLOR_PRIMARY), (x - 20, sr.y + 45))
            
        st_rect = pygame.Rect(sx, sy + 660, 300, 55)
        self.draw_rounded_panel(st_rect)
        st_surf = self.font_ui.render(self.status_text, True, COLOR_TEXT)
        self.virtual_screen.blit(st_surf, st_surf.get_rect(center=st_rect.center))

        for el in self.elements:
            if isinstance(el, Button):
                bg = COLOR_PRIMARY if el.style=="primary" else (COLOR_SECONDARY if el.style=="secondary" else (COLOR_SURFACE_HOVER if el.style=="surface_hover" else COLOR_SURFACE))
                if el.hovered and el.enabled: bg = COLOR_PRIMARY_HOVER if el.style=="primary" else (COLOR_SECONDARY_HOVER if el.style=="secondary" else (COLOR_SURFACE_HOVER if el.style=="surface_hover" else COLOR_SURFACE_HOVER))
                if not el.enabled: bg = (bg[0]//3, bg[1]//3, bg[2]//3)
                pygame.draw.rect(self.virtual_screen, bg, el.rect, border_radius=8)
                l_surf = self.font_ui.render(el.label, True, COLOR_TEXT)
                self.virtual_screen.blit(l_surf, l_surf.get_rect(center=el.rect.center))
            elif isinstance(el, Checkbox):
                pygame.draw.rect(self.virtual_screen, COLOR_BG, el.rect, border_radius=4)
                if el.checked: pygame.draw.rect(self.virtual_screen, COLOR_PRIMARY, el.rect.inflate(-8, -8), border_radius=2)
                self.virtual_screen.blit(self.font_ui.render(el.label, True, COLOR_TEXT_MUTED), (el.rect.right+10, el.rect.y+2))
            elif isinstance(el, InputNumber):
                pygame.draw.rect(self.virtual_screen, COLOR_BG, el.rect, border_radius=6)
                s = self.font_ui.render(str(el.val), True, COLOR_TEXT); self.virtual_screen.blit(s, s.get_rect(center=el.rect.center))
            elif isinstance(el, Slider):
                self.virtual_screen.blit(self.font_label.render(f"{el.label} (ms): {int(el.curr_val)}", True, COLOR_TEXT_MUTED), (el.rect.x, el.rect.y-25))
                pygame.draw.rect(self.virtual_screen, COLOR_BORDER, el.rect, border_radius=4)
                hx = el.rect.x + (el.curr_val - el.min_val) / max(1, el.max_val-el.min_val) * el.rect.w
                pygame.draw.circle(self.virtual_screen, COLOR_PRIMARY, (int(hx), el.rect.centery), 10)
            elif isinstance(el, Dropdown):
                pygame.draw.rect(self.virtual_screen, COLOR_SURFACE_HOVER if el.hovered else COLOR_SURFACE, el.rect, border_radius=8)
                pygame.draw.rect(self.virtual_screen, COLOR_BORDER, el.rect, 1, border_radius=8)
                t = self.font_ui.render(el.options[el.curr_idx], True, COLOR_TEXT)
                self.virtual_screen.blit(t, t.get_rect(center=el.rect.center))
                pygame.draw.polygon(self.virtual_screen, COLOR_TEXT_MUTED, [(el.rect.right-20, el.rect.centery-3), (el.rect.right-10, el.rect.centery-3), (el.rect.right-15, el.rect.centery+3)])

        for el in self.elements:
            if isinstance(el, Dropdown) and el.expanded:
                for i, opt in enumerate(el.options):
                    opt_rect = pygame.Rect(el.rect.x, el.rect.bottom + i * 35, el.rect.w, 35)
                    m_pos_adj = (pygame.mouse.get_pos()[0]-max(0,(self.win_w-VIRTUAL_WIDTH)//2), pygame.mouse.get_pos()[1]-self.scroll_y)
                    pygame.draw.rect(self.virtual_screen, COLOR_SURFACE_HOVER if opt_rect.collidepoint(m_pos_adj) else COLOR_SURFACE, opt_rect)
                    pygame.draw.rect(self.virtual_screen, COLOR_BORDER, opt_rect, 1)
                    ot = self.font_ui.render(opt, True, COLOR_TEXT)
                    self.virtual_screen.blit(ot, ot.get_rect(center=opt_rect.center))

    def draw_maze(self):
        if not ("Generating" in self.status_text):
            for r in range(self.maze.rows):
                for c in range(self.maze.cols):
                    val = self.maze.visited[r][c]
                    if val > 0:
                        cx, cy = int(self.x_offset + c * self.cell_size + self.cell_size/2), int(self.y_offset + r * self.cell_size + self.cell_size/2)
                        pygame.draw.circle(self.virtual_screen, COLOR_PATH if val == 1 else COLOR_DEADEND, (cx, cy), int(self.cell_size * 0.35))
        for r in range(self.maze.rows + 1):
            for c in range(self.maze.cols):
                if self.maze.north_wall[r][c] == 1:
                    pygame.draw.line(self.virtual_screen, COLOR_WALL, (self.x_offset + c * self.cell_size, self.y_offset + r * self.cell_size), (self.x_offset + (c + 1) * self.cell_size, self.y_offset + r * self.cell_size), 2)
        for r in range(self.maze.rows):
            for c in range(self.maze.cols + 1):
                if self.maze.east_wall[r][c] == 1:
                    pygame.draw.line(self.virtual_screen, COLOR_WALL, (self.x_offset + c * self.cell_size, self.y_offset + r * self.cell_size), (self.x_offset + c * self.cell_size, self.y_offset + (r + 1) * self.cell_size), 2)
        if self.maze.start_cell: self.draw_emoji(self.maze.start_cell[0], self.maze.start_cell[1], "🐁")
        if self.maze.end_cell: self.draw_emoji(self.maze.end_cell[0], self.maze.end_cell[1], "🧀")

    def draw_emoji(self, r, c, emoji):
        cx, cy = int(self.x_offset + c * self.cell_size + self.cell_size / 2), int(self.y_offset + r * self.cell_size + self.cell_size / 2)
        s = self.font_emoji.render(emoji, True, COLOR_TEXT)
        sz = int(self.cell_size * 0.7)
        if sz > 0: s = pygame.transform.scale(s, (sz, sz))
        self.virtual_screen.blit(s, s.get_rect(center=(cx, cy)))

    def draw_algo_state(self):
        if not self.algo_state: return
        tag, path = self.algo_state[0], (self.algo_state[2] if self.algo_state[0] in ["visit", "backtrack"] else (self.algo_state[1] if self.algo_state[0] == "step" else []))
        for r, c in path:
            cx, cy = int(self.x_offset + c * self.cell_size + self.cell_size / 2), int(self.y_offset + r * self.cell_size + self.cell_size / 2)
            pygame.draw.circle(self.virtual_screen, COLOR_PATH, (cx, cy), int(self.cell_size * 0.25))
        if path:
            r, c = path[-1]
            cx, cy = int(self.x_offset + c * self.cell_size + self.cell_size / 2), int(self.y_offset + r * self.cell_size + self.cell_size / 2)
            pygame.draw.circle(self.virtual_screen, COLOR_GEN_DOT if "Generating" in self.status_text else COLOR_TEXT, (cx, cy), int(self.cell_size * 0.4), 3)
    def handle_event(self, event):
        win_off_x = max(0, (self.win_w - VIRTUAL_WIDTH) // 2)
        pos = list(pygame.mouse.get_pos())
        pos[0] -= win_off_x; pos[1] -= self.scroll_y
        for el in self.elements: el.hovered = el.rect.collidepoint(pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_any = False
            for el in self.elements:
                if isinstance(el, Dropdown) and el.expanded:
                    for i in range(len(el.options)):
                        opt_rect = pygame.Rect(el.rect.x, el.rect.bottom + i * 35, el.rect.w, 35)
                        if opt_rect.collidepoint(pos):
                            el.curr_idx = i; el.expanded = False; clicked_any = True
                            if el.id == "gen_drop": self.gen_type = "dfs" if i == 0 else "bfs"
                            if el.id == "solve_drop": self.solver_type = "backtrack" if i == 0 else "wall-follower"
                            break
                    if not clicked_any: el.expanded = False
            if not clicked_any:
                for el in self.elements:
                    if el.rect.collidepoint(pos):
                        self.on_click(el); clicked_any = True
                        if isinstance(el, Slider): el.dragging = True
                        break
            if not clicked_any:
                if pygame.Rect(CONTENT_OFFSET_X, 140, self.canvas_size, self.canvas_size).collidepoint(pos):
                    c, r = int((pos[0] - self.x_offset) / self.cell_size), int((pos[1] - self.y_offset) / self.cell_size)
                    if not self.is_animating:
                        if self.maze.start_cell and self.maze.end_cell: self.maze.start_cell = (r, c); self.maze.end_cell = None
                        elif self.maze.start_cell: (self.maze.start_cell != (r, c) and setattr(self.maze, 'end_cell', (r, c)))
                        else: self.maze.start_cell = (r, c)
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y += event.y * 30; lim = min(0, self.win_h - VIRTUAL_HEIGHT); self.scroll_y = max(lim, min(0, self.scroll_y))
        if event.type == pygame.VIDEORESIZE: self.win_w, self.win_h = event.w, event.h; self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONUP:
            for el in self.elements: (isinstance(el, Slider) and setattr(el, 'dragging', False))

    def on_click(self, el):
        if self.is_animating and el.id not in ["next_step", "step_mode", "speed_slider"]: return
        if isinstance(el, Dropdown): el.expanded = not el.expanded; return
        upd = False
        if el.id == "rows_inc": self.rows = min(50, self.rows + 1); upd = True
        elif el.id == "rows_dec": self.rows = max(5, self.rows - 1); upd = True
        elif el.id == "cols_inc": self.cols = min(50, self.cols + 1); upd = True
        elif el.id == "cols_dec": self.cols = max(5, self.cols - 1); upd = True
        if upd:
            self.calculate_grid(); self.maze = Maze(self.rows, self.cols)
            for e in self.elements: (isinstance(e, InputNumber) and setattr(e, 'val', self.rows if e.id=="rows" else self.cols))
            return
        if el.id == "challenge": el.checked = not el.checked; self.challenge_mode = el.checked
        elif el.id == "step_mode": el.checked = not el.checked; self.step_mode = el.checked; self.btn_next.enabled = el.checked
        elif el.id == "generate": self.start_gen()
        elif el.id == "solve": self.start_solve()
        elif el.id == "next_step": self.advance_algo()

    def start_gen(self):
        self.maze = Maze(self.rows, self.cols); self.calculate_grid(); self.current_algo = self.maze.generate_dfs(self.challenge_mode) if self.gen_type == "dfs" else self.maze.generate_bfs(self.challenge_mode); self.is_animating = True; self.status_text = "Generating..."; self.btn_solve.enabled = False
        
    def start_solve(self):
        if not self.maze.start_cell or not self.maze.end_cell: self.status_text = "Set points first!"; return
        self.current_algo = self.maze.solve_backtracking() if self.solver_type == "backtrack" else self.maze.solve_wall_follower(); self.is_animating = True; self.status_text = "Solving..."

    def advance_algo(self):
        if not self.current_algo: return
        try:
            self.algo_state = next(self.current_algo); tag = self.algo_state[0]
            if tag == "solved": self.is_animating = False; self.status_text = "Solved!"
            elif tag == "failed": self.is_animating = False; self.status_text = "No Path Found"
            elif tag == "loop": self.is_animating = False; self.status_text = "Trapped in cycle!"
            self.stats["path"] = len(self.algo_state[1]) if tag in ["step", "solved", "failed", "loop"] else (len(self.algo_state[2]) if tag in ["visit", "backtrack"] else 0)
            self.stats["visited"] = sum(1 for r in self.maze.visited for c in r if c > 0)
            if tag == "backtrack": self.stats["backtracks"] += 1
        except StopIteration:
            self.is_animating = False; ("Generating" in self.status_text and self.maze.reset_visited()); self.status_text = "Done"; self.btn_solve.enabled = True

    def run(self):
        while True:
            for event in pygame.event.get(): (event.type == pygame.QUIT and (pygame.quit() or sys.exit())); self.handle_event(event)
            if self.is_animating and not self.step_mode: (pygame.time.get_ticks() % max(16, self.speed) < 16 and self.advance_algo())
            m_pos = pygame.mouse.get_pos()
            for el in self.elements: (isinstance(el, Slider) and el.dragging and setattr(self, 'speed', el.min_val + (max(0, min(el.rect.w, m_pos[0] - (max(0, (self.win_w - VIRTUAL_WIDTH) // 2) + el.rect.x))) / el.rect.w) * (el.max_val - el.min_val)) or (isinstance(el, Slider) and el.dragging and setattr(el, 'curr_val', self.speed)))
            self.draw_ui(); self.draw_maze(); self.draw_algo_state(); self.screen.fill(COLOR_BG); win_off_x = max(0, (self.win_w - VIRTUAL_WIDTH) // 2); self.screen.blit(self.virtual_screen, (win_off_x, self.scroll_y))
            if VIRTUAL_HEIGHT > self.win_h:
                bh = (self.win_h / VIRTUAL_HEIGHT) * self.win_h; by = (-self.scroll_y / VIRTUAL_HEIGHT) * self.win_h
                pygame.draw.rect(self.screen, COLOR_BORDER, (self.screen.get_width()-8, 0, 6, self.win_h), border_radius=3); pygame.draw.rect(self.screen, COLOR_PRIMARY, (self.screen.get_width()-8, by, 6, bh), border_radius=3)
            pygame.display.flip(); self.clock.tick(FPS)

if __name__ == "__main__":
    app = MazeApp(); app.run()