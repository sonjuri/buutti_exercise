from collections import deque

class MazeAlgorithm:
    def __init__(self, maze_file, max_moves):
        self.maze_file = maze_file
        self.max_moves = max_moves
        self.maze = self.read_maze_file()

    ### Read txt file into 2D list
    def read_maze_file(self):
        with open(self.maze_file, 'r') as file:
            return [list(line.strip()) for line in file]

    ### Get the size of the complete maze
    def get_maze_size(self):
        maze_height = len(self.maze)     # Number of rows
        maze_width = len(self.maze[0]) if self.maze else 0     # Number of columns if maze has at least one row
        return maze_width, maze_height

    ### Get Pentti's position in the maze
    def get_penttis_position(self, pentti):
        maze_width, maze_height = self.get_maze_size()
        y_temp = -1
        for line in self.maze:
            y_temp += 1
            if pentti in line:
                x = line.index(pentti)
        y = maze_height - y_temp
        return x, y

    ### Move Pentti to different directions. Use the previous x and y values as current position.
    def move_pentti(self, position, direction):
        x, y = position

        if direction == "up":
            new_position = (x, y - 1)
        elif direction == "down":
            new_position = (x, y + 1)
        elif direction == "left":
            new_position = (x - 1, y)
        elif direction == "right":
            new_position = (x + 1, y)
        else:
            raise ValueError("Pentti cannot go that way.")      # Very unlikely error to get in this case, but just to make sure

        return new_position

    ### Solve the given maze
    ### Using deque to perform breadth-first search in order to find the optimal direction for each move
    def solve_maze(self):
        start_position = self.get_penttis_position("^")
        queue = deque([(start_position, 0)])
        visited = set([start_position])
        maze_width, maze_height = self.get_maze_size()

        while queue:
            current_position, moves = queue.popleft()    # popleft() used instead of pop() to ensure 'first in first out' in the queue
            x, y = current_position

            if self.maze[y][x] == "E":
                print(f"Pentti escaped the maze in {moves} moves, good job Pentti. The maximum number of moves was {self.max_moves} and this was the {self.maze_file} maze.")
                return True

            ### Go through all of the possible directions
            directions = ["up", "down", "left", "right"]
            for direction in directions:
                new_position = self.move_pentti(current_position, direction)
                new_width, new_height = new_position

                ### See if the new position is valid -> if it is in the maze, if it is a wall and if it has been visited before
                if (
                    0 <= new_width < maze_width
                    and 0 <= new_height < maze_height
                    and self.maze[new_height][new_width] != "#"
                    and new_position not in visited
                ):
                    queue.append((new_position, moves + 1))
                    visited.add(new_position)

        print(f"Pentti could not find a way out from the maze after {self.max_moves}")
        return False


### Tries for the first maze for each max moves
first_maze_file = "maze-task-first.txt"
f_twenty = MazeAlgorithm(first_maze_file, max_moves=20)
f_twenty.solve_maze()

f_hundred_fifty = MazeAlgorithm(first_maze_file, max_moves=150)
f_hundred_fifty.solve_maze()

f_two_hundred = MazeAlgorithm(first_maze_file, max_moves=200)
f_two_hundred.solve_maze()

### Tries for the second maze for each max moves
second_maze_file = "maze-task-second.txt"
s_twenty = MazeAlgorithm(second_maze_file, max_moves=20)
s_twenty.solve_maze()

s_hundred_fifty = MazeAlgorithm(second_maze_file, max_moves=150)
s_hundred_fifty.solve_maze()

s_two_hundred = MazeAlgorithm(second_maze_file, max_moves=200)
s_two_hundred.solve_maze()