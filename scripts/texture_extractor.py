import os
import zlib
import shutil
from lib import getFilePath, getROMData, getSafeFolderName

main_pointer_table_offset = 0
version = 0
tables = [7, 14, 25]


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
                extractTable(tbl_start,tbl_size,f"{dump_path}/table_{focused_tbl}/",file_path)

getROMTables()