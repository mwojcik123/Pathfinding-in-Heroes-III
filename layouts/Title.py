class Title:
    def __init__(self, image, pos, can_walk, terrain_cost=1):
        self.image = image
        self.pos = pos
        self.can_walk = can_walk
        terrain_cost = terrain_cost

    # def change(self, bol):
    #     self.can_walk = bol

    def __getitem__(self):
        if (self.can_walk == True):
            return 0
        else:
            return 1

    def __repr__(self):

        return "3"

    def __eq__(self, other):
        return self.pos == other.pos
