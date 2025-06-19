from collections import deque

def find_shortest_path(grid):
    rows = len(grid)
    cols = len(grid[0])

    # Найти начальную и конечную точки
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                if start is None:
                    start = (r, c)
                else:
                    end = (r, c)

    if not start or not end:
        return None  # Не найдено две точки

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Вверх, вниз, влево, вправо
    visited = [[False]*cols for _ in range(rows)]
    parent = {}  # Для восстановления пути

    queue = deque()
    queue.append(start)
    visited[start[0]][start[1]] = True

    while queue:
        curr = queue.popleft()
        if curr == end:
            break  # Путь найден

        r, c = curr
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if not visited[nr][nc] and grid[nr][nc] != 1:
                    visited[nr][nc] = True
                    parent[(nr, nc)] = curr
                    queue.append((nr, nc))

    # Если путь не найден
    if not visited[end[0]][end[1]]:
        return None

    # Восстановление пути
    path = []
    current = end
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()

    # Пометить путь (например, значением 3)
    result = [row[:] for row in grid]  # Скопировать матрицу
    for r, c in path:
        if result[r][c] == 0:
            result[r][c] = 3

    return result
