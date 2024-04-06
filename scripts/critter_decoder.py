import zlib
import os
import shutil
import json
import struct
from lib import getFilePath, getROMData, maps

num_tables = 32
pointer_tables = []
main_pointer_table_offset = 0
setup_table_index = 9
script_table_index = 10
files = {}
tab_indentation = 0
folder_removal = []
version = 0

CRITTER_TYPES = [
    "TYPE_BAT_BROWN",
    "TYPE_BAT_PURPLE",
    "TYPE_FISH",
    "TYPE_BUTTERFLY",
    "TYPE_MOUSE",
]

def grabCritters(data, mapPath):
    built_file = mapPath + "/critter.bin"
    data = []
    with open(built_file, "rb") as fh:
        count = int.from_bytes(fh.read(1), "big")
        for _ in range(count):
            critter_type = int.from_bytes(fh.read(1), "big")
            count_0 = int.from_bytes(fh.read(1), "big")
            critter_bundle_count = int.from_bytes(fh.read(1), "big")
            sub_data = {
                "critter_type": CRITTER_TYPES[critter_type],
                "bundle_count": critter_bundle_count,
            }
            new_sub = []
            for y in range(count_0):
                pos_x = int.from_bytes(fh.read(2), "big")
                pos_y = int.from_bytes(fh.read(2), "big")
                pos_z = int.from_bytes(fh.read(2), "big")
                offset_data = [
                    1, # 0x06
                    1, # 0x07
                    2, # 0x08
                    1, # 0x0A
                    1, # 0x0B
                    2, # 0x0C
                    1, # 0x0E
                    1, # 0x0F
                    2, # 0x10
                    1, # 0x12
                    1, # 0x13
                    4, # 0x14
                    1, # 0x18
                    1, # 0x19
                    1, # 0x1A
                    1, # 0x1B
                    1, # 0x1C
                    1, # 0x1D
                    1, # 0x1E
                    1, # 0x1F
                ]
                extra_data = {}
                offset = 6
                for entry in offset_data:
                    extra_data[f"unk_{hex(offset)}"] = int.from_bytes(fh.read(entry), "big")
                    offset += entry
                new_sub.append({
                    "x": pos_x,
                    "y": pos_y,
                    "z": pos_z,
                    "unk": extra_data
                })
            sub_data["sub"] = new_sub
            data.append(sub_data)
    with open(f"{mapPath}/critter.json", "w") as fh:
        fh.write(json.dumps(data, indent=4))
    # if os.path.exists(built_file):
    #     os.remove(built_file)


def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).rstrip("_")

def extractMaps(src_file: str, dump_path: str):
    global maps

    for mapIndex, mapName in enumerate(maps):
        mapPath = f"{dump_path}/{mapIndex} - {make_safe_filename(mapName)}"
        os.mkdir(mapPath)
        extractMap(src_file, mapIndex, mapPath)

def extractMap(src_file: str, mapIndex : int, mapPath : str):
    global pointer_tables
    global files
    global num_tables
    global folder_removal

    critter_table = 0x16 - (version == 3)
    entry_size = 0

    idx = 0
    with open(src_file,"rb") as fl:
        fl.seek(main_pointer_table_offset + (num_tables * 4) + (4 * critter_table))
        tbl_size = int.from_bytes(fl.read(4),"big")
        if tbl_size > mapIndex:
            fl.seek(main_pointer_table_offset + (4 * critter_table))
            tbl_ptr = main_pointer_table_offset + int.from_bytes(fl.read(4),"big")
            fl.seek(tbl_ptr + (4 * mapIndex))
            entry_start = main_pointer_table_offset + (int.from_bytes(fl.read(4),"big") & 0x7FFFFFFF)
            entry_finish = main_pointer_table_offset + (int.from_bytes(fl.read(4),"big") & 0x7FFFFFFF)
            entry_size = entry_finish - entry_start
            if entry_size > 0:
                fl.seek(entry_start)
                compress = fl.read(entry_size)
                temp_bin = "temp.bin"
                with open(temp_bin,"wb") as fh:
                    fh.write(compress)
                if int.from_bytes(compress[0:1],"big") == 0x1F and int.from_bytes(compress[1:2],"big") == 0x8B:
                    data = zlib.decompress(compress, 15+32)
                else:
                    data = compress
                # Critters
                built_file = mapPath + "/critter.bin"
                with open(built_file, "wb") as fh:
                    fh.write(data)
                grabCritters(data, mapPath)
                if os.path.exists(temp_bin):
                    os.remove(temp_bin)
            idx += 1
    if entry_size == 0:
        folder_removal.append(mapPath)

def bytereadToInt(read):
    total = 0
    for x in list(read):
        total = (total * 256) + x
    return total

def extractScripts():
    global folder_removal
    global main_pointer_table_offset
    global version

    file_path = getFilePath()
    main_pointer_table_offset, version, dump_path, valid = getROMData(file_path, "critters")
    if valid:
        extractMaps(file_path, dump_path)
        for x in folder_removal:
            if os.path.exists(x):
                for filename in os.listdir(x):
                    file_path = os.path.join(x,filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print("Failed to delete %s. Reason: %s" % (file_path, e))
                os.rmdir(x)

extractScripts()