import itertools
from collections import defaultdict, deque

from utils import read_file_as_lines


def build_directed_graph(map_of_orbits):
    graph = {'COM': None}
    for orbit in map_of_orbits:
        parent, child = orbit.split(")")
        graph[child] = parent
    return graph


def num_of_parents(obj, graph):
    if graph[obj] is None:
        return 0
    return 1 + num_of_parents(graph[obj], graph)


def orbit_count_checksums(map_of_orbits):
    graph = build_directed_graph(map_of_orbits)
    return sum(num_of_parents(obj, graph) for obj in graph)


def build_undirected_graph(map_of_orbits):
    graph = defaultdict(list)
    for orbit in map_of_orbits:
        obj_1, obj_2 = orbit.split(")")
        graph[obj_1].append(obj_2)
        graph[obj_2].append(obj_1)
    return graph


def _bfs(from_obj, to_obj, graph):
    queue = deque([(from_obj, 0)])
    visited = set(from_obj)
    while queue:
        obj, dist = queue.popleft()
        if obj == to_obj:
            return dist
        for neigh in graph[obj]:
            if neigh not in visited:
                visited.add(neigh)
                queue.append((neigh, dist + 1))


def minimum_orbital_transfers(map_of_orbits):
    undirected_graph = build_undirected_graph(map_of_orbits)
    return _bfs("YOU", "SAN", undirected_graph) - 2


def main():
    map_of_orbits_1, map_of_orbits_2 = itertools.tee(read_file_as_lines("input_6.txt"))
    p1 = orbit_count_checksums(map_of_orbits_1)
    p2 = minimum_orbital_transfers(map_of_orbits_2)
    print(f'part 1: {p1}, part 2: {p2}')


if __name__ == '__main__':
    main()
