import argparse
from collections import deque


class MazeAlgorithm:
    def __init__(self, maze_file, max_moves):
        self.maze_file = maze_file
        self.max_moves = max_moves
        self.maze = self.read_maze_file()
        self.start_position = None
        self.exit_position = None

    def read_maze_file(self):
        """
        Read txt file into 2D list

        :return: maze as 2D array
        """
        try:
            with open(self.maze_file, "r") as file:
                return [list(line.strip()) for line in file]
        except FileNotFoundError:
            print(f"File '{self.maze_file}' was not found")

    def get_maze_size(self):
        """
        Get the size of the complete maze

        :return: maze size as height and width
        """
        maze_height = len(self.maze)  # Number of rows
        maze_width = (
            len(self.maze[0]) if self.maze else 0
        )  # Number of columns if maze has at least one row
        return maze_width, maze_height

    def get_penttis_position(self):
        """
        Get Pentti's position in the maze
        
        :return: x an y coordinates for Pentti's location
        """
        y = -1
        for line in self.maze:
            y += 1
            if "^" in line:
                x = line.index("^")
                break
        return x, y

    def move_pentti(self, position, direction):
        """
        Move Pentti to different directions. Use the previous x and y values as current position.

        :position: Pentti's position in the maze
        :direction: Direction of the movement
        :return: New location for Pentti
        """
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
            raise ValueError(
                "Pentti cannot go that way."
            )  # Very unlikely error to because breadth-first search is used, but just to make sure

        return new_position

    def solve_maze(self):
        """
        Solve the given maze
        Using deque to perform breadth-first search in order to find the optimal direction for each move
        The positions that are present in the code are stored in position_dict
        popleft() is used in the while-loop instead of pop() to ensure 'first in first out' in the queue.
        Go through all of the possible directions, checks if the position is valid (is it's in the maze, it it's a wall, has it been visited)
        
        :return: dictionary of the positions in the maze
        """
        self.start_position = self.get_penttis_position()
        queue = deque([(self.start_position, 0)])
        visited = set([self.start_position])
        maze_width, maze_height = self.get_maze_size()
        position_dict = {}
        solved = False

        while queue:
            current_position, moves = queue.popleft()

            if moves > self.max_moves:
                print(f"Pentti could not find a way out from the maze after {self.max_moves} moves")
                break

            x, y = current_position

            if self.maze[y][x] == "E":
                print(
                    f"Pentti escaped the maze in {moves} moves, good job Pentti."
                    f"The maximum number of moves was {self.max_moves} and this was the {self.maze_file} maze."
                )
                solved = True
                self.exit_position = current_position
                self.mark_path(position_dict)
                return position_dict, solved

            directions = ["up", "down", "left", "right"]
            for direction in directions:
                new_position = self.move_pentti(current_position, direction)
                new_width, new_height = new_position

                if (
                    0 <= new_width < maze_width
                    and 0 <= new_height < maze_height
                    and self.maze[new_height][new_width] != "#"
                    and new_position not in visited
                ):
                    queue.append((new_position, moves + 1))
                    visited.add(new_position)
                    position_dict[new_position] = current_position

        return position_dict, solved


    def mark_path(self, position_dict):
        """
        Mark the optimal path on the maze

        :position_dict: Dictionary where the positions are saved to
        """
        path_position = self.exit_position
        while path_position != self.start_position:
            x, y = path_position
            if path_position not in position_dict:
                break
            self.maze[y][x] = "*"
            path_position = position_dict[path_position]
            

    def print_maze(self):
        """
        Print the maze with the optimal solution(s)
        """
        for row in self.maze:
            print(''.join(row))

parser = argparse.ArgumentParser()
parser.add_argument('maze_file', type=str,
                    help='The maze file to be solved')
parser.add_argument('max_moves', type=int,
                    help='Max moves to be used to solve the maze')
args = parser.parse_args()

maze_file = args.maze_file
max_moves = args.max_moves
maze_alg = MazeAlgorithm(maze_file, max_moves=max_moves)

if maze_alg.maze:
    position_dict_first_maze, solved = maze_alg.solve_maze()
    if solved:
        maze_alg.mark_path(position_dict_first_maze)
        maze_alg.print_maze()