import random

def solve_backtracking(maze):
    maze.reset_visited()
    start_r, start_c = maze.start_cell
    stack = [(start_r, start_c)]
    maze.visited[start_r][start_c] = 1
    
    while stack:
        curr_r, curr_c = stack[-1]
        
        if (curr_r, curr_c) == maze.end_cell:
            yield ("solved", list(stack))
            return

        yield ("step", list(stack), maze.visited)

        moves = maze.get_valid_moves(curr_r, curr_c)
        unvisited_moves = [m for m in moves if maze.visited[m[0]][m[1]] == 0]

        if unvisited_moves:
            next_r, next_c, _ = random.choice(unvisited_moves)
            maze.visited[next_r][next_c] = 1
            stack.append((next_r, next_c))
        else:
            maze.visited[curr_r][curr_c] = 2  # Dead end
            stack.pop()
    
    yield ("failed", [])

def solve_wall_follower(maze):
    from maze import Direction
    dir_vectors = {
        Direction.NORTH: (-1, 0),
        Direction.EAST: (0, 1),
        Direction.SOUTH: (1, 0),
        Direction.WEST: (0, -1)
    }
    dir_order = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
    
    curr_r, curr_c = maze.start_cell
    curr_dir_idx = 1 # Start facing East
    
    maze.reset_visited()
    path = [(curr_r, curr_c)]
    maze.visited[curr_r][curr_c] = 1
    
    max_steps = maze.rows * maze.cols * 10
    steps = 0
    
    while steps < max_steps:
        if (curr_r, curr_c) == maze.end_cell:
            yield ("solved", list(path))
            return
        
        yield ("step", list(path), maze.visited)
        
        priorities = [
            (curr_dir_idx + 1) % 4, # Right
            curr_dir_idx,           # Straight
            (curr_dir_idx + 3) % 4, # Left
            (curr_dir_idx + 2) % 4  # Back
        ]
        
        moved = False
        for p_idx in priorities:
            target_dir = dir_order[p_idx]
            can_move = False
            if target_dir == Direction.NORTH and curr_r > 0 and maze.north_wall[curr_r][curr_c] == 0: can_move = True
            if target_dir == Direction.SOUTH and curr_r < maze.rows - 1 and maze.north_wall[curr_r + 1][curr_c] == 0: can_move = True
            if target_dir == Direction.WEST and curr_c > 0 and maze.east_wall[curr_r][curr_c] == 0: can_move = True
            if target_dir == Direction.EAST and curr_c < maze.cols - 1 and maze.east_wall[curr_r][curr_c + 1] == 0: can_move = True
            
            if can_move:
                dr, dc = dir_vectors[target_dir]
                new_r = curr_r + dr
                new_c = curr_c + dc
                
                if maze.visited[new_r][new_c] >= 1:
                    maze.visited[curr_r][curr_c] = 2
                    maze.visited[new_r][new_c] = 2
                else:
                    maze.visited[new_r][new_c] = 1
                
                curr_r, curr_c = new_r, new_c
                curr_dir_idx = p_idx
                path.append((curr_r, curr_c))
                moved = True
                break
        
        if not moved:
            break
        steps += 1
        
    if steps >= max_steps:
        yield ("loop", list(path))
    else:
        yield ("failed", list(path))
