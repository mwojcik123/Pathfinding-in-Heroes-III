
# import required module
import pygame
import struct
# import winsound
# while True:
# debil = winsound
# winsound.PlaySound("LOOPDEVL.wav", winsound.SND_ASYNC+winsound.SND_LOOP)
# winsound.Beep(32767, 2000)
# from playsound import playsound
# c = input("press  enter to close")
# # for playing note.wav file
# playsound('/path/note.wav')
# print('playing sound using  playsound')
# crash_sound = pygame.mixer.Sound("LOOPDEVL.wav")
pygame.mixer.init()
# print(pygame.mixer.get_num_channels())
# pygame.mixer.music.load('SWAMP.MP3')
# pygame.mixer.music.play()
# pygame.mixer.music.set_volume(0.9)
# g = pygame.mixer.set_reserved(1)
# x = pygame.mixer.Sound('LOOPDEVL.wav')
# y = pygame.mixer.Sound('LOOPSTAR.wav')
# z = pygame.mixer.Sound('HORSE00.wav')
# a = pygame.mixer.Sound('LOOPBIRD.wav')
# b = pygame.mixer.Sound('LOOPWIND.wav')
# c = pygame.mixer.Sound('LOOPSANC.wav')
# x.set_volume(0.1)
# y.set_volume(0.1)
# z.set_volume(0.1)
# pygame.mixer.Channel(0).play(x, loops=-1)
# print(pygame.mixer.Channel(g).play(z, loops=-1))
# pygame.mixer.find_channel().play(x, loops=-1)
# pygame.mixer.find_channel().play(y, loops=-1)
# pygame.mixer.find_channel().play(a, loops=-1)
# pygame.mixer.find_channel().play(b, loops=-1)
# pygame.mixer.find_channel().play(c, loops=-1)
# pygame.mixer.find_channel().play(c, loops=-1)

# print(pygame.mixer.find_channel())
# pygame.mixer.get_busy()

# print(pygame.mixer.Channel(g).play(z, loops=-1))
# print(g)
# g.play(z, loops=-1)

# print(pygame.mixer.get_busy())
# c = input("press  enter to close")

r = open("gwno.msg", "rb")
print(r)
print(struct.unpack("III", r.read(12)))
