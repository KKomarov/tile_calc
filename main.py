import random


def tile_calc():
    w = 7
    h = 19
    tile_map = [
        [-1] * h,
        [-1] * h,
        [-1] * h,
        [5, 7, 6, 6, 1, 4, 2, 5, 6, 3, 7, 6, 4, 2, 7, 6, 4, 4, -1],
        [3, 1, 4, 2, 5, 6, 7, 3, 1, 4, 2, 1, 3, 5, -1, -1, -1, -1, -1],
        [-1] * h,
        [-1] * h,
    ]
    stock = [11 + 2, 15 + 1, 8 + 1, 16 + 2, 9 + 1, 11, 13 + 2]
    tile_map = [
        [-1] * h,
        [-1] * h,
        [4, 2, 1, 4, 2, 7, 6, 7, 4, 2, 1, 5, -1, -1, -1, -1, -1, -1, -1],
        [5, 7, 6, 6, 1, 4, 2, 5, 6, 3, 7, 6, 4, 2, 7, 6, 4, 4, -1],
        [3, 1, 4, 2, 5, 6, 7, 3, 1, 4, 2, 1, 3, 5, 4, 2, 7, 1, 6],
        [4, 2, 7, 1, 3, 2, 4, 6, 2, 7, 5, 4, 6, 1, 3, 5, 6, 2, 4],
        [7, 3, 5, 4, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ]
    stock = [8, 9, 10, 6, 5, 7, 8]

    for i in range(w):
        for j in range(h):
            v = tile_map[i][j]
            if v != -1:
                tile_map[i][j] -= 1

    full_brute(0, tile_map, stock)
    greedy_pick(h, stock, tile_map)


def greedy_pick(h, stock, tile_map, variant='greedy'):
    for i in [3, 4, 2, 5, 1, 6]:
        for j in range(h):
            v = tile_map[i][j]
            # if i == 2 and 5 <= j <= 9:
            #     stock[v] -= 1
            if v != -1:
                continue

            excluded = [
                get_(tile_map, i + 1, j),
                get_(tile_map, i - 1, j),
                get_(tile_map, i, j + 1),
                get_(tile_map, i, j - 1),
                get_(tile_map, i - 2, j),
                get_(tile_map, i + 2, j),
                get_(tile_map, i, j + 2),
                get_(tile_map, i, j - 2),
                get_(tile_map, i - 1, j - 1),
                get_(tile_map, i - 1, j + 1),
                get_(tile_map, i + 1, j + 1),
                get_(tile_map, i + 1, j - 1),
                get_(tile_map, i, j - 4),
            ]
            for _ in range(2):
                if variant == 'random':
                    possibilities = list(set(range(len(stock))) - set(excluded))
                    v = random.choice(possibilities)
                elif variant == 'greedy':
                    stock_max = 0
                    for si, sv in enumerate(stock):
                        if sv > stock_max and si not in excluded:
                            v, stock_max = si, sv

                if v != -1:
                    break

                # too strict, apply fewer rules
                excluded = excluded[:-1]

            if v == -1:
                continue

            stock[v] -= 1
            tile_map[i][j] = v
    show_tiles(tile_map)
    print('Stock remains', stock)


def get_coord(pos):
    h = 19
    order = [3, 4, 2, 5, 1, 6]
    j = pos % h
    i = pos // h
    if pos >= h * len(order):
        return -1, -1
    return order[i], j


def full_brute(pos, tile_map, stock):
    show_result = pos == 0
    while True:
        i, j = get_coord(pos)
        if i == -1:
            return 1
        v = tile_map[i][j]
        if v == -1:
            break
        pos += 1

    excluded = [
        get_(tile_map, i + 1, j),
        get_(tile_map, i - 1, j),
        get_(tile_map, i, j + 1),
        get_(tile_map, i, j - 1),
        get_(tile_map, i - 2, j),
        get_(tile_map, i + 2, j),
        get_(tile_map, i, j + 2),
        get_(tile_map, i, j - 2),
        get_(tile_map, i - 1, j - 1),
        get_(tile_map, i - 1, j + 1),
        get_(tile_map, i + 1, j + 1),
        get_(tile_map, i + 1, j - 1),
        get_(tile_map, i, j - 4),
    ]
    possibilities = list(set(range(len(stock))) - set(excluded))
    possibilities = sorted(possibilities, key=lambda x: -stock[x])
    for p in possibilities:
        if stock[p] <= 0:
            continue
        # print(f'For {i + 1}:{j} pick {p + 1}')
        stock[p] -= 1
        tile_map[i][j] = p
        r = full_brute(pos + 1, tile_map, stock)
        if r > 0:
            if show_result:
                show_tiles(tile_map)
                print('Stock remains', stock)
            return 1
        # print(f'For {i + 1}:{j} revert {p + 1}')
        stock[p] += 1
        tile_map[i][j] = -1
    return 0


def get_(tile_map, i, j):
    if i < 0 or j < 0:
        return -1
    try:
        return tile_map[i][j]
    except IndexError:
        return -1


def show_tiles(tile_map):
    for i in range(len(tile_map)):
        print(i + 1, ')', '\t'.join(map(lambda x: str(x + 1), tile_map[i])))


if __name__ == '__main__':
    tile_calc()
