#!/usr/bin/env python
#
# Copyright (C) 2014  Johannes Schauer <j.schauer@email.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import io
import zlib
import sunau
import struct
import codecs
import os
from PIL import Image, ImageDraw
import soundfile
import zlib
import pygame
# print(soundfile.available_formats())
# def is_pcx(data):
#     size, width, height = struct.unpack("<III", data[:12])
#     return size == width*height or size == width*height*3
# pygame.mixer.get_init(frequency=22050, size=8, channels=1)
pygame.mixer.init()

# def read_pcx(data):
#     size, width, height = struct.unpack("<III", data[:12])
#     if size == width*height:
#         im = Image.fromstring('P', (width, height), data[12:12+width*height])
#         palette = []
#         for i in range(256):
#             offset = 12+width*height+i*3
#             r, g, b = struct.unpack("<BBB", data[offset:offset+3])
#             palette.extend((r, g, b))
#         im.putpalette(palette)
#         return im
#     elif size == width*height*3:
#         return Image.fromstring('RGB', (width, height), data[12:])
#     else:
#         return None


# def unpack_lod(infile, outdir):
#     f = open(infile, "rb")

#     header = f.read(24)
#     print(header)
#     print(struct.unpack("24s", header))
#     # if header != b'LOD\x00':

#     #     return False

#     f.seek(24)
#     total = struct.unpack("<IIIIIIII", f.read(32))
#     print(total)
#     f.seek(92)

#     files = []

#     for i in range(total):
#         filename, = struct.unpack("16s", f.read(16))
#         filename = filename[:filename.index(b'\0')]
#         offset, size, _, csize = struct.unpack("<IIII", f.read(16))
#         files.append((filename, offset, size, csize))
#     print(files)
#     for filename, offset, size, csize in files:
#         name = codecs.decode(filename, 'utf-8')
#         print(name)
#         print(type(name))
#         filename = os.path.join(outdir, name)

#         f.seek(offset)
#         if csize != 0:
#             data = zlib.decompress(f.read(csize))
#         else:
#             data = f.read(size)
#         if is_pcx(data):
#             im = read_pcx(data)
#             if not im:
#                 return False
#             filename = os.path.splitext(filename)[0]
#             filename = filename+".png"
#             im.save(filename)
#         else:
#             with open(filename, "wb") as o:
#                 o.write(data)

#     return True


# ret = unpack_lod("Heroes3.snd", "./lods")
# print(ret)
# print(sunau.open('Heroes3.au', 'rb'))
file1 = open('Heroes3.snd', "rb")
file2 = open('LOOPCRYS.wav', "rb")
de = file2.read()
# print(de)


def read_int32(reader):
    return struct.unpack('i', reader.read(4))[0]

# Zdefiniuj funkcję do odczytu ciągu znaków o znanej maksymalnej długości.


def read_string(reader, max_length):
    data = reader.read(max_length)
    null_index = data.find(b'\x00')
    if null_index != -1:
        data = data[:null_index]
    return data.decode('utf-8')


file_entries = []
# Otwórz strumień danych.
with open('Heroes3.snd', 'rb') as file:
    # reader = file.read()
    file_count = struct.unpack('I', file.read(4))[0]
    print(file_count)
    # Inicjalizacja pustej listy dla metadanych o plikach.

    for _ in range(file_count):
        # Odczytaj dane z pliku.
        file_name_raw = read_string(file, 40)
        # print(file_name_raw)
        # file_name_and_extension = file_name_raw.split('\x00')[0]
        # print(file_name_and_extension)

        file_offset = read_int32(file)
        size = read_int32(file)
        # print(size)
        # print(file_offset)

        # Dodaj metadane do listy.
        file_entries.append((file_name_raw, file_offset, size))

# print(file_entries)
# print(file_entries[6][1])
print(file_entries)
file1.seek(file_entries[68][1])
data = file1.read(file_entries[68][2])
sound = pygame.mixer.Sound(data)
sound.set_volume(0.1)
# print(data)
s = open("wawka.wav", 'wb+')
# s.write(data)
s.close()
sound2 = pygame.mixer.Sound("LOOPWIND.wav")
pygame.mixer.find_channel().play(sound2, loops=-1)
# print(data)
# with open('Heroes3.snd', 'rb') as file:
#     # Przeczytaj pierwsze cztery bajty
#     header = file.read(4)
# print(struct.unpack('i', file.read(4))[0])
#     print(header)
#     print(struct.unpack('4s', header))
c = input("press  enter to close")
#     # Sprawdź, czy to jest poprawny nagłówek .snd
#     if header == b'.snd':
#         # Jeśli tak, odczytaj resztę danych
#         # Tutaj możesz umieścić kod do odczytu danych dźwiękowych w formacie .snd
#         # Przy użyciu funkcji struct.unpack() i odpowiednich formatów
#         # Na przykład:

#         # Odczytaj kolejne dane jako unsigned integer (4 bajty)
#         data = file.read(4)
#         # '>I' to format dla unsigned integer
#         value = struct.unpack('>I', data)[0]

#         print(f'Wartość: {value}')
#     else:
#         print('To nie jest plik .snd')
