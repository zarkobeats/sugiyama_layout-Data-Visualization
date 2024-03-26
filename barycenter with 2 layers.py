import numpy as np

# Define the lists for x and y axes

nodes_for_every_level = [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h', 'i']]
edges = [('a', 'e'), ('a', 'f'), ('b', 'e'), ('b', 'h'), ('b', 'i'), ('c', 'f'), ('c', 'h'), ('c', 'i'), ('d', 'e'), ('d', 'g'), ('d', 'i')]

# nodes_for_every_level = [['a', 'b', 'c'], ['d', 'e', 'f']]
# edges = [('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'f')]
previous_matrix = None

for i, item in enumerate(nodes_for_every_level):
    if i < len(nodes_for_every_level) - 1:
        rows = nodes_for_every_level[i]
        columns = nodes_for_every_level[i + 1]
        index_map = {val: idx for idx, val in enumerate(rows)}
        index_map.update({val: idx + len(rows) for idx, val in enumerate(columns)})

        matrix_size = (len(rows), len(columns))
        matrix = np.zeros(matrix_size, dtype=int)
        for edge in edges:
            vertical = index_map.get(edge[0])
            horizontal = index_map.get(edge[1])
            if vertical is not None and horizontal is not None:
                matrix[vertical, horizontal - len(rows)] = 1


def reorder_matrix(matrix, nodes_for_every_level_copy):
    row_barycenters = np.zeros(matrix.shape[0])
    for i, row in enumerate(matrix):
        row_indices = np.nonzero(row)
        row_barycenter = np.mean(row_indices)
        row_barycenters[i] = round(row_barycenter, 2)

    sorted_row_indices = np.argsort(row_barycenters)
    sorted_matrix = matrix[sorted_row_indices]
    column_barycenters = np.zeros(sorted_matrix.shape[1])

    for j, col in enumerate(sorted_matrix.T):
        col_indices = np.nonzero(col)
        if len(col_indices[0]) > 0:
            col_barycenter = (np.mean(col_indices))
        column_barycenters[j] = round(col_barycenter, 2)

    sorted_column_indices = np.argsort(column_barycenters)
    final_sorted_matrix = sorted_matrix[:, sorted_column_indices]

    return final_sorted_matrix, column_barycenters, row_barycenters, nodes_for_every_level_copy


def recursion_matrix(matrix, nodes_for_every_level_copy):
    global previous_matrix
    final_sorted_matrix, column_barycenters, row_barycenters, nodes_for_every_level_copy = reorder_matrix(matrix, nodes_for_every_level_copy)

    columns_with_same_barycenter = {}
    rows_with_same_barycenter = {}

    for idx in range(len(nodes_for_every_level_copy) - 1):
        original_row_alias = np.array(nodes_for_every_level_copy[idx])
        original_column_alias = np.array(nodes_for_every_level_copy[idx + 1])
        original_row_indices = np.arange(len(original_row_alias))
        original_column_indices = np.arange(len(original_column_alias))

        bary_sorted_idx_row = np.argsort(row_barycenters)
        original_row_indices = original_row_indices[bary_sorted_idx_row]

        bary_sorted_idx_col = np.argsort(column_barycenters)
        original_column_indices = original_column_indices[bary_sorted_idx_col]

        upper_row = original_row_alias[original_row_indices]
        lower_row = original_column_alias[original_column_indices]
        nodes_for_every_level_copy = [list(upper_row)] + [list(lower_row)]

    if np.array_equal(final_sorted_matrix, previous_matrix):
        if len(set(column_barycenters)) != len(column_barycenters) or len(set(row_barycenters)) != len(row_barycenters):
            for i, r_barycente in enumerate(row_barycenters):
                if r_barycente not in rows_with_same_barycenter:
                    rows_with_same_barycenter[r_barycente] = [i]
                else:
                    rows_with_same_barycenter[r_barycente].append(i)

        for c_barycenter, rows in rows_with_same_barycenter.items():
            if len(rows) > 1:
                for i in range(len(rows) - 1):
                    final_sorted_matrix[:, [rows[i], rows[i + 1]]] = final_sorted_matrix[:, [rows[i + 1], rows[i]]]
                    nodes_for_every_level_copy[idx][rows[i]], nodes_for_every_level_copy[idx][rows[i + 1]] = nodes_for_every_level_copy[idx][rows[i + 1]], nodes_for_every_level_copy[idx][rows[i]]

            for i, c_barycenter in enumerate(column_barycenters):
                if c_barycenter not in columns_with_same_barycenter:
                    columns_with_same_barycenter[c_barycenter] = [i]
                else:
                    columns_with_same_barycenter[c_barycenter].append(i)

        for barycenter, columns in columns_with_same_barycenter.items():
            if len(columns) > 1:
                for i in range(len(columns) - 1):
                    final_sorted_matrix[:, [columns[i], columns[i + 1]]] = final_sorted_matrix[:, [columns[i + 1], columns[i]]]
                    nodes_for_every_level_copy[idx + 1][columns[i]], nodes_for_every_level_copy[idx + 1][columns[i + 1]] = nodes_for_every_level_copy[idx + 1][columns[i + 1]], nodes_for_every_level_copy[idx + 1][columns[i]]

        if len(set(column_barycenters)) == len(column_barycenters) and len(set(row_barycenters)) == len(row_barycenters):
            return final_sorted_matrix, nodes_for_every_level_copy
        return recursion_matrix(final_sorted_matrix, nodes_for_every_level_copy)
    else:
        previous_matrix = final_sorted_matrix
        return recursion_matrix(final_sorted_matrix, nodes_for_every_level_copy)


last_sorted_matrix, nodes_for_every_level = recursion_matrix(matrix, nodes_for_every_level)

print(nodes_for_every_level)
