import pygame

class UIElement:
    def __init__(self, x, y, w, h, id=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.id = id
        self.hovered = False

class Button(UIElement):
    def __init__(self, x, y, w, h, label, id, style="primary", enabled=True):
        super().__init__(x, y, w, h, id)
        self.label = label
        self.style = style
        self.enabled = enabled

class Dropdown(UIElement):
    def __init__(self, x, y, w, h, options, curr_idx, id):
        super().__init__(x, y, w, h, id)
        self.options = options
        self.curr_idx = curr_idx
        self.expanded = False

class Slider(UIElement):
    def __init__(self, x, y, w, h, min_val, max_val, curr_val, label, id):
        super().__init__(x, y, w, h, id)
        self.min_val = min_val
        self.max_val = max_val
        self.curr_val = curr_val
        self.dragging = False
        self.label = label

class InputNumber(UIElement):
    def __init__(self, x, y, w, h, val, id):
        super().__init__(x, y, w, h, id)
        self.val = val

class Checkbox(UIElement):
    def __init__(self, x, y, label, id, checked=False):
        super().__init__(x, y, 20, 20, id)
        self.label = label
        self.checked = checked