from Units import Unit
import pygame
import time


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, pos=None, image=None,):
        self.image = image
        self.parent = parent
        self.pos = pos

        self.g = 0
        self.h = 0
        self.f = 0

    def __getitem__(self, items):
        return self.pos[items]

    def __repr__(self):
        return "{}".format(self.pos)

    def __eq__(self, other):
        return self.pos == other.pos


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
            "Player", game.assets.Player, 2, 5, 20, [24, 6])
        self.units = []
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
                print("hej")
                time.sleep(0.4)
                self.current_palyer.new_pose([next[1], next[0]])
            else:
                self.IsMove = False

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
        print(maze[end[1]][end[0]])
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
                print(path)
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

                    print(a)
                    print(b)
                    print(c)

                    nextX = (b[1]-c[1])
                    nextY = (b[0]-c[0])

                    beforeX = (b[1]-a[1])
                    beforeY = (b[0]-a[0])

                    # nextY = (b[1]-c[1])
                    print("X {}".format(a[0]))
                    print("X {}".format(c[1]))
                    print("nextX {} nextY {}".format(nextX, nextY))
                    print("beforeX {} beforeY {}".format(beforeX, beforeY))
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
                    # cross

                    # if (nextY == -2) and (beforeY == -2):
                    #     if (nextX == -1) and (beforeX == -1):
                    #         bx = 64
                    #         by = 0
                    #     elif (nextX == 0) and (beforeX == 0):
                    #         bx = 64
                    #         by = 32
                    #     if (nextX == 1) and (beforeX == 1):
                    #         bx = 64
                    #         by = 64
                    #     if (nextX == -2) and (beforeX == -2):
                    #         bx = 96
                    #         by = 32

                    # if (nextX == -2) and (beforeX == -2):
                    #     if (nextY == -1) and (beforeY == -1):
                    #         bx = 128
                    #         by = 64
                    #     elif (nextY == 0) and (beforeY == 0):
                    #         bx = 128
                    #         by = 32
                    #     if (nextY == 1) and (beforeY == 1):
                    #         bx = 128
                    #         by = 0
                    #     if (nextY == 2) and (beforeY == 2):
                    #         bx = 160
                    #         by = 32

                    # if (nextY == 2) and (beforeY == 2):
                    #     if (nextX == -1) and (beforeX == -1):
                    #         bx = 192
                    #         by = 64
                    #     if (nextX == 0) and (beforeX == 0):
                    #         bx = 192
                    #         by = 32
                    #     if (nextX == 1) and (beforeX == 1):
                    #         bx = 192
                    #         by = 0
                        # if (nextX == -2) and (beforeX == -2):
                        #     bx = 96
                        #     by = 32
                        # elif (nextY == 1) and (beforeY == 1):
                        #     bx = 0
                        #     by = 64
                    # if (afterX == 1) and (beforeX == 1):
                    #     bx = 32
                    #     if (afterY == -2) and (beforeY == -2):
                    #         by = 0
                    #     if (afterY == 0) and (beforeY == 0):
                    #         by = 32
                    #     if (afterY == 1) and (beforeY == 1):
                    #         by = 64
                    # elif (beforeX) == -2:
                    #     bx += 0
                    #     if (beforeY) == -1:
                    #         by += 0
                    #     # if (beforeY) == 2:
                    #     #     by += 64
                    #     if (beforeY) == -1:
                    #         by += 64
                    #     if (beforeY) == -2:
                    #         bx += 224
                    #         by += 32
                    #     if (beforeY) == 2:
                    #         bx += 32
                    #         by += 32

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
            print()
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


class ObjectControler:
    def __init__(self, game):
        self.game = game
        self.objects = []

    def attacking(self, attacker, attacked):
        attacked.hp -= attacker.attack
        if (attacked.hp <= 0):
            self.units.remove(attacked)
        print("Unit {} (player {}) attacked Object {} (player {})".format(
            attacker.name, attacker.player, attacked.name, attacked.player))
