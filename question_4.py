from utils import read_file_as_string


def valid_password_part_1(password):
    if len(password) != 6:
        return False
    if any(password[idx - 1] > password[idx] for idx in range(1, 6)):
        return False
    if all(password[idx - 1] != password[idx] for idx in range(1, 6)):
        return False
    return True


def valid_password_part_2(password):
    if len(password) != 6:
        return False
    if any(password[idx - 1] > password[idx] for idx in range(1, 6)):
        return False
    if all(password.count(char) != 2 for char in set(password)):
        return False
    return True


def num_of_passwords(low, high, valid):
    return sum(valid(str(num)) for num in range(low, high + 1))


def main():
    low, high = map(int, read_file_as_string("input_4.txt").split("-"))
    p1 = num_of_passwords(low, high, valid_password_part_1)
    p2 = num_of_passwords(low, high, valid_password_part_2)
    print(f'part 1: {p1}, part 2: {p2}')


if __name__ == '__main__':
    main()
