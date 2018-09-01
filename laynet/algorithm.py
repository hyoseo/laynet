def run():
    K = 5
    roomInputs = [1, 2, 3, 6, 5, 4, 4, 2, 5, 3, 6, 1, 6, 5, 3, 2, 4, 1, 2, 5, 1, 4, 3, 6, 8, 4, 3, 1, 5, 6, 2]
    rooms = dict()

    for v in roomInputs:
        if v in rooms.keys():
            rooms[v] += 1
        else:
            rooms[v] = 1

    for k, v in rooms.items():
        if v == 1:
            print(v)
