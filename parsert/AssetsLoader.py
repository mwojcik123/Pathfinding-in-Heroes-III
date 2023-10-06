import zlib
import struct
import codecs
import os
from PIL import Image, ImageDraw
from parsert.Asset import Asset


class AssetsLoader:
    def __init__(self):
        self.file = open("H3sprite.lod", "rb")
        self.files_list = self.unpack_lod("H3sprite.lod", "./out")
        # print(self.files_list)
        print(self.files_list)

    # def loader(self, file):
    def get_sprite(self, name, pos, z_index, above, passable, active):
        lower_name = name.lower()
        # print(lower_name)
        for i in self.files_list:
            if i[0] == lower_name:
                # print(lower_name)

                # print(i)

                # files.append((name, offset, size, csize))
                self.file.seek(i[1])
                if i[3] != 0:
                    data = zlib.decompress(self.file.read(i[3]))

                else:
                    data = self.file.read(i[2])
                    print(data)

                return Asset(data, pos, z_index, above, passable, active)

    def is_pcx(self, data):
        size, width, height = struct.unpack("<III", data[:12])
        return size == width*height or size == width*height*3

    def read_pcx(self, data):
        size, width, height = struct.unpack("<III", data[:12])
        if size == width*height:
            im = Image.fromstring('P', (width, height),
                                  data[12:12+width*height])
            palette = []
            for i in range(256):
                offset = 12+width*height+i*3
                r, g, b = struct.unpack("<BBB", data[offset:offset+3])
                palette.extend((r, g, b))
            im.putpalette(palette)
            return im
        elif size == width*height*3:
            return Image.fromstring('RGB', (width, height), data[12:])
        else:
            return None

    def unpack_lod(self, infile, outdir):
        f = open(infile, "rb")

        header = f.read(4)
        # print(header)
        if header != b'LOD\x00':

            return Exception("failed file")

        f.seek(8)
        total, = struct.unpack("<I", f.read(4))

        f.seek(92)

        files = []

        for i in range(total):
            filename, = struct.unpack("16s", f.read(16))
            filename = filename[:filename.index(b'\0')]
            name = codecs.decode(filename, 'utf-8').lower()

            offset, size, xk, csize = struct.unpack("<IIII", f.read(16))
            # gwno = struct.unpack("8s", f.read(8))
            # print(gwno)
            files.append((name, offset, size, csize, xk))
        return files
        # print(files)
        # for filename, offset, size, csize in files:

        # name = codecs.decode(filename, 'utf-8')
        # print(name)
        # print(type(name))
        # filename = os.path.join(outdir, name)

        # f.seek(offset)
        # if csize != 0:
        #     data = zlib.decompress(f.read(csize))
        # else:
        #     data = f.read(size)
        # if self.is_pcx(data):
        #     im = self.read_pcx(data)
        #     if not im:
        #         return False
        #     filename = os.path.splitext(filename)[0]
        #     filename = filename+".png"
        #     im.save(filename)
        # else:
        #     with open(filename, "wb") as o:
        #         o.write(data)

        # return True
