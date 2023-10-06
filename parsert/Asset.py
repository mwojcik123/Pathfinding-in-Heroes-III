import base64
from PIL import Image
import io
import os
import struct
import json
from collections import defaultdict
import numpy as np
import pygame
from itertools import cycle
import random


class Asset:
    def __init__(self, byte_file, pos, z_index, above, passable, active):
        self.pos = pos
        self.z_index = z_index
        self.above = above
        self.passable = passable
        self.active = active
        self.time = pygame.time.get_ticks()
        self.images = cycle(self.extract_def(byte_file))
        self.ima = next(self.images)
        # self.extract_def(byte_file)
        # self.images = []
        # self.image_list = images

    def get_blit_pos(self, w, h, lm, tm):
        # print(tm, lm)
        lef = (self.pos[0] * 32 - (w - 32))
        top = (self.pos[1] * 32 - (h - 32))
        # print([lef, top])
        self.blit_pos = [lef, top]

    def draw(self, screen):
        if (pygame.time.get_ticks() - self.time > 200):
            self.time = pygame.time.get_ticks()
            self.ima = next(self.images)
        screen.blit(self.ima, self.blit_pos)

    def extract_def(self, infile, outdir="./out"):
        # io.BufferedReader
        f = io.BytesIO(infile)
        # bn = os.path.basename(infile)
        # bn = os.path.splitext(bn)[0].lower()

        # t - type
        # blocks - # of blocks
        # the second and third entry are width and height which are not used
        # print(f.read(16))
        t, x, y, blocks = struct.unpack("<IIII", f.read(16))
        # print(t)
        # print(x)
        # print(y)
        # print(blocks)
        palette = []
        images = []
        for i in range(256):
            r, g, b = struct.unpack("<BBB", f.read(3))
            palette.extend((r, g, b))

        offsets = defaultdict(list)
        for i in range(blocks):
            # bid - block id
            # entries - number of images in this block
            # the third and fourth entry have unknown meaning
            bid, entries, no1, no2 = struct.unpack("<IIII", f.read(16))
            # print(bid)
            # print(entries)
            # print(no1)
            # print(no2)

            names = []
            # a list of 13 character long filenames
            cont = 0
            for j in range(entries):
                cont += 1
                g = f.read(13)

                # print(g)
                name = struct.unpack("13s", g)
            # a list of offsets
            for j in range(entries):
                offs, = struct.unpack("<I", f.read(4))
                offsets[bid].append(offs)

        # outpath = os.path.join(outdir, "%s.dir" % bn)
        # if os.path.exists(outpath):
        #     if not os.path.isdir(outpath):
        #         print("output path exists and is no directory")
        #         return False
        # else:
        #     os.mkdir(outpath)

        out_json = {"sequences": [], "type": t, "format": -1}

        firstfw, firstfh = -1, -1
        for bid, l in offsets.items():
            # print("SSS")
            # print(bid, l)
            # print("SSS")
            frames = []
            for j, offs in enumerate(l):
                f.seek(offs)
                pixeldata = bytearray()
                # first entry is the size which is unused
                # fmt - encoding format of image data
                # fw,fh - full width and height
                # w,h - width and height, w must be a multiple of 16
                # lm,tm - left and top margin
                _, fmt, fw, fh, w, h, lm, tm = struct.unpack(

                    "<IIIIIIii", f.read(32))
                # print(fmt, fw, fh, w, h, lm, tm)
                self.get_blit_pos(w, fh, lm, tm)
                # outname = os.path.join(outdir, "%s.dir" %
                #                        bn, "%02d_%02d.png" % (bid, j))
                # print("writing to %s" % outname)

                # SGTWMTA.def and SGTWMTB.def fail here
                # they have inconsistent left and top margins
                # they seem to be unused
                if lm > fw or tm > fh:
                    # print"margins (%dx%d) are higher than dimensions (%dx%d)"%(lm,tm,fw,fh)
                    return False

                if firstfw == -1 and firstfh == -1:
                    firstfw = fw
                    firstfh = fh
                else:
                    if firstfw > fw:
                        # print "must enlarge width"
                        fw = firstfw
                    if firstfw < fw:
                        # print "first with smaller than latter one"
                        return False
                    if firstfh > fh:
                        # print "must enlarge height"
                        fh = firstfh
                    if firstfh < fh:
                        # print "first height smaller than latter one"
                        return False

                if out_json["format"] == -1:
                    out_json["format"] = fmt
                elif out_json["format"] != fmt:
                    # print "format %d of this frame does not match of last frame %d"%(fmt,global_fmt)
                    return False

                # frames.append(os.path.join("%s.dir" %
                #                            bn, "%02d_%02d.png" % (bid, j)))

                if w != 0 and h != 0:
                    if fmt == 0:
                        pixeldata = f.read(w*h)
                    elif fmt == 1:
                        lineoffs = struct.unpack("<"+"I"*h, f.read(4*h))
                        for lineoff in lineoffs:
                            f.seek(offs+32+lineoff)
                            totalrowlength = 0
                            while totalrowlength < w:
                                code, length = struct.unpack("<BB", f.read(2))
                                length += 1
                                if code == 0xff:  # raw data
                                    pixeldata.extend(f.read(length))
                                else:  # rle
                                    # print(type(code))
                                    # print(length*chr(code))
                                    pixeldata.extend(length*chr(code))
                                totalrowlength += length
                    # elif fmt == 2:
                    #     lineoffs = struct.unpack("<%dH" % h, f.read(2*h))
                    #     _, _ = struct.unpack("<BB", f.read(2))  # unknown
                    #     for lineoff in lineoffs:
                    #         if f.tell() != offs+32+lineoff:
                    #             # print "unexpected offset: %d, expected %d"%(f.tell(),offs+32+lineoff)
                    #             f.seek(offs+32+lineoff)
                    #         totalrowlength = 0
                    #         while totalrowlength < w:
                    #             segment, = struct.unpack("<B", f.read(1))
                    #             code = segment >> 5
                    #             length = (segment & 0x1f)+1
                    #             if code == 7:  # raw data
                    #                 pixeldata.extend(f.read(length))
                    #                 print(pixeldata)
                    #             else:  # rle
                    #                 print(length*chr(code))
                    #                 pixeldata.extend(length*chr(code))
                    #             totalrowlength += length
                    elif fmt == 3:
                        # each row is split into 32 byte long blocks which are individually encoded
                        # two bytes store the offset for each block per line
                        ileh = int(w/32)
                        iled = int(w/16)
                        # print(ileh)
                        # print(iled)
                        # print(pixeldata)
                        lineoffs = [struct.unpack(
                            "<"+"H"*ileh, f.read(iled)) for i in range(h)]

                        for lineoff in lineoffs:
                            for i in lineoff:
                                if f.tell() != offs+32+i:
                                    # print "unexpected offset: %d, expected %d"%(f.tell(),offs+32+i)
                                    f.seek(offs+32+i)
                                totalblocklength = 0
                                while totalblocklength < 32:
                                    segment, = struct.unpack("<B", f.read(1))
                                    code = segment >> 5
                                    length = (segment & 0x1f)+1
                                    if code == 7:  # raw data
                                        # print(type(f.read(length)))
                                        pixeldata.extend(f.read(length))

                                        # print(pixeldata)
                                        # print(str(f.read(length)))
                                    else:  # rle
                                        # print(length*chr(code))
                                        # print(type(code))
                                        for e in range(0, length):

                                            pixeldata.append(int(code))

                                    totalblocklength += length
                    else:
                        # print "unknown format: %d"%fmt
                        return False
                    # print(fw, fh)
                    imp = Image.frombytes('P', (w, h), pixeldata)
                    imp.putpalette(palette)
                    # convert to RGBA
                    # imp.show()
                    imrgb = imp.convert("RGBA")
                    # replace special colors
                    # 0 -> (0,0,0,0)    = full transparency
                    # 1 -> (0,0,0,0x40) = shadow border
                    # 2 -> ???
                    # 3 -> ???
                    # 4 -> (0,0,0,0x80) = shadow body
                    # 5 -> (0,0,0,0)    = selection highlight, treat as full transparency
                    # 6 -> (0,0,0,0x80) = shadow body below selection, treat as shadow body
                    # 7 -> (0,0,0,0x40) = shadow border below selection, treat as shadow border
                    pixrgb = np.array(imrgb)
                    pixp = np.array(imp)
                    # print("XXXXXXXXXXXXXXX")
                    # print(pixp)
                    # print("XXXXXXXXXXXXXXX")
                    pixrgb[pixp == 0] = (0, 0, 0, 0)
                    pixrgb[pixp == 1] = (0, 0, 0, 0x40)
                    pixrgb[pixp == 4] = (0, 0, 0, 0x80)
                    pixrgb[pixp == 5] = (0, 0, 0, 0)
                    pixrgb[pixp == 6] = (0, 0, 0, 0x80)
                    pixrgb[pixp == 7] = (0, 0, 0, 0x40)
                    # imag = pygame.image.fr
                    imrgb = Image.fromarray(pixrgb)
                    im = Image.new('RGBA', (fw, fh), (0, 0, 0, 0))
                    im.paste(imrgb, (lm, tm))
                else:  # either width or height is zero
                    # imag = pygame.image.frombytes()
                    im = Image.new('RGBA', (fw, fh), (0, 0, 0, 0))

                images.append(pygame.image.frombytes(
                    im.tobytes(), im.size, im.mode))

            # out_json["sequences"].append({"group": bid, "frames": frames})
            # with open(os.path.join(outdir, "%s.json" % bn), "w+") as o:
            #     json.dump(out_json, o, indent=4)
        indeks_podzialu = random.randint(1, len(images))

        return images[indeks_podzialu:]+images[:indeks_podzialu]
