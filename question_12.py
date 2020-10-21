import re

from utils import read_file_as_lines


class Axes:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        for attr in self.__dict__:
            yield attr

    def __getitem__(self, axis):
        return self.__dict__[axis]

    def __setitem__(self, axis, value):
        self.__dict__[axis] = value

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, z: {self.z}'


class Moon:

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update_gravity(self, other):
        for axis in self.position:
            self._update_gravity_on_axis(axis, other)

    def _update_gravity_on_axis(self, axis, other):
        if self.position[axis] < other.position[axis]:
            self.velocity[axis] += 1
        elif self.position[axis] > other.position[axis]:
            self.velocity[axis] -= 1

    def update_velocity(self):
        for axis in self.position:
            self.position[axis] += self.velocity[axis]

    def potential_energy(self):
        return sum(abs(self.position[axis]) for axis in self.position)

    def kinetic_energy(self):
        return sum(abs(self.velocity[axis]) for axis in self.velocity)

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def __str__(self):
        return str(self.velocity)


def apply_gravity(moons):
    for i in range(len(moons)):
        for j in range(i + 1, len(moons)):
            moons[i].update_gravity(moons[j])
            moons[j].update_gravity(moons[i])


def apply_velocity(moons):
    for moon in moons:
        moon.update_velocity()


def simulate_motion(moons, steps):
    for _ in range(steps):
        apply_gravity(moons)
        apply_velocity(moons)


def total_system_energy(moons):
    simulate_motion(moons, 1000)
    return sum(moon.total_energy() for moon in moons)


def parse_position(string):
    match = re.findall(r'-?\d+', string)
    return Axes(int(match[0]), int(match[1]), int(match[2]))


def main():
    input_ = read_file_as_lines("input_12.txt")
    positions = [parse_position(line) for line in input_]
    moons = [Moon(pos, Axes(0, 0, 0)) for pos in positions]
    p1 = total_system_energy(moons)
    p2 = ""
    print(f'part 1: {p1}, part 2: {p2}')


if __name__ == '__main__':
    main()
