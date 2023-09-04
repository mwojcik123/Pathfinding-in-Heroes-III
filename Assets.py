from layouts.Spritesheet import spritesheet
import pygame
import os


class Assets:
    def __init__(self):
        self.terr_00 = spritesheet("./test/terrain/terr_00.jpg")
        self.terr_01 = spritesheet("./test/terrain/terr_01.jpg")
        self.terr_02 = spritesheet("./test/terrain/terr_02.jpg")
        self.terr_03 = spritesheet("./test/terrain/terr_03.jpg")
        self.terr_04 = spritesheet("./test/terrain/terr_04.jpg")
        self.terr_05 = spritesheet("./test/terrain/terr_05.jpg")
        self.terr_06 = spritesheet("./test/terrain/terr_06.jpg")
        self.terr_07 = spritesheet("./test/terrain/terr_07.jpg")
        self.terr_08 = spritesheet("./test/terrain/terr_08.jpg")
        self.terr_09 = spritesheet("./test/terrain/terr_09.jpg")

        self.skeleton = spritesheet("./test/objects/creatures/avwskel0.png")
        self.skeleton_images_list = self.skeleton.load_strip(
            (0, 0, 64, 64), 30, pygame.Color(0, 0, 0, 0))

        self.arrow = spritesheet("./test/ui/sprites/patharrow.png")

        self.stump = pygame.image.load(os.path.join(
            'test', "objects", 'avlstm1.png'))

        self.arrow2 = pygame.image.load(os.path.join(
            'test', "ui", "sprites", 'patharrow.png'))

        self.Player = pygame.image.load(os.path.join(
            'test', "objects", "heroes", 'ah01_e.png'))
        self.sprite_data = {
            "Dirt": self.terr_00,
            "Grass": self.terr_02,
            "Lava": self.terr_07,
            "Rock": self.terr_09,
            "Rough": self.terr_05,
            "Sand": self.terr_01,
            "Snow": self.terr_03,
            "Sub": self.terr_06,
            "Swamp": self.terr_04,
            "Water": self.terr_08,
        }
