import random

def generate_dfs(maze, challenge_mode=False):
    from maze import Direction
    maze.reset_visited()
    curr_r = random.randint(0, maze.rows - 1)
    curr_c = random.randint(0, maze.cols - 1)
    maze.visited[curr_r][curr_c] = 1
    stack = [(curr_r, curr_c)]
    
    yield ("start", (curr_r, curr_c))

    while stack:
        curr_r, curr_c = stack[-1]
        neighbors = maze.get_unvisited_neighbors(curr_r, curr_c)
        
        if neighbors:
            next_r, next_c, direction = random.choice(neighbors)
            maze.remove_wall(curr_r, curr_c, direction)
            maze.visited[next_r][next_c] = 1
            stack.append((next_r, next_c))
            
            if challenge_mode and random.random() < 0.05:
                rand_dir = random.choice(list(Direction))
                maze.remove_wall(curr_r, curr_c, rand_dir)
            
            yield ("visit", (next_r, next_c), list(stack))
        else:
            stack.pop()
            yield ("backtrack", (curr_r, curr_c), list(stack))

def generate_bfs(maze, challenge_mode=False):
    from maze import Direction
    maze.reset_visited()
    curr_r = random.randint(0, maze.rows - 1)
    curr_c = random.randint(0, maze.cols - 1)
    maze.visited[curr_r][curr_c] = 1
    queue = [(curr_r, curr_c)]
    
    yield ("start", (curr_r, curr_c))

    while queue:
        curr_r, curr_c = queue[0]
        neighbors = maze.get_unvisited_neighbors(curr_r, curr_c)
        
        if neighbors:
            next_r, next_c, direction = random.choice(neighbors)
            maze.remove_wall(curr_r, curr_c, direction)
            maze.visited[next_r][next_c] = 1
            queue.append((next_r, next_c))
            
            if challenge_mode and random.random() < 0.05:
                rand_dir = random.choice(list(Direction))
                if rand_dir == Direction.NORTH and curr_r > 0: maze.remove_wall(curr_r, curr_c, rand_dir)
                if rand_dir == Direction.SOUTH and curr_r < maze.rows - 1: maze.remove_wall(curr_r, curr_c, rand_dir)
                if rand_dir == Direction.WEST and curr_c > 0: maze.remove_wall(curr_r, curr_c, rand_dir)
                if rand_dir == Direction.EAST and curr_c < maze.cols - 1: maze.remove_wall(curr_r, curr_c, rand_dir)

            yield ("visit", (next_r, next_c), list(queue))
        else:
            queue.pop(0)
            yield ("backtrack", (curr_r, curr_c), list(queue))
