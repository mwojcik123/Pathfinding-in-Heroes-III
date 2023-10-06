from Units import Unit
import pygame
import time


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, pos=None, image=None, cost=0):
        self.image = image
        self.parent = parent
        self.pos = pos
        self.cost = cost
        self.g = 0
        self.h = 0
        self.f = 0

    def __getitem__(self, items):
        return self.pos[items]

    def __repr__(self):
        return "<{}>".format(self.pos)

    def __eq__(self, other):
        return self.pos == other.pos

    def __le__(self, other):
        if (self.get_cost() <= other.get_cost()):
            return self
        else:
            return other

    def get_cost(self):
        suma = self.cost
        parent = self.parent
        while parent is not None:
            suma += parent.cost
            parent = parent.parent
        return suma


class Path():
    def __init__(self, image=None, pos=None):
        self.image = image
        self.pos = pos

    def __getitem__(self, items):
        return self.pos[items]

    def __repr__(self):
        return "{}".format(self.pos)


class PlayerControler:
    def __init__(self, game):
        self.game = game
        self.cursor_pos = None
        self.IsMove = False
        self.path = []
        self.current_objects = None
        self.current_palyer = Unit(
            "Player", game.assets.Player, 2, 5, 20, [17, 6])
        self.units = []
        self.avilable_path = []
        # self.units.append(Unit("vilager", 1, 5, 20, [3, 3]))
        # self.units.append(Unit("vilager", 2, 5, 20, [1, 1]))

    def attacking(self, attacker, attacked):
        attacked.hp -= attacker.attack
        if (attacked.hp <= 0):
            self.units.remove(attacked)
        print("Unit {} (palyer {}) attacked Unit {} (palyer {})".format(
            attacker.name, attacker.player, attacked.name, attacked.player))

    def move(self):
        if (self.IsMove):
            if (self.path != []):
                # g = self.path
                next = self.path.pop()
                # print("hej")

                self.current_palyer.new_pose([next[1], next[0]])
                time.sleep(0.1)
            else:
                self.IsMove = False
                self.avilable_maze(
                    self.game.scenario.shape, (self.current_palyer.pos[0], self.current_palyer.pos[1]))

    def wypisz_powtorzenia(self):
        powtorzenia = {}
        for element in self.path:
            if self.path.count(element) > 1:
                powtorzenia[element] = self.path.count(element)

        for element, ilosc_powtorzen in powtorzenia.items():
            print(f"{element} występuje {ilosc_powtorzen} razy")

    def conflict(self, node, avilable_terrain):
        for avilable in avilable_terrain:
            if (node == avilable):
                if (node.get_cost() < avilable.get_cost()):
                    return node
                else:
                    return False

    def avilable_maze(self, maze, start):
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0

        # isFind = True
        avilable_terrain = []
        new_check_terrain = []
        new_check_terrain.append(start_node)

        while len(new_check_terrain) > 0:
            # for loop_count in range(8):
            child = []
            # print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
            for index, item in enumerate(new_check_terrain):
                # print(item)
                # print(index)
                # if (maze[item[1]][item[0]] == 0):
                avilable_terrain.append(item)
                child.append(item)

                # else:
                #     new_check_terrain.pop(index)
            # print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
            new_check_terrain = []
            # print(maze[6, 24])
            # print(new_check_terrain)
            # print("avil")
            # print(avilable_terrain)
            next_array = []
            array_for_conflict = []
            for node in child:
                for new_pos in [(0, -1, 100), (0, 1, 100), (-1, 0, 100), (1, 0, 100), (-1, -1, 144), (-1, 1, 144), (1, -1, 144), (1, 1, 144)]:

                    # Get node pos
                    node_pos = (
                        node.pos[0] + new_pos[0], node.pos[1] + new_pos[1])

                    # Make sure within range
                    if node_pos[0] > (len(maze) - 1) or node_pos[0] < 0 or node_pos[1] > (len(maze[len(maze)-1]) - 1) or node_pos[1] < 0:
                        continue

                    # Make sure walkable terrain
                    if maze[node_pos[1]][node_pos[0]].can_walk == False:
                        continue
                    # print(maze[node_pos[1]][node_pos[0]].terrain_cost)
                    cost = maze[node_pos[1]][node_pos[0]
                                             ].terrain_cost*new_pos[2]
                    # Create new node
                    new_node = Node(
                        node, node_pos, cost=cost)
                    if (new_node in avilable_terrain):
                        array_for_conflict.append(new_node)
                        continue

                    next_array.append(new_node)

            # second_array = []
            remove_array = []
            for n in array_for_conflict:
                for avilable in avilable_terrain:
                    if (n == avilable):
                        if (n.get_cost() < avilable.get_cost()):
                            next_array.append(n)
                            remove_array.append(avilable)
                        else:
                            continue
            # print(remove_array)
            for rem in remove_array:
                for debil in avilable_terrain:
                    if (rem == debil):
                        avilable_terrain.remove(debil)
            # print(rem)
            # avilable_terrain = list(set(avilable_terrain)-set(fuk_array))
            # result = []
            # for gupi_el in avilable_terrain:
            #     if (gupi_el in fuk_array):
            #         continue
            #     else:
            #         result.append(gupi_el)
            # avilable_terrain = result
            # print(next_array)
            # print(next_array)
            # unique_objects = {}
            # for obj in next_array:

            #     if obj.pos not in unique_objects:
            #         # print(obj.get_cost())

            #         unique_objects[obj.pos] = obj
            #     else:
            #         if (obj.get_cost() > unique_objects[obj.pos].get_cost()):
            #             unique_objects[obj.pos] = obj
            #         # print(unique_objects[obj.pos].get_cost())
            # second_array = list(unique_objects.values())
            # print(next_array)
            # print(new_check_terrain)
            # print("ugie")
            # print(avilable_terrain)
            # print("bugie")
            filtered_nodes = {}

            for node in next_array:
                pos = node.pos
                cost = node.get_cost()

                if pos not in filtered_nodes:
                    filtered_nodes[pos] = node
                else:
                    existing_node = filtered_nodes[pos]
                    if cost <= existing_node.get_cost():
                        filtered_nodes[pos] = node

            # new_check_terrain = next_array

            new_check_terrain = list(filtered_nodes.values())
            # print(new_check_terrain)
            # for r in next_array:
            #     if (r in avilable_terrain):
            #         continue
            #     x = r
            #     for secondd in second_array:
            #         if (r == secondd):
            #             x = x <= secondd
            #     second_array.append(x)
            # else:
            #     second_array.append(r)

            # print(avilable_terrain)
            # for ind, s in enumerate(next_array):
            #     for g in avilable_terrain:
            #         if (s == g):
            #             print("<{} {}>".format(s, g))
            #             # next_array.pop(ind)
            #             continue
            #         else:
            #             second_array.append(s)
            # second_array.append(s)

            # print(second_array)

            # new_check_terrain = next_array
            # print(new_check_terrain)
            # print(second_array)
            # s = second_array

        self.avilable_path = avilable_terrain[::-1]
        # print(self.avilable_path)

    def astar(self, maze, start, end):
        if (self.IsMove == True):
            self.IsMove = False
            return 0
        else:
            if (self.cursor_pos == end):
                self.IsMove = True
            else:
                self.cursor_pos = end
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""
        # check if no walk
        # print(maze[end[1]][end[0]])
        if (maze[end[0]][end[1]] == 1):
            return 0

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    # x1 = current.pos[0]
                    # y1 = current.pos[1]
                    # if (current.parent):
                    # x2 = current.parent.pos[0]
                    # y2 = current.parent.pos[1]
                    # x2 = current.parent.pos[0]
                    # y2 = current.parent.pos[1]
                    # print(x1-x2)
                    # print(y1-y2)
                    # if(current.parent.pos)
                    # current.image = self.game.assets.arrow.image_at(
                    #     (0, 0, 32, 32), pygame.Color(0, 0, 0, 0))
                    path.append(current.pos)
                    current = current.parent
                # print(path)
                off_path = []
                last = path[0]
                last_cursor_image = self.game.assets.arrow.image_at(
                    (0, 192, 32, 32), pygame.Color(0, 255, 255))
                off_path.append(Path(last_cursor_image, (last[0], last[1])))
                for x in range(1, len(path)-1):
                    # print(x)
                    a = path[x-1]
                    b = path[x]
                    c = path[x+1]

                    # print(a)
                    # print(b)
                    # print(c)

                    nextX = (b[1]-c[1])
                    nextY = (b[0]-c[0])

                    beforeX = (b[1]-a[1])
                    beforeY = (b[0]-a[0])

                    # nextY = (b[1]-c[1])
                    # print("X {}".format(a[0]))
                    # print("X {}".format(c[1]))
                    # print("nextX {} nextY {}".format(nextX, nextY))
                    # print("beforeX {} beforeY {}".format(beforeX, beforeY))
                    bx = 0
                    by = 0
                    # if (beforeX) == -2:
                    #     bx += 0
                    # if (beforeX) == 0:
                    #     bx += 196
                    # if (beforeX) == 2:
                    #     bx += 128
                    # woloio
                    if (beforeX == -1) and (beforeY == 0):
                        if (nextX == 1) and (nextY == 0):
                            bx = 64
                            by = 32
                        elif (nextX == 1) and (nextY == -1):
                            bx = 64
                            by = 64
                        elif (nextX == 1) and (nextY == 1):
                            bx = 64
                            by = 0

                    if (beforeX == 0) and (beforeY == 1):
                        if (nextX == 0) and (nextY == -1):
                            bx = 0
                            by = 32
                        elif (nextX == -1) and (nextY == -1):
                            bx = 0
                            by = 64
                        elif (nextX == 1) and (nextY == -1):
                            bx = 0
                            by = 0

                    if (beforeX == 0) and (beforeY == -1):
                        if (nextX == 0) and (nextY == 1):
                            bx = 128
                            by = 32
                        elif (nextX == 1) and (nextY == 1):
                            bx = 128
                            by = 64
                        elif (nextX == -1) and (nextY == 1):
                            bx = 128
                            by = 0

                    if (beforeX == 1) and (beforeY == 0):
                        if (nextX == -1) and (nextY == 0):
                            bx = 192
                            by = 32
                        elif (nextX == -1) and (nextY == -1):
                            bx = 192
                            by = 0
                        elif (nextX == -1) and (nextY == 1):
                            bx = 192
                            by = 64

                    if (beforeX == -1) and (beforeY == -1):
                        if (nextX == 0) and (nextY == 1):
                            bx = 96
                            by = 0
                        elif (nextX == 1) and (nextY == 1):
                            bx = 96
                            by = 32
                        elif (nextX == 1) and (nextY == 0):
                            bx = 96
                            by = 64
                        elif (nextX == 1) and (nextY == -1):
                            bx = 96
                            by = 64
                        elif (nextX == -1) and (nextY == 1):
                            bx = 96
                            by = 0

                    if (beforeX == -1) and (beforeY == 1):
                        if (nextX == 0) and (nextY == 1):
                            bx = 32
                            by = 0
                        elif (nextX == 1) and (nextY == -1):
                            bx = 32
                            by = 32
                        elif (nextX == 1) and (nextY == 0):
                            bx = 32
                            by = 0
                        elif (nextX == 0) and (nextY == -1):
                            bx = 32
                            by = 64
                        elif (nextX == 1) and (nextY == 1):
                            bx = 32
                            by = 0
                        elif (nextX == -1) and (nextY == -1):
                            bx = 32
                            by = 64
                    if (beforeX == 1) and (beforeY == -1):
                        if (nextX == -1) and (nextY == 1):
                            bx = 160
                            by = 32

                        elif (nextX == -1) and (nextY == -1):
                            bx = 160
                            by = 0
                        elif (nextX == 1) and (nextY == -1):
                            bx = 160
                            by = 32
                        elif (nextX == 1) and (nextY == 0):
                            bx = 160
                            by = 64
                        elif (nextX == -1) and (nextY == 0):
                            bx = 160
                            by = 0
                        elif (nextX == 0) and (nextY == 1):
                            bx = 160
                            by = 64
                        # elif (nextX == 1) and (nextY == 1):
                        #     bx = 160
                        #     by = 0
                        elif (nextX == 1) and (nextY == 1):
                            bx = 160
                            by = 64

                    if (beforeX == 1) and (beforeY == 1):
                        if (nextX == -1) and (nextY == 0):
                            bx = 224
                            by = 64
                        elif (nextX == -1) and (nextY == -1):
                            bx = 224
                            by = 32
                        elif (nextX == -1) and (nextY == 1):
                            bx = 224
                            by = 64
                        elif (nextX == 0) and (nextY == -1):
                            bx = 224
                            by = 0

                    img = self.game.assets.arrow.image_at(
                        (0+bx, 0+by, 32, 32), pygame.Color(0, 255, 255))
                    off_path.append(Path(img, b))

                self.path = off_path
                return off_path[::-1]
                # current.image = self.game.assets.arrow.image_at(
                #     (0, 0, 32, 32), pygame.Color(0, 0, 0, 0))
                # print(a[1]-b[1]+b[1]-c[1])
                # print(path[x])

                # return path[::-1]  # Return reversed path

            # Generate children
            children = []
            # Adjacent squares
            for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

                # Get node pos
                node_pos = (
                    current_node.pos[0] + new_pos[0], current_node.pos[1] + new_pos[1])

                # Make sure within range
                if node_pos[0] > (len(maze) - 1) or node_pos[0] < 0 or node_pos[1] > (len(maze[len(maze)-1]) - 1) or node_pos[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_pos[0]][node_pos[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_pos)

                # Append
                children.append(new_node)

            # Loop through children
            # print()
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.pos[0] - end_node.pos[0]) **
                           2) + ((child.pos[1] - end_node.pos[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

    def astarv2(self, maze, end):
        if (self.IsMove == True):
            self.IsMove = False
            self.avilable_maze(
                self.game.scenario.shape, (self.current_palyer.pos[0], self.current_palyer.pos[1]))
            return 0
        else:
            if (self.cursor_pos == end):
                self.IsMove = True
            else:
                self.cursor_pos = end
        # print(end)
        for title in self.avilable_path:
            # print(title)
            if (end[0] == title[1] and end[1] == title[0]):
                path = []
                current = title
                # print("sdsd")
                # print("sdsd")
                while current is not None:
                    # x1 = current.pos[0]
                    # y1 = current.pos[1]
                    # if (current.parent):
                    # x2 = current.parent.pos[0]
                    # y2 = current.parent.pos[1]
                    # x2 = current.parent.pos[0]
                    # y2 = current.parent.pos[1]
                    # print(x1-x2)
                    # print(y1-y2)
                    # if(current.parent.pos)
                    # current.image = self.game.assets.arrow.image_at(
                    #     (0, 0, 32, 32), pygame.Color(0, 0, 0, 0))
                    path.append(current.pos)
                    current = current.parent
                off_path = []
                last = path[0]
                last_cursor_image = self.game.assets.arrow.image_at(
                    (0, 192, 32, 32), pygame.Color(0, 255, 255))
                off_path.append(Path(last_cursor_image, (last[1], last[0])))
                for x in range(1, len(path)-1):
                    # print(x)
                    a = path[x-1]
                    b = path[x]
                    c = path[x+1]

                    # print(a)
                    # print(b)
                    # print(c)

                    nextX = (b[1]-c[1])
                    nextY = (b[0]-c[0])

                    beforeX = (b[1]-a[1])
                    beforeY = (b[0]-a[0])

                    # nextY = (b[1]-c[1])
                    # print("X {}".format(a[0]))
                    # print("X {}".format(c[1]))
                    # print("nextX {} nextY {}".format(nextX, nextY))
                    # print("beforeX {} beforeY {}".format(beforeX, beforeY))
                    bx = 0
                    by = 0
                    # if (beforeX) == -2:
                    #     bx += 0
                    # if (beforeX) == 0:
                    #     bx += 196
                    # if (beforeX) == 2:
                    #     bx += 128
                    # woloio
                    if (beforeX == -1) and (beforeY == 0):
                        if (nextX == 1) and (nextY == 0):
                            bx = 64
                            by = 32
                        elif (nextX == 1) and (nextY == -1):
                            bx = 64
                            by = 64
                        elif (nextX == 1) and (nextY == 1):
                            bx = 64
                            by = 0

                    if (beforeX == 0) and (beforeY == 1):
                        if (nextX == 0) and (nextY == -1):
                            bx = 0
                            by = 32
                        elif (nextX == -1) and (nextY == -1):
                            bx = 0
                            by = 64
                        elif (nextX == 1) and (nextY == -1):
                            bx = 0
                            by = 0

                    if (beforeX == 0) and (beforeY == -1):
                        if (nextX == 0) and (nextY == 1):
                            bx = 128
                            by = 32
                        elif (nextX == 1) and (nextY == 1):
                            bx = 128
                            by = 64
                        elif (nextX == -1) and (nextY == 1):
                            bx = 128
                            by = 0

                    if (beforeX == 1) and (beforeY == 0):
                        if (nextX == -1) and (nextY == 0):
                            bx = 192
                            by = 32
                        elif (nextX == -1) and (nextY == -1):
                            bx = 192
                            by = 0
                        elif (nextX == -1) and (nextY == 1):
                            bx = 192
                            by = 64

                    if (beforeX == -1) and (beforeY == -1):
                        if (nextX == 0) and (nextY == 1):
                            bx = 96
                            by = 0
                        elif (nextX == 1) and (nextY == 1):
                            bx = 96
                            by = 32
                        elif (nextX == 1) and (nextY == 0):
                            bx = 96
                            by = 64
                        elif (nextX == 1) and (nextY == -1):
                            bx = 96
                            by = 64
                        elif (nextX == -1) and (nextY == 1):
                            bx = 96
                            by = 0

                    if (beforeX == -1) and (beforeY == 1):
                        if (nextX == 0) and (nextY == 1):
                            bx = 32
                            by = 0
                        elif (nextX == 1) and (nextY == -1):
                            bx = 32
                            by = 32
                        elif (nextX == 1) and (nextY == 0):
                            bx = 32
                            by = 0
                        elif (nextX == 0) and (nextY == -1):
                            bx = 32
                            by = 64
                        elif (nextX == 1) and (nextY == 1):
                            bx = 32
                            by = 0
                        elif (nextX == -1) and (nextY == -1):
                            bx = 32
                            by = 64
                    if (beforeX == 1) and (beforeY == -1):
                        if (nextX == -1) and (nextY == 1):
                            bx = 160
                            by = 32

                        elif (nextX == -1) and (nextY == -1):
                            bx = 160
                            by = 0
                        elif (nextX == 1) and (nextY == -1):
                            bx = 160
                            by = 32
                        elif (nextX == 1) and (nextY == 0):
                            bx = 160
                            by = 64
                        elif (nextX == -1) and (nextY == 0):
                            bx = 160
                            by = 0
                        elif (nextX == 0) and (nextY == 1):
                            bx = 160
                            by = 64
                        # elif (nextX == 1) and (nextY == 1):
                        #     bx = 160
                        #     by = 0
                        elif (nextX == 1) and (nextY == 1):
                            bx = 160
                            by = 64

                    if (beforeX == 1) and (beforeY == 1):
                        if (nextX == -1) and (nextY == 0):
                            bx = 224
                            by = 64
                        elif (nextX == -1) and (nextY == -1):
                            bx = 224
                            by = 32
                        elif (nextX == -1) and (nextY == 1):
                            bx = 224
                            by = 64
                        elif (nextX == 0) and (nextY == -1):
                            bx = 224
                            by = 0

                    img = self.game.assets.arrow.image_at(
                        (0+bx, 0+by, 32, 32), pygame.Color(0, 255, 255))
                    off_path.append(Path(img, (b[1], b[0])))

                self.path = off_path
                return off_path[::-1]
                # return path
        return None


class ObjectControler:
    def __init__(self, game):
        self.game = game
        self.objects = []

    def attacking(self, attacker, attacked):
        attacked.hp -= attacker.attack
        if (attacked.hp <= 0):
            self.units.remove(attacked)
        # print("Unit {} (player {}) attacked Object {} (player {})".format(
        #     attacker.name, attacker.player, attacked.name, attacked.player))
