import json
from layouts.Title import Title
from layouts.Stump import Stump
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)


class Scenario:
    def __init__(self, game, file):
        self.game = game
        self.terrain_objects = []
        self.terrain_maze = self.load_file(file)
        self.shape = self.load_shape(self.terrain_maze)

    def load_shape(self, file):
        board = np.zeros((36, 36), dtype=int)
        for i in file:
            if (i.can_walk == False):
                board[i.pos[1], i.pos[0]] = 1

        print(board)
        return board
        # with open(file) as user_file:
        #     file_contents = user_file.read()

        # data = json.loads(file_contents)

        # size = data["info"]["mapSize"]
        # for i in range(size*size):
        #     # terrain = i["terrain"]["type"]
        #     rotate = 0
        #     for r in data["tiles"][i]["mirror"]:
        #         if (r == "TerrainVertical"):
        #             rotate += 32

        #         if (r == "TerrainHorizontal"):
        #             rotate += 64

        #     sprite = data["tiles"][i]["terrain"]["sprite"]
        #     type = data["tiles"][i]["terrain"]["type"]
        #     canwalk = True
        #     if (data["tiles"][i]["terrain"]["type"] == "Water"):
        #         canwalk = False

        #     vector = sprite*32
        #     terr = self.game.assets.sprite_data[type].image_at(
        #         (0+rotate, 0+vector, 32+rotate, 32+vector))
        #     board.append(
        #         Title(terr, ((i % size), (i // size)), canwalk))
        # return board

    def load_file(self, file):
        board = []
        with open(file) as user_file:
            file_contents = user_file.read()

        data = json.loads(file_contents)

        size = data["info"]["mapSize"]
        for i in range(size*size):
            # terrain = i["terrain"]["type"]
            rotate = 0
            for r in data["tiles"][i]["mirror"]:
                if (r == "TerrainVertical"):
                    rotate += 32

                if (r == "TerrainHorizontal"):
                    rotate += 64

            sprite = data["tiles"][i]["terrain"]["sprite"]
            type = data["tiles"][i]["terrain"]["type"]
            canwalk = True
            if (data["tiles"][i]["terrain"]["type"] == "Water"):
                canwalk = False

            vector = sprite*32
            terr = self.game.assets.sprite_data[type].image_at(
                (0+rotate, 0+vector, 32+rotate, 32+vector))
            board.append(
                Title(terr, ((i % size), (i // size)), canwalk))

        for obj in data["objectDetails"]["entries"]:
            # print(obj["attributes"]["header"])
            # print("ed")
            if (obj["attributes"]["header"] == "AvLStm1.def"):
                board.append(Stump(self.game.assets.stump,
                             [obj["x"], obj["y"]], False))
                self.terrain_objects.append(
                    Stump(self.game.assets.stump, [obj["x"], obj["y"]], False))
        return board
        # board = []
