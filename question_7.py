import itertools

from utils import read_file_as_string
from intcode import IntCode


def amplifier_controller_software_part_1(arr):
    highest_signal = float('-inf')
    perms = itertools.permutations(range(5))
    for perm in perms:
        last_output = 0
        for i in range(5):
            program = IntCode(arr, inputs=[perm[i], last_output])
            output = program.execute(pause_on_output=True)
            last_output = output
        highest_signal = max(highest_signal, last_output)
    return highest_signal


def amplifier_controller_software_part_2(arr):
    highest_signal = float('-inf')
    perms = itertools.permutations(range(5, 10))
    for perm in perms:
        programs = [IntCode(arr, inputs=[perm[i]]) for i in range(5)]
        last_output = 0
        while not programs[-1].halted:
            for program in programs:
                program.add_to_inputs(last_output)
                output = program.execute(pause_on_output=True)
                if output:
                    last_output = output
        highest_signal = max(highest_signal, last_output)
    return highest_signal


def main():
    arr = list(map(int, read_file_as_string("input_7.txt").split(',')))
    p1 = amplifier_controller_software_part_1(arr)
    p2 = amplifier_controller_software_part_2(arr)
    print(f'part 1: {p1}, part 2: {p2}')


if __name__ == '__main__':
    main()
