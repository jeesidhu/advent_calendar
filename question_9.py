from utils import read_file_as_string
from intcode import IntCode


def boost_program(arr, inputs):
    prog = IntCode(arr, inputs)
    output = prog.execute()
    return output


def main():
    arr = list(map(int, read_file_as_string("input_9.txt").split(',')))
    p1 = boost_program(arr, [1])
    p2 = boost_program(arr, [2])
    print(f'part 1: {p1}, part 2: {p2}')


if __name__ == '__main__':
    main()
