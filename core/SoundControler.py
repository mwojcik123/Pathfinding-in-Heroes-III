import pygame
import asyncio
import codecs
import struct


class SoundControler:
    def __init__(self):
        self.effect_sounds_file = open("Heroes3.snd", "rb")

        self.effect_sounds_file = self._unpack_snd()
        self.now_playing_music = None
        self.music_volume = 0.0
        self.interactive_effect_chanel = pygame.mixer.set_reserved(1)

    def _read_int32(self, reader):
        return struct.unpack('i', reader.read(4))[0]

# Zdefiniuj funkcję do odczytu ciągu znaków o znanej maksymalnej długości.

    def _read_string(self, reader, max_length):
        data = reader.read(max_length)
        null_index = data.find(b'\x00')
        if null_index != -1:
            data = data[:null_index]
        return data.decode('utf-8')

    def _unpack_snd(self):
        file_entries = []
        file = self.effect_sounds_file
        # reader = file.read()
        file_count = struct.unpack('I', file.read(4))[0]
        # print(file_count)
        # Inicjalizacja pustej listy dla metadanych o plikach.

        for _ in range(file_count):
            # Odczytaj dane z pliku.
            file_name_raw = self._read_string(file, 40)
            # print(file_name_raw)
            # file_name_and_extension = file_name_raw.split('\x00')[0]
            # print(file_name_and_extension)

            file_offset = self._read_int32(file)
            size = self._read_int32(file)
            # print(size)
            # print(file_offset)

            # Dodaj metadane do listy.
            file_entries.append((file_name_raw, file_offset, size))
        return file_entries

    def play_interactive_effect(self, effect):
        pygame.mixer.Channel(self.interactive_effect_chanel).play(effect)

    def play_terrain_music(self, effect):
        pygame.mixer.music.play(effect)

    def play_terrain_music(self, effect):
        pygame.mixer.music.play(effect)
