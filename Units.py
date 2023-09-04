class Unit:
    def __init__(self, name, image, player, attack, full_hp, pos):
        self.full_hp = full_hp
        self.image = image
        self.player = player
        self.hp = full_hp
        self.name = name
        self.attack = attack
        self.pos = pos

    def new_pose(self, pos):
        self.pos = pos

    def __repr__(self) -> str:
        return "{} Player {}".format(self.name, self.player)


class Object:
    def __init__(self, name, shape, player, hp, pos):
        self.name = name
        self.hp = hp
        self.shape = shape
        self.player = player
        self.pos = pos

    def __repr__(self) -> str:
        return "{} Player {}".format(self.name, self.player)


# class PlayerObject(Object):
#     def __init__(self, name, shape, player):
#         super().__init__(name, shape, player)
