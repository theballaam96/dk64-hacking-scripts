import zlib
import os
import shutil
import json
import struct

from lib import getFilePath, getROMData, getSafeFolderName, maps

main_pointer_table_offset = 0
setup_table_index = 9
folder_removal = []
version = 0

temp_file = "temp.bin"

def int_to_float(val):
    """Convert a hex int to a float."""
    if val == 0:
        return 0
    return struct.unpack("!f", bytes.fromhex(hex(val).split("0x")[1]))[0]

def decodeData(data):
    model_two = []
    mystery = []
    actor = []
    if len(data) >= 0xC:
        with open(temp_file,"wb") as fh:
            fh.write(data)
        with open(temp_file,"rb") as fh:
            model_two_size = int.from_bytes(fh.read(4),"big")
            for x in range(model_two_size):
                fh.seek(4 + (x * 0x30))
                byte_read = []
                for y in range(0x30):
                    byte_read.append(int.from_bytes(fh.read(1),"big"))
                fh.seek(4 + (x * 0x30))
                coords = []
                for y in range(3):
                    coords.append(int_to_float(int.from_bytes(fh.read(4),"big")))
                model_two.append({
                    "coords": coords.copy()
                    # "data": byte_read.copy()
                })
            mystery_start = 4 + (model_two_size * 0x30)
            fh.seek(mystery_start)
            mystery_size = int.from_bytes(fh.read(4),"big")
            for x in range(mystery_size):
                fh.seek(mystery_start + 4 + (x * 0x24))
                byte_read = []
                for y in range(0x24):
                    byte_read.append(int.from_bytes(fh.read(1),"big"))
                mystery.append({
                    "data": byte_read.copy()
                })
            actor_start = mystery_start + 4 + (mystery_size * 0x24)
            fh.seek(actor_start)
            actor_size = int.from_bytes(fh.read(4),"big")
            for x in range(actor_size):
                fh.seek(actor_start + 4 + (x * 0x38))
                byte_read = []
                for y in range(0x38):
                    byte_read.append(int.from_bytes(fh.read(1),"big"))
                actor.append({
                    "data": byte_read.copy()
                })
        if os.path.exists(temp_file):
            os.remove(temp_file)
    return {"model_two":model_two.copy(),"mystery":mystery.copy(),"actor":actor.copy()}

def make_safe_filename(s):
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).rstrip("_")

def extractMaps(src_file: str, dump_path: str):
    global maps
    global folder_removal

    setup_table_index = 9 - (version == 3)
    with open(src_file,"rb") as fh:
        fh.seek(main_pointer_table_offset + (setup_table_index * 4))
        setup_table = (int.from_bytes(fh.read(4),"big") & 0x7FFFFFFF) + main_pointer_table_offset
        for mapIndex, mapName in enumerate(maps):
            lim = 221
            if version == 3:
                lim = 200
            if mapIndex < lim:
                mapPath = f"{dump_path}/{make_safe_filename(mapName)}"
                os.mkdir(mapPath)
                fh.seek(setup_table + (mapIndex * 4))
                file_start = (int.from_bytes(fh.read(4),"big") & 0x7FFFFFFF) + main_pointer_table_offset
                file_end = (int.from_bytes(fh.read(4),"big") & 0x7FFFFFFF) + main_pointer_table_offset
                file_size = file_end - file_start
                fh.seek(file_start)
                header_check = int.from_bytes(fh.read(2),"big")
                is_compressed = header_check == 0x1F8B
                fh.seek(file_start)
                compress = fh.read(file_size)
                if is_compressed and file_size > 0:
                    data = zlib.decompress(compress, 15+32)
                else:
                    data = compress
                with open(f"{mapPath}/data.bin","wb") as fg:
                    fg.write(data)
                json_data = decodeData(data)
                total_size = 0
                for x in ["model_two","mystery","actor"]:
                    total_size += len(json_data[x])
                if total_size == 0:
                    folder_removal.append(mapPath)
                with open(f"{mapPath}/output.json","w") as fg:
                    fg.write(json.dumps(json_data, indent=4))

def extractSetup():
    global folder_removal
    global main_pointer_table_offset
    global version

    file_path = getFilePath()
	main_pointer_table_offset, version, dump_path, valid = getROMData(file_path, "setup")
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

extractSetup()