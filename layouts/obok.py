class Object1:
    def __init__(self, image, pos, can_walk):
        self.image = image
        self.pos = pos
        self.can_walk = can_walk

    def __eq__(self, other):
        return self.pos == other.pos
