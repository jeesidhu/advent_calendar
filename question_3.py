from utils import read_file_as_lines

STEPS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}


def manhattan(coord_1, coord_2):
    return abs(coord_1[0] - coord_2[0]) + abs(coord_1[1] - coord_2[1])


def path(start_pos, moves):
    x, y = start_pos[0], start_pos[1]
    coords = set()
    for move in moves:
        direction = move[0]
        steps = int(move[1:])
        for _ in range(steps):
            x += STEPS[direction][0]
            y += STEPS[direction][1]
            coords.add((x, y))
    return coords


def closest_intersection_part_1(wires):
    central_port = (0, 0)
    wire_1_path = path(central_port, wires[0])
    wire_2_path = path(central_port, wires[1])
    intersections = [coord for coord in wire_1_path if coord in wire_2_path]
    return min(manhattan(central_port, intersection)
               for intersection in intersections)


def path_with_steps(start_pos, moves):
    x, y = start_pos[0], start_pos[1]
    steps_so_far = 0
    coords = {}
    for move in moves:
        direction = move[0]
        steps = int(move[1:])
        for step in range(steps):
            x += STEPS[direction][0]
            y += STEPS[direction][1]
            steps_so_far += 1
            # Only want to record steps from the first time
            # a wire visits the same position
            if (x, y) not in coords:
                coords[(x, y)] = steps_so_far
    return coords


def closest_intersection_part_2(wires):
    central_port = (0, 0)
    wire_1_path = path_with_steps(central_port, wires[0])
    wire_2_path = path_with_steps(central_port, wires[1])
    intersections = [coord for coord in wire_1_path if coord in wire_2_path]
    return min(wire_1_path[intersection] + wire_2_path[intersection]
               for intersection in intersections)


def main():
    wires = [line.split(",") for line in read_file_as_lines("input_3.txt")]
    p1 = closest_intersection_part_1(wires)
    p2 = closest_intersection_part_2(wires)
    print(f'part 1: {p1}, part 2: {p2}')


if __name__ == '__main__':
    main()
