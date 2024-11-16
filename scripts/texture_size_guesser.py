import os
import zlib
import shutil
import json
from lib import getFilePath, getROMData, maps, Version

main_pointer_table_offset = 0
version = Version.us
tables = [7, 14, 25]

size_guesses = {
    0x1000: {
        "dim": (32, 64),
        "format": "rgba5551"
    },
    0x800: {
        "dim": (32, 32),
        "format": "rgba5551"
    },
    0xFC0: {
        "dim": (48, 42),
        "format": "rgba5551"
    },
    0xAA0: {
        "dim": (32, 44),
        "format": "rgba5551"
    },
    0xF20: {
        "dim": (44, 44),
        "format": "rgba5551"
    }
}

def extractTable(start, size, folder, path, table_index):
    print(f"Extracting {size} entries to {folder}")
    with open(path, "rb") as fg:
        dump_data = {}
        for entry in range(size):
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
                if len(data) > 0:
                    dim = (0, 0)
                    format = None
                    if len(data) in size_guesses:
                        dim = size_guesses[len(data)]["dim"]
                        format = size_guesses[len(data)]["format"]
                    add = {
                        "size": hex(len(data)),
                        "verified": True,
                    }
                    if dim[0] != 0 and dim[1] != 0:
                        add["dimensions"] = dim
                    if format is not None:
                        add["format"] = format
                    dump_data[entry] = add
                    
                    
        with open(f"{folder}table_{table_index}.json", "w") as dump:
            dump.write(json.dumps(dump_data, indent=4))

def getROMTables():
    global main_pointer_table_offset
    global version

    file_path = getFilePath()
    main_pointer_table_offset, version, dump_path, valid = getROMData(file_path, "texture sizes")
    if valid:
        if os.path.exists(dump_path):
            shutil.rmtree(dump_path)
        os.mkdir(dump_path)

        with open(file_path,"rb") as fh:
            for tbl in tables:
                focused_tbl = tbl
                if version == Version.kiosk:
                    focused_tbl -= 1 # Kiosk is missing table 0
                fh.seek(main_pointer_table_offset + (32 * 4) + (focused_tbl * 4))
                tbl_size = int.from_bytes(fh.read(4),"big")
                fh.seek(main_pointer_table_offset + (focused_tbl * 4))
                tbl_start = main_pointer_table_offset + int.from_bytes(fh.read(4),"big")
                extractTable(tbl_start,tbl_size,f"{dump_path}/",file_path, focused_tbl)

getROMTables()