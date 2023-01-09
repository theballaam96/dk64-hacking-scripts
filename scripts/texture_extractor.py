import os
import zlib
import shutil
from lib import getFilePath, getROMData, versions, getDirectoryLevel
import texture_size_guesser
import json
from PIL import Image

main_pointer_table_offset = 0
version = 0
tables = [7, 14, 25]
temp_im = "temp_im.bin"

DISABLE_SMART_IMAGE_PROCESSING = False

class N64ImageFormats:
    
    def __init__(self, bytes_per_px: int, color_bits: int, alpha_bits: int):
        self.bytes_per_px = bytes_per_px
        self.color_bits = color_bits
        self.alpha_bits = alpha_bits

formats = {
    "rgba5551": N64ImageFormats(2, 5, 1),
}

def getImage(file_bytes: bytes, table_index: int, file_index: int, version_index: int) -> tuple:
    with open(f"{getDirectoryLevel()}bin/texture sizes/{versions[version_index]}/table_{table_index}.json", "r") as fh:
        data = json.loads(fh.read())
        with open(temp_im, "wb") as tmp:
            tmp.write(file_bytes)
        with open(temp_im, "rb") as tmp:
            if str(file_index) in data:
                file_data = data[str(file_index)]
                if file_data["verified"] and "dimensions" in file_data and "format" in file_data:
                    if file_data["format"] in formats:
                        format_data = formats[file_data["format"]]
                        dim = (file_data["dimensions"][0], file_data["dimensions"][1])
                        im_f = Image.new(mode="RGBA", size=dim)
                        px = im_f.load()
                        bit_offsets = [0]*4
                        bit_sizes = [format_data.color_bits] * 3
                        bit_sizes.append(format_data.alpha_bits)
                        start = format_data.alpha_bits
                        for x in range(3):
                            bit_offsets[2 - x] = start
                            start += format_data.color_bits
                        for y in range(dim[1]):
                            for x in range(dim[0]):
                                tmp.seek(format_data.bytes_per_px * ((dim[1] * y) + x))
                                pixel_data = int.from_bytes(tmp.read(format_data.bytes_per_px), "big")
                                pixel_rgba = [0]*4
                                for c in range(4):
                                    clamp = (1 << bit_sizes[c]) - 1
                                    channel = (pixel_data >> bit_offsets[c]) & clamp
                                    pixel_rgba[c] = int((channel / clamp) * 255)
                                px[x, y] = tuple(pixel_rgba)
                        return (im_f, True)
    return (file_bytes, False)

def extractTable(start, size, folder, path, table_index, version):
    print(f"Extracting {size} entries to {folder}")
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
                if not DISABLE_SMART_IMAGE_PROCESSING:
                    f_bytes, is_png = getImage(data, table_index, entry, version)
                else:
                    is_png = False
                entry_hex = "{:04X}".format(entry)
                if is_png:
                    f_bytes.save(f"{folder}tex{entry_hex}.png")
                else:
                    with open(f"{folder}tex{entry_hex}.bin","wb") as tex:
                        tex.write(data)

def getROMTables():
    global main_pointer_table_offset
    global version

    file_path = getFilePath()
    main_pointer_table_offset, version, dump_path, valid = getROMData(file_path, "textures")
    if valid:
        for x in tables:
            tbl_name = x
            if version == 3:
                tbl_name = x - 1
            tbl_path = f"{dump_path}/table_{tbl_name}"
            if os.path.exists(tbl_path):
                shutil.rmtree(tbl_path)
            os.mkdir(tbl_path)

        with open(file_path,"rb") as fh:
            for tbl in tables:
                focused_tbl = tbl
                if version == 3:
                    focused_tbl -= 1 # Kiosk is missing table 0
                fh.seek(main_pointer_table_offset + (32 * 4) + (focused_tbl * 4))
                tbl_size = int.from_bytes(fh.read(4),"big")
                fh.seek(main_pointer_table_offset + (focused_tbl * 4))
                tbl_start = main_pointer_table_offset + int.from_bytes(fh.read(4),"big")
                extractTable(tbl_start,tbl_size,f"{dump_path}/table_{focused_tbl}/",file_path, focused_tbl, version)
    if os.path.exists(temp_im):
        os.remove(temp_im)

getROMTables()