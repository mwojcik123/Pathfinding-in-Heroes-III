from Controler import PlayerControler, ObjectControler
from Assets import Assets
from core.Scenario import Scenario
import pygame
from ex1 import astar
from itertools import cycle
# class Disease:
#     def __init__(self, name, progress=0):
#         self.name = name

#         self.progress = progress

#     def grow_progress(self):
#         self.progress += 1
#         self.name.hp -= 1
#         print(self.progress)

#     def decrease_progress(self):
#         self.progress -= 1
#         self.name.hp += 1

#         print(self.progress)


class Game:
    def __init__(self, screen, timer):
        self.screen = screen
        self.timer = timer
        self.assets = Assets()

        self.units_controler = PlayerControler(self)
        self.objects_controler = ObjectControler(self)
        self.scenario = Scenario(self, "test.json")
        print(self.assets.skeleton_images_list)

        self.tick_time = pygame.time.get_ticks()
        self.skl = cycle(self.assets.skeleton_images_list)
        self.now_cycle = next(cycle(self.assets.skeleton_images_list))

        # self.path = self.units_controler.astar(self.scenario.shape,
        #                                        (self.units_controler.current_palyer.pos[1], self.units_controler.current_palyer.pos[0]), (4, 6))
        # print(self.path)

    def find_path(self, pos):
        self.units_controler.astar(self.scenario.shape,
                                   (self.units_controler.current_palyer.pos[1], self.units_controler.current_palyer.pos[0]), pos)

    def Run(self):
        # print(pygame.time.get_ticks())

        self.units_controler.move()
        # for e in self.path:
        #     self.screen.blit(self.units_controler.current_palyer.image,
        #                      (e[0]*32, e[1]*32))
        for i in self.scenario.terrain_maze:
            self.screen.blit(i.image, (i.pos[0] * 32, i.pos[1] * 32))

        for i in self.scenario.terrain_objects:
            self.screen.blit(i.image, (i.pos[0] * 32, i.pos[1] * 32))

        self.screen.blit(self.units_controler.current_palyer.image,
                         (self.units_controler.current_palyer.pos[0]*32-32, self.units_controler.current_palyer.pos[1]*32-32))

        if (pygame.time.get_ticks() - self.tick_time > 200):
            self.tick_time = pygame.time.get_ticks()
            self.now_cycle = next(cycle(self.skl))

        self.screen.blit(self.now_cycle,
                         (192, 192))

        for e in self.units_controler.path:
            if (e.image):
                self.screen.blit(e.image,
                                 (e[1]*32, e[0]*32))
    # def get_status(self):
    #     return self.hp


pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True
game = Game(screen, clock)


while running:
    game.Run()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            xy = pygame.mouse.get_pos()
            print(xy[0]//32)
            game.find_path((xy[1]//32, xy[0]//32))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()


units = game.units_controler.units
print(units)
# game.units_controler.attacking(units[0], units[1])
# game.units_controler.attacking(units[0], units[1])
# game.units_controler.attacking(units[0], units[1])
# game.units_controler.attacking(units[0], units[1])

units = game.units_controler.units
# print(units)
# print(game.scenario.terrain_maze)
# class Dog(Animal):
#     def __init__(self, name, say, master, color):
#         super().__init__(name, say,  master)
#         self.color = color

#     def bark(self):
#         print("{} {} say {}!".format(self.name, self.color, self.say))
