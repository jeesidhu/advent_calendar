import heapq
import math
from collections import defaultdict

from utils import read_file_as_lines


class Coordinate:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Asteroid:
    id_ = "#"

    def __init__(self, coordinate):
        self.coordinate = coordinate

    def angle(self, other):
        dx = self.coordinate.x - other.coordinate.x
        dy = self.coordinate.y - other.coordinate.y
        radians = -math.atan2(dx, dy)
        degrees = math.degrees(radians)
        return degrees

    def distance(self, other):
        dx = self.coordinate.x - other.coordinate.x
        dy = self.coordinate.y - other.coordinate.y
        return abs(dx) + abs(dy)


def parse_asteroids(map_):
    asteroids = set()
    for y, row in enumerate(map_):
        for x, cell in enumerate(row):
            if cell == Asteroid.id_:
                coordinate = Coordinate(x, y)
                asteroid = Asteroid(coordinate)
                asteroids.add(asteroid)
    return asteroids


def asteroids_in_sight(location, asteroids):
    in_sight = set()
    for asteroid in asteroids:
        if asteroid != location:
            in_sight.add(asteroid.angle(location))
    return len(in_sight)


def best_monitoring_station_location(asteroids):
    station = None
    highest_in_sight = 0
    for asteroid in asteroids:
        in_sight = asteroids_in_sight(asteroid, asteroids)
        if in_sight > highest_in_sight:
            highest_in_sight = in_sight
            station = asteroid
    return station, highest_in_sight


def vaporize(laser, asteroids):
    metadata = defaultdict(list)
    for asteroid in asteroids:
        if asteroid != laser:
            angle = asteroid.angle(laser)
            distance = asteroid.distance(laser)
            heapq.heappush(metadata[angle], (distance, asteroid))

    vaporized = []
    while len(vaporized) != len(asteroids) - 1:
        for angle in sorted(metadata):
            if metadata[angle]:
                asteroid = heapq.heappop(metadata[angle])[1]
                vaporized.append(asteroid)
    return vaporized


def main():
    map_ = read_file_as_lines("input_10.txt")
    asteroids = parse_asteroids(map_)
    location, p1 = best_monitoring_station_location(asteroids)
    vaporized = vaporize(location, asteroids)
    p2 = vaporized[199].coordinate.x * 100 + vaporized[199].coordinate.y
    print(f'part 1: {p1}, part 2: {p2}')


if __name__ == '__main__':
    main()
