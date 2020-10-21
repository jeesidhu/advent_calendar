from utils import read_file_as_string
from intcode import IntCode


def gravity_assist_program_part_1(arr, noun, verb):
    prog = IntCode(arr)
    prog.update(1, noun)
    prog.update(2, verb)
    prog.execute()
    return prog.get(0)


def gravity_assist_program_part_2(arr):
    for noun in range(100):
        for verb in range(100):
            if gravity_assist_program_part_1(arr, noun, verb) == 19690720:
                return 100 * noun + verb


def main():
    arr = list(map(int, read_file_as_string("input_2.txt").split(',')))
    p1 = gravity_assist_program_part_1(arr, 12, 2)
    p2 = gravity_assist_program_part_2(arr)
    print(f'part 1: {p1}, part 2: {p2}')


if __name__ == '__main__':
    main()
