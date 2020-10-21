from intcode import IntCode
from utils import read_file_as_string


class Robot:

    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def turn_left(self):
        left = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
        self.direction = left[self.direction]

    def turn_right(self):
        right = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
        self.direction = right[self.direction]

    def move_forward(self):
        step = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}
        x = self.position[0] + step[self.direction][0]
        y = self.position[1] + step[self.direction][1]
        self.position = (x, y)


def run_robot(arr, start_color):
    prog = IntCode(arr)
    start_pos = (0, 0)
    robot = Robot(start_pos, 'N')
    panels = {}
    while not prog.halted:
        default_color = start_color if robot.position == start_pos else 0
        current_color = panels.get(robot.position, default_color)
        prog.add_to_inputs(current_color)
        new_color = prog.execute(pause_on_output=True)
        panels[robot.position] = new_color
        turn = prog.execute(pause_on_output=True)
        robot.turn_left() if turn == 0 else robot.turn_right()
        robot.move_forward()
    return panels


def render(panel):
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    for x, y in panel:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    height = max_y - min_y + 1
    width = max_x - min_x + 1
    canvas = [[' ' for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            pos = (min_x + x, min_y + y)
            if panel.get(pos, 0) == 1:
                canvas[y][x] = '#'
    return '\n'.join(''.join(row) for row in canvas)


def main():
    arr = list(map(int, read_file_as_string("input_11.txt").split(',')))
    p1 = len(run_robot(arr, 0))
    panel = run_robot(arr, 1)
    p2 = render(panel)
    print(f'part 1: {p1}, part 2: \n{p2}')


if __name__ == '__main__':
    main()
