def is_valid(v, visited, dest):
    # Check if this vertex is already visited or it is not a valid vertex
    return (v[0] >= 0) and (v[0] < len(visited)) and (v[1] >= 0) and (v[1] < len(visited[0])) and (visited[v[0]][v[1]] == False)

def backtrack(src, dest, visited, path):
    # Mark the source cell as visited
    visited[src[0]][src[1]] = True

    # If this vertex is the destination vertex, return True
    if src == dest:
        return True

    # Define the possible movements for the car
    moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Left, Up, Right, Down

    # Check all adjacent vertices
    for move in moves:
        adj = (src[0] + move[0], src[1] + move[1])

        if is_valid(adj, visited, dest):
            path.append(adj)

            # If a valid path is found, return True
            if backtrack(adj, dest, visited, path):
                return True

            # If no valid path is found, remove this vertex from the path
            path.pop()

    return False

def get_directions(src, dest):
    # Initialize the visited matrix
    visited = [[False for _ in range(100)] for _ in range(100)]

    # Initialize the path
    path = [src]

    # Run the backtracking algorithm
    if not backtrack(src, dest, visited, path):
        return []

    # Convert the path to directions
    directions = []
    for i in range(1, len(path)):
        if path[i][0] > path[i - 1][0]:
            directions.append('DOWN')
        elif path[i][0] < path[i - 1][0]:
            directions.append('UP')
        elif path[i][1] > path[i - 1][1]:
            directions.append('RIGHT')
        else:
            directions.append('LEFT')

    return directions
