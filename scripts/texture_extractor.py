import os
import zlib
import shutil
from lib import getFilePath, getROMData, versions, getDirectoryLevel, TextureFormats, TextureFile, getSafeFileName, Version
import math
from PIL import Image
from db_textures_7 import textures_7
from db_textures_14 import textures_14
from db_textures_25 import textures_25
from typing import BinaryIO
from enum import IntEnum, auto

main_pointer_table_offset = 0
version = Version.us
tables = [7, 14, 25]
temp_im = "temp_im.bin"
texture_data_tables = {
    7: textures_7,
    14: textures_14,
    25: textures_25,
}

DISABLE_SMART_IMAGE_PROCESSING = False

class RenderingFormats(IntEnum):
    RGBA = auto()
    IA = auto()

class N64ImageFormats:
    
    def __init__(self, bits_per_px: int, render: RenderingFormats, color_bits: int, alpha_bits: int):
        self.bits_per_px = bits_per_px
        self.render = render
        self.color_bits = color_bits
        self.alpha_bits = alpha_bits



formats = {
    TextureFormats.RGBA5551: N64ImageFormats(16, RenderingFormats.RGBA, 5, 1),
    TextureFormats.RGBA32: N64ImageFormats(32, RenderingFormats.RGBA, 8, 8),
    TextureFormats.IA16: N64ImageFormats(16, RenderingFormats.IA, 8, 8),
    TextureFormats.IA8: N64ImageFormats(8, RenderingFormats.IA, 4, 4),
    TextureFormats.IA4: N64ImageFormats(4, RenderingFormats.IA, 3, 1),
    TextureFormats.I16: N64ImageFormats(16, RenderingFormats.IA, 16, 0),
    TextureFormats.I8: N64ImageFormats(8, RenderingFormats.IA, 8, 0),
    TextureFormats.I4: N64ImageFormats(4, RenderingFormats.IA, 4, 0),
}

def convertImage(fh: BinaryIO, file_data: TextureFile):
    format_data = formats[file_data.format]
    dim = (file_data.width, file_data.height)
    im_f = Image.new(mode="RGBA", size=dim)
    px = im_f.load()
    bit_sizes = [format_data.color_bits] * 3
    bit_sizes.append(format_data.alpha_bits)
    bit_offsets = [0]*4
    start = format_data.alpha_bits
    for x in range(3):
        bit_offsets[2 - x] = start
        if format_data.render == RenderingFormats.RGBA:
            start += format_data.color_bits
    for y in range(dim[1]):
        for x in range(dim[0]):
            mult = (format_data.bits_per_px / 8) * ((dim[0] * y) + x)
            fh.seek(int(mult))
            shift = int((mult % 1) * 8)
            pixel_data = int.from_bytes(fh.read(math.ceil(format_data.bits_per_px / 8)), "big")
            if format_data.bits_per_px < 8:
                pixel_data <<= shift
                pixel_data &= 0xFF
                and_val = 0xFF - ((1 << format_data.bits_per_px) - 1)
                pixel_data &= and_val
                pixel_data >>= (8 - format_data.bits_per_px)
            pixel_rgba = [0]*4
            for c in range(4):
                channel_index = c
                check = format_data.color_bits == 0
                if c == 3:
                    check = format_data.alpha_bits == 0
                if check:
                    pixel_rgba[c] = 255
                else:
                    clamp = (1 << bit_sizes[c]) - 1
                    channel = (pixel_data >> bit_offsets[channel_index]) & clamp
                    pixel_rgba[c] = int((channel / clamp) * 255)
            px[x, y] = tuple(pixel_rgba)
    return im_f

table_gifs = {}

def getImageHex(index: int):
    return "{:04X}".format(index)

def getImage(file_bytes: bytes, table_index: int, file_index: int, version_index: int, size: int) -> tuple:
    global table_gifs
    entry_hex = "{:04X}".format(file_index)
    with open(temp_im, "wb") as tmp:
        tmp.write(file_bytes)
    with open(temp_im, "rb") as tmp:
        
        if table_index in texture_data_tables:
            current_table = texture_data_tables[table_index]
            if current_table[file_index].convert and current_table[file_index].format in formats:
                if len(current_table[file_index].gif_listing) > 0:
                    table_gifs[current_table[file_index].name] = [f"{getImageHex(f)}_{current_table[f].name}" for f in current_table[file_index].gif_listing]
                return (convertImage(tmp, current_table[file_index]), True, f"{entry_hex}_{current_table[file_index].name}")
    return (file_bytes, False, f"tex{entry_hex}")

def genGIFFrame(path):
    im = Image.open(path)
    alpha = im.getchannel("A")
    im = im.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
    im.paste(255, mask)
    im.info["transparency"] = 255
    return im

GIF_LENGTH_PER_FRAME = 8

def extractTable(start, size, folder, path, table_index, version):
    global table_gifs
    print(f"Extracting {size} entries to {folder}")
    table_gifs = {}
    with open(path, "rb") as fg:
        for entry in range(size):
            if (entry % 500 == 499) or entry == (size - 1):
                print(f"{entry+1}/{size}")

            fg.seek(start + (entry * 4))
            entry_start = main_pointer_table_offset + (int.from_bytes(fg.read(4),"big") & 0x7FFFFFFF)
            entry_finish = main_pointer_table_offset + (int.from_bytes(fg.read(4),"big") & 0x7FFFFFFF)
            entry_size = entry_finish - entry_start
            if entry_size != 0:
                fg.seek(entry_start)
                data = fg.read(entry_size)
                fg.seek(entry_start)
                indic = int.from_bytes(fg.read(2), "big")
                if indic == 0x1F8B:
                    data = zlib.decompress(data, (15 + 32))
                entry_hex = "{:04X}".format(entry)
                file_name = f"tex{entry_hex}"
                if not DISABLE_SMART_IMAGE_PROCESSING:
                    f_bytes, is_png, file_name = getImage(data, table_index, entry, version, len(data))
                else:
                    is_png = False
                if is_png:
                    f_bytes.save(f"{folder}{getSafeFileName(file_name)}.png")
                with open(f"{folder}{getSafeFileName(file_name)}.bin","wb") as tex:
                    tex.write(data)
        gif_path = f"{folder}gifs"
        if os.path.exists(gif_path):
            shutil.rmtree(gif_path)
        if len(table_gifs) > 0:
            os.mkdir(gif_path)
            files_in_dir = [x for x in os.listdir(folder) if os.path.isfile(os.path.join(folder, x))]
            for gif_name in table_gifs:
                gif_list = table_gifs[gif_name]
                imgs = []
                for f in gif_list:
                    if f"{f}.png" in files_in_dir:
                        imgs.append(genGIFFrame(os.path.join(folder, f"{f}.png")))
                if len(imgs) <= 1:
                    continue
                imgs[0].save(f"{gif_path}/{gif_name}.gif", save_all=True, append_images=imgs[1:], loop=0, duration=GIF_LENGTH_PER_FRAME * len(imgs), disposal=2)

def getROMTables():
    global main_pointer_table_offset
    global version

    file_path = getFilePath()
    main_pointer_table_offset, version, dump_path, valid = getROMData(file_path, "textures")
    if valid:
        for x in tables:
            tbl_name = x
            if version == Version.kiosk:
                tbl_name = x - 1
            tbl_path = f"{dump_path}/table_{tbl_name}"
            if os.path.exists(tbl_path):
                shutil.rmtree(tbl_path)
            os.mkdir(tbl_path)

        with open(file_path,"rb") as fh:
            for tbl in tables:
                focused_tbl = tbl
                if version == Version.kiosk:
                    focused_tbl -= 1 # Kiosk is missing table 0
                fh.seek(main_pointer_table_offset + (32 * 4) + (focused_tbl * 4))
                tbl_size = int.from_bytes(fh.read(4),"big")
                fh.seek(main_pointer_table_offset + (focused_tbl * 4))
                tbl_start = main_pointer_table_offset + int.from_bytes(fh.read(4),"big")
                extractTable(tbl_start,tbl_size,f"{dump_path}/table_{focused_tbl}/",file_path, focused_tbl, version)
    if os.path.exists(temp_im):
        os.remove(temp_im)

getROMTables()