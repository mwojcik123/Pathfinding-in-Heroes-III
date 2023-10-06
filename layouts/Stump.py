class Object1:
    def __init__(self, image, pos, can_walk):
        self.image = image
        self.pos = pos
        self.can_walk = can_walk

    def __eq__(self, other):
        return self.pos == other.pos


class Stump(Object1):
    def __init__(self, image, pos, can_walk):
        super().__init__(image, pos, can_walk)


class Road(Object1):
    def __init__(self, image, pos, can_walk):
        super().__init__(image, pos, can_walk)


class Title(Object1):
    def __init__(self, image, pos, can_walk, terrain_cost=1):
        super().__init__(image, pos, can_walk)
        self.terrain_cost = terrain_cost

    def __getitem__(self):
        if (self.can_walk == True):
            return 0
        else:
            return 1

    def __repr__(self):

        return "3"


stump = Stump(3, (3, 3), True)
title = Stump(2, (3, 3), False)

if (stump == title):
    print("ruwne")
