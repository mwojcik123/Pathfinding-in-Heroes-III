

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
