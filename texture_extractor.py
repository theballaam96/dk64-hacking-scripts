import tkinter as tk
from tkinter import filedialog
import os
import zlib
import shutil

root = tk.Tk()
root.withdraw()

pointer_table_offsets = [0x101C50,0x1038D0,0x1039C0, 0x1A7C20]
main_pointer_table_offset = pointer_table_offsets[0]
version = 0
tables = [7, 14, 25]
folder_append = ["_us","_pal","_jp","_kiosk"]


def extractTable(start, size, folder, path):
    print(f"Extracting {size} entries to {folder}")
    with open(path, "rb") as fg:
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
                entry_hex = "{:04X}".format(entry)
                with open(f"{folder}tex{entry_hex}.bin","wb") as tex:
                    tex.write(data)

def getROMTables():
    global main_pointer_table_offset
    global version
    global folder_append

    append = folder_append[0]

    file_path = filedialog.askopenfilename()
    with open(file_path,"rb") as fh:
        endianness = int.from_bytes(fh.read(1),"big")
        if endianness != 0x80:
            print("File is little endian. Convert to big endian and re-run")
            exit()
        else:
            fh.seek(0x3D)
            release_or_kiosk = int.from_bytes(fh.read(1),"big")
            region = int.from_bytes(fh.read(1),"big")
            version = -1
            if release_or_kiosk == 0x50:
                version = 3 # Kiosk
            else:
                if region == 0x45:
                    version = 0 # US
                elif region == 0x4A:
                    version = 2 # JP
                elif region == 0x50:
                    version = 1 # PAL
                else:
                    print("Invalid version")
                    exit()
            main_pointer_table_offset = pointer_table_offsets[version]
            append = folder_append[version]

    dump_path = f"textures{append}"
    if os.path.exists(dump_path):
        shutil.rmtree(dump_path)
    os.mkdir(dump_path)
    for x in tables:
        tbl_name = x
        if version == 3:
            tbl_name = x - 1
        tbl_path = f"{dump_path}/table_{tbl_name}"
        if os.path.exists(tbl_path):
            shutil.rmtree(tbl_path)
        os.mkdir(tbl_path)

    with open(file_path,"rb") as fh:
        tbl_index = 0
        for tbl in tables:
            focused_tbl = tbl
            if version == 3:
                focused_tbl -= 1 # Kiosk is missing table 0
            fh.seek(main_pointer_table_offset + (32 * 4) + (focused_tbl * 4))
            tbl_size = int.from_bytes(fh.read(4),"big")
            fh.seek(main_pointer_table_offset + (focused_tbl * 4))
            tbl_start = main_pointer_table_offset + int.from_bytes(fh.read(4),"big")
            extractTable(tbl_start,tbl_size,f"{dump_path}/table_{focused_tbl}/",file_path)

getROMTables()