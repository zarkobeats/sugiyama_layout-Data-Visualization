import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# data
edges = [
    (1, 4),
    (3, 4),
    (3, 5),
    (4, 6),
    (2, 4),
    (5, 7),
    (2, 5),
    (5, 6),
    (6, 7),
    (1, 6),
    (6, 8),
    (1, 7),
    (1, 8)
]

graph = nx.DiGraph()  # directed graph
graph.add_edges_from(edges)


# sugiyama layout
def sugiyama_layout(graph):
    acyclic_graph = cycle_breaking(graph)

    graph, positions, nodes_for_every_level, edges_copy = assign_levels_and_positions(acyclic_graph)

    positions = crossing_reduction(graph, positions, nodes_for_every_level)

    return positions


# step 1: cycle breaking
def cycle_breaking(graph):
    cycle_edges = list(nx.simple_cycles(graph))  # Find cycles in the graph

    for cycle in cycle_edges:
        u, v = cycle[0], cycle[-1]

        if u == v:
            graph.remove_edge(u, v)
        elif u != v:
            graph.remove_edge(u, v)
            graph.add_edge(v, u)

    return graph


# step 2: leveling
def assign_levels_and_positions(graph):
    levels = {}  # {2: 1, 3: 1, 1: 1, 5: 2, 4: 2, 6: 3, 8: 4, 7: 4}
    nodes_for_every_level = []  # [[2, 3, 1], [5, 4], [6], [8, 7]]
    dummy_nodes = []
    edges_copy = []  # [(3, 5), (2, 5), (3, 4), (1, 4), (2, 4), (4, 6), (5, 6), (1, 'd610'), ('d610', 6), (6, 8), (1, 'd810'),
    # ('d810', 'd811'), ('d811', 8), (5, 'd750'), ('d750', 7), (6, 7), (1, 'd710'), ('d710', 'd711'), ('d711', 7)]
    positions = {}

    for node in nx.topological_sort(graph):
        max_level = 0
        for predecessor in graph.predecessors(node):
            max_level = max(max_level, levels.get(predecessor))
        levels[node] = max_level + 1

    for node1, level in levels.items():
        for predecessor in graph.predecessors(node1):
            offset = abs(levels[node1] - levels[predecessor])
            dummy = [f"d{node1}{predecessor}{i}" for i in range(offset - 1)]
            if offset > 1:
                dummy_nodes_copy = [predecessor] + dummy + [node1]
                dummy_nodes.append(dummy)
                edges_copy += [(dummy_nodes_copy[i], dummy_nodes_copy[i + 1]) for i in range(len(dummy_nodes_copy) - 1)]
            if offset == 1:
                edges_copy += [(predecessor, node1)]

    graph.remove_edges_from(edges)
    graph.add_edges_from(edges_copy)

    for dummy_list in dummy_nodes:
        for dummy1 in dummy_list:
            for predecessor1 in graph.predecessors(dummy1):
                levels[dummy1] = levels[predecessor1] + 1

    for key, value in levels.items():
        index_ = value - 1
        node = key
        while len(nodes_for_every_level) <= index_:
            nodes_for_every_level.append([])
        nodes_for_every_level[index_].append(node)

    for i, lists in enumerate(nodes_for_every_level):
        for j, item in enumerate(lists):
            positions[item] = (j, -i)
    return graph, positions, nodes_for_every_level, edges_copy


# step 3: Crossings minimization
def count_crossings(nodes_for_every_level, edges_copy):
    crossings = 0
    for i, item in enumerate(nodes_for_every_level):
        if i < len(nodes_for_every_level) - 1:  # Process all levels except the last one
            rows = nodes_for_every_level[i]
            columns = nodes_for_every_level[i + 1]
            index_map = {val: idx for idx, val in enumerate(rows)}
            index_map.update({val: idx + len(rows) for idx, val in enumerate(columns)})

            matrix_size = (len(rows), len(columns))
            matrix = np.zeros(matrix_size, dtype=int)
            for edge in edges_copy:
                vertical = index_map.get(edge[0])
                horizontal = index_map.get(edge[1])
                if vertical is not None and horizontal is not None:
                    matrix[vertical, horizontal - len(rows)] = 1

            current_levels_crossings = 0
            for row_index, row in enumerate(matrix):
                for col_index, cell in enumerate(row):
                    if cell == 1:
                        for prev_row_index in range(row_index):
                            current_levels_crossings += sum(matrix[prev_row_index][col_index + 1:])
            crossings += current_levels_crossings
            print(matrix)
    return crossings


def crossing_reduction(graph, positions, nodes_for_every_level):
    for level_nodes in nodes_for_every_level:
        barycenter = calculate_barycenter(graph, level_nodes, positions)
        level_nodes.sort(key=lambda node: barycenter[node])
        for i, node in enumerate(level_nodes):
            positions[node] = i, positions[node][1]
    return positions


# calculating the barycenter based on the positions of the predecessors
def calculate_barycenter(graph, level_nodes, positions):
    barycenter = {}
    for i, node in enumerate(level_nodes):
        sum_of_positions_of_predecessors = 0
        number_of_predecessors = 0
        for predecessor in graph.predecessors(node):
            sum_of_positions_of_predecessors += positions[predecessor][0]
            number_of_predecessors += 1
        if number_of_predecessors > 0:
            barycenter[node] = sum_of_positions_of_predecessors / number_of_predecessors
        else:
            barycenter[node] = i  # if no predecessors, barycenter is i
    return barycenter


# step 4: final positions
positions = sugiyama_layout(graph)

# step 5: Visualization
plt.figure(figsize=(10, 8))
nx.draw(graph, pos=positions, with_labels=True, node_size=1000, node_color="lightblue", font_size=12)
plt.suptitle("Sugiyama layout")
plt.show()
