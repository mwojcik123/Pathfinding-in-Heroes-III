# a = "elo"
import base64
from PIL import Image
import io
import os
import struct
import json
from collections import defaultdict
import numpy as np
# b = b"elo"
# c = bytes(a, encoding="latin-1")
# print(c)
# print(a)
# print(b[0])
# print(str(a))
# infile = "AVMgorf0.def"
# f = open(infile, "rb")
# # f2 = open("tekst.txt", "rb")
# bn = os.path.basename(infile)
# bn = os.path.splitext(bn)[0].lower()

# t, x, y, blocks = struct.unpack("<IIII", f.read(16))
# print(t)
# print(x)
# print(y)
# print(blocks)

# # palette = []
# v = f.read(3)
# for i in range(256):
#     r, g, b = struct.unpack("<BBB", v)
#     print(r)
#     print(g)
#     print(b)

#     palette.extend((r, g, b))
# f.seek(4)
# content = f.readlines()

# f.read
# heli = f.detach()
# content = f.readlines()

# print(bytes(content[0], "utf-8"))
# print(content[0][0])
# print(heli.read(3))
# print(content)
# print(content.decode('utf-8'))

# print(str(bytes(content, "utf-8")))
# print(f)

# img = Image.open(io.BytesIO(content))


def extract_def(infile, outdir):
    f = open(infile, "rb")
    print(type(f))
    bn = os.path.basename(infile)
    bn = os.path.splitext(bn)[0].lower()

    # t - type
    # blocks - # of blocks
    # the second and third entry are width and height which are not used
    # print(f.read(16))
    t, x, y, blocks = struct.unpack("<IIII", f.read(16))
    print(t)
    print(x)
    print(y)
    print(blocks)
    palette = []

    for i in range(256):
        r, g, b = struct.unpack("<BBB", f.read(3))
        palette.extend((r, g, b))

    offsets = defaultdict(list)
    for i in range(blocks):
        # bid - block id
        # entries - number of images in this block
        # the third and fourth entry have unknown meaning
        bid, entries, no1, no2 = struct.unpack("<IIII", f.read(16))
        print(bid)
        print(entries)
        print(no1)
        print(no2)

        names = []
        # a list of 13 character long filenames
        cont = 0
        for j in range(entries):
            cont += 1
            g = f.read(13)

            print(g)
            name = struct.unpack("13s", g)
        # a list of offsets
        for j in range(entries):
            offs, = struct.unpack("<I", f.read(4))
            offsets[bid].append(offs)

    outpath = os.path.join(outdir, "%s.dir" % bn)
    if os.path.exists(outpath):
        if not os.path.isdir(outpath):
            print("output path exists and is no directory")
            return False
    else:
        os.mkdir(outpath)

    out_json = {"sequences": [], "type": t, "format": -1}

    firstfw, firstfh = -1, -1
    for bid, l in offsets.items():
        print("SSS")
        print(bid, l)
        print("SSS")
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
            outname = os.path.join(outdir, "%s.dir" %
                                   bn, "%02d_%02d.png" % (bid, j))
            print("writing to %s" % outname)

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

            frames.append(os.path.join("%s.dir" %
                          bn, "%02d_%02d.png" % (bid, j)))

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
                                print(type(code))
                                print(length*chr(code))
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
                print(fw, fh)
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
                imrgb = Image.fromarray(pixrgb)
                im = Image.new('RGBA', (fw, fh), (0, 0, 0, 0))
                im.paste(imrgb, (lm, tm))
            else:  # either width or height is zero
                im = Image.new('RGBA', (fw, fh), (0, 0, 0, 0))
            im.save(outname)
        out_json["sequences"].append({"group": bid, "frames": frames})
        with open(os.path.join(outdir, "%s.json" % bn), "w+") as o:
            json.dump(out_json, o, indent=4)
    return True


ret = extract_def("Watrtl.def", "./out")
