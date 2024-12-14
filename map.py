# https://rosettacode.org/wiki/Maze_generation#Python
from random import shuffle, randrange

def make_maze(w=6, h=6):
    # 미로의 방문 여부를 추적
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    # 수직, 수평 벽 정보 저장
    walls = {'vertical': [[True] * (w + 1) for _ in range(h)],
             'horizontal': [[True] * w for _ in range(h + 1)]}

    def walk(x, y):
        vis[y][x] = 1
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                walls['horizontal'][max(y, yy)][x] = False  # 수평 벽 제거
            if yy == y:
                walls['vertical'][y][max(x, xx)] = False  # 수직 벽 제거
            walk(xx, yy)

    walk(randrange(w), randrange(h))
    return walls
