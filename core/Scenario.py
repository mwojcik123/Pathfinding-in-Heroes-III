import json
import pygame

from parsert.AssetsLoader import AssetsLoader
# from layouts.Title import Title
from layouts.Stump import Stump, Title, Road
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)


def sort_objects(e):
    return e.z_index


def sort_extra(lista):
    board = []
    y = 10
    while y != -1:
        x = 0
        while x != 500:

            for i in range(len(lista)):
                # print(i)
                if (lista[i].pos[1] == x and lista[i].above == y):
                    # c = lista.pop(i)
                    board.append(lista[i])
            x = x + 1
        y = y - 1
    # print(board)
    return board


class Scenario:
    def __init__(self, game, file):
        self.game = game
        self.assets_loader = AssetsLoader()
        self.terrain_objects = []
        self.road_maze = []
        self.terrain_maze = self.load_file(file)

        # self.asse = self.assets_loader.get_sprite("AvLStm1.def")
        # print(self.asse.images)
        self.shape = self.load_shape(self.terrain_maze)
        # print(self.shape)

    # def change_no_walk(self, x, y):
    #     for tit in self.terrain_maze:
    #         if (tit.pos[0] == x and tit.pos[1] == y):
    #             tit.can_walk = False

    def terrain_fill(self, pos, passable):
        board = []
        for index, row in enumerate(passable[::-1]):
            start = 255 - row
            # print(start)
            power = 7

            while power != 0:

                if (start - pow(2, power) >= 0):
                    start = start - pow(2, power)
                    # print("123")
                    x = pos[0] - 8 + power+1
                    y = pos[1] - index
                    board.append((x, y))

                power = power - 1

        for tit in self.terrain_maze:
            for obj in board:
                if (tit.pos[0] == obj[0] and tit.pos[1] == obj[1]):
                    tit.can_walk = False
                    # print(tit.pos)

    def load_shape(self, file):

        for obj in self.terrain_objects:
            self.terrain_fill(obj.pos, obj.passable)
            # for gx in obj.passable:
            #     while
        # for tit in self.terrain_maze:
        #     for obj in self.terrain_objects:
        #         if (tit.pos[0] == obj.pos[0] and tit.pos[1] == obj.pos[1]):
        #             tit.can_walk = False
            # tit.change(False)
            # print("es")
        # board = np.zeros((36, 36), dtype=int)
        # for i in file:
        #     if (i.can_walk == False):
        #         board[i.pos[1], i.pos[0]] = 1

        # print(board)
        n = [self.terrain_maze[i:i+36]
             for i in range(0, len(self.terrain_maze), 36)]
        return n
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
        board_objects = []
        board_map = []
        with open(file) as user_file:
            file_contents = user_file.read()

        data = json.loads(file_contents)

        size = data["info"]["mapSize"]
        for i in range(size*size):
            # terrain = i["terrain"]["type"]
            rotate = 0
            rotate_road = 0
            for r in data["tiles"][i]["mirror"]:
                if (r == "TerrainVertical"):
                    rotate += 32

                if (r == "TerrainHorizontal"):
                    rotate += 64

            # road rotation
            for r in data["tiles"][i]["mirror"]:
                if (r == "RoadVertical"):
                    rotate_road += 32

                if (r == "RoadHorizontal"):
                    rotate_road += 64
            road_cost = 1
            sprite = data["tiles"][i]["terrain"]["sprite"]
            sprite_road = data["tiles"][i]["road"]["sprite"]
            type = data["tiles"][i]["terrain"]["type"]
            type_road = data["tiles"][i]["road"]["type"]
            canwalk = True
            if (data["tiles"][i]["road"]["type"] == "Cobble"):
                road_cost = 0.5
            if (data["tiles"][i]["road"]["type"] == "Dirt"):
                road_cost = 0.8
            if (data["tiles"][i]["road"]["type"] == "Gravel"):
                road_cost = 0.65
            cost = 1
            if (data["tiles"][i]["terrain"]["type"] == "Dirt"):
                cost = 1 * road_cost
            if (data["tiles"][i]["terrain"]["type"] == "Grass"):
                cost = 1 * road_cost
            if (data["tiles"][i]["terrain"]["type"] == "Lava"):
                cost = 1.3 * road_cost
            if (data["tiles"][i]["terrain"]["type"] == "Rock"):
                cost = 1.2 * road_cost
            if (data["tiles"][i]["terrain"]["type"] == "Roug"):
                cost = 1.1 * road_cost
            if (data["tiles"][i]["terrain"]["type"] == "Sand"):
                cost = 1.5 * road_cost
            if (data["tiles"][i]["terrain"]["type"] == "Snow"):
                cost = 1.7 * road_cost
            if (data["tiles"][i]["terrain"]["type"] == "Sub"):
                cost = 1.4 * road_cost
            if (data["tiles"][i]["terrain"]["type"] == "Swamp"):
                cost = 1.9 * road_cost
            if (data["tiles"][i]["terrain"]["type"] == "Lava"):
                cost = 1.4 * road_cost

            if (data["tiles"][i]["terrain"]["type"] == "Water"):
                canwalk = False

            if (type_road != "None"):
                vector_road = sprite_road*32
                road = self.game.assets.sprite_road[type_road].image_at(
                    (0+rotate_road, 0+vector_road, 32, 32), pygame.Color(255, 255, 255, 0))
                self.road_maze.append(
                    Road(road, ((i % size), (i // size)), True))
            vector = sprite*32
            terr = self.game.assets.sprite_terrain[type].image_at(
                (0+rotate, 0+vector, 32+rotate, 32+vector))
            board_map.append(
                Title(terr, ((i % size), (i // size)), canwalk, terrain_cost=cost))

        for obj in data["objectDetails"]["entries"]:
            # print(obj["attributes"]["header"])
            # print("ed")
            # if (obj["attributes"]["header"] == "AvLStm1.def"):

            self.terrain_objects.append(self.assets_loader.get_sprite(
                obj["attributes"]["header"], (obj["x"], obj["y"]), obj["attributes"]["landscapeGroup"], obj["attributes"]["above"], obj["attributes"]["passable"], obj["attributes"]["active"]))
        # self.terrain_objects.reverse()
        self.terrain_objects = sort_extra(self.terrain_objects)
        return board_map
        # board = []
