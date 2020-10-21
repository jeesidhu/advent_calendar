from utils import read_file_as_lines


def calc_fuel(mass):
    return mass // 3 - 2


def total_fuel_part_1(masses):
    return sum(calc_fuel(mass) for mass in masses)


def total_fuel_part_2(masses):
    total_fuel = 0
    for mass in masses:
        fuel = calc_fuel(mass)
        while fuel > 0:
            total_fuel += fuel
            fuel = calc_fuel(fuel)
    return total_fuel


def main():
    masses = list(map(int, read_file_as_lines("input_1.txt")))
    p1 = total_fuel_part_1(masses)
    p2 = total_fuel_part_2(masses)
    print(f'part 1: {p1}, part 2: {p2}')


if __name__ == '__main__':
    main()
