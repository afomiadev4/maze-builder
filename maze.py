class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        

        self.north_wall = [[1 for _ in range(cols)] for _ in range(rows)]
        
        self.east_wall = [[1 for _ in range(cols)] for _ in range(rows)]
        
        
        self.phantom_bottom_row = [1 for _ in range(cols)]
        
        self.left_edge_boundary = [1 for _ in range(rows)]

    def break_wall(self, r, c, direction):
       
        if direction == "N":
            self.north_wall[r][c] = 0
        elif direction == "E":
            self.east_wall[r][c] = 0
        elif direction == "S":
            if r > 0:
                self.north_wall[r-1][c] = 0
            else:
                self.phantom_bottom_row[c] = 0
        elif direction == "W":
            if c > 0:
                self.east_wall[r][c-1] = 0
            else:
                self.left_edge_boundary[r] = 0

    def is_wall_intact(self, r, c, direction):
        
        if direction == "N":
            return self.north_wall[r][c] == 1
        elif direction == "E":
            return self.east_wall[r][c] == 1
        elif direction == "S":
            if r > 0:
                return self.north_wall[r-1][1] == 1
            return self.phantom_bottom_row[c] == 1
        elif direction == "W":
            if c > 0:
                return self.east_wall[r][c-1] == 1
            return self.left_edge_boundary[r] == 1
        

    