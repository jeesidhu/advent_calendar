from utils import read_file_as_string
from intcode import IntCode


def diagnostic_program(arr, inputs):
    program = IntCode(arr, inputs)
    output = program.execute()
    return output


def main():
    arr = list(map(int, read_file_as_string("input_5.txt").split(',')))
    p1 = diagnostic_program(arr, [1])
    p2 = diagnostic_program(arr, [5])
    print(f'part 1: {p1}, part 2: {p2}')


if __name__ == '__main__':
    main()
