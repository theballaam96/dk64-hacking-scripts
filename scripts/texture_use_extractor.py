import os
import zlib
import shutil
from lib import getFilePath, getROMData, getSafeFolderName, maps

main_pointer_table_offset = 0
version = 0
mapgeo_table = [1,1,1,0]
m2geo_table = [4,4,4,3]
actgeo_table = [5,5,5,4]
geo_tables = [mapgeo_table,m2geo_table,actgeo_table]
geo_table_names = ["map_geometry","modeltwo_geometry","actor_geometry"]
unused = list(range(6030))
used = {}

def extractTable(table_start,table_size,dump_path,src_path,table_index,use_mapname):
    with open(src_path,"rb") as fh:
        for item in range(table_size):
            fh.seek(table_start + (item * 4))
            item_start = main_pointer_table_offset + (int.from_bytes(fh.read(4),"big") & 0x7FFFFFFF)
            item_finish = main_pointer_table_offset + (int.from_bytes(fh.read(4),"big") & 0x7FFFFFFF)
            item_size = item_finish - item_start
            if item_size > 0:
                fh.seek(item_start)
                compress = fh.read(item_size)
                if int.from_bytes(compress[0:1],"big") == 0x1F and int.from_bytes(compress[1:2],"big") == 0x8B:
                    data = zlib.decompress(compress, 15+32)
                else:
                    data = compress
                temp = "temp.bin"
                with open(temp,"wb") as fg:
                    fg.write(data)
                data_size = len(data)
                commands = int(data_size / 8) + 1
                texture_list = []
                with open(temp, "rb") as fg:
                    for x in range(commands):
                        fg.seek(x * 8)
                        command_header = int.from_bytes(fg.read(1),"big")
                        if command_header == 0xFD:
                            fg.seek((x * 8) + 4)
                            text = int.from_bytes(fg.read(4),"big")
                            if not text in texture_list:
                                texture_list.append(text)
                            if text in unused and item not in (0x59,0x5B,0x1F2,0x1F3,0x1F5,0x1F6):
                                unused.remove(text)
                            if text < 6130:
                                if text in used:
                                    used[text].append(f"t{table_index}f{item}")
                                else:
                                    used[text] = [f"t{table_index}f{item}"]
                if len(texture_list) > 0:
                    sub_dump = f"{dump_path}/item_{item}.txt"
                    if use_mapname:
                        sub_dump = f"{dump_path}/{item} - {maps[item]}.txt"
                    with open(sub_dump,"w") as fg:
                        for x in texture_list:
                            fg.write(f"{hex(x)}\n")
                if os.path.exists(temp):
                    os.remove(temp)


def getROMTables():
    global main_pointer_table_offset
    global version

    file_path = getFilePath()
    main_pointer_table_offset, version, dump_path, valid = getROMData(file_path, "texture uses")
    if valid:
        for x in geo_table_names:
            tbl_path = f"{dump_path}/{x}"
            if os.path.exists(tbl_path):
                shutil.rmtree(tbl_path)
            os.mkdir(tbl_path)

        with open(file_path,"rb") as fh:
            tbl_index = 0
            for sub_index, tbl in enumerate(geo_tables):
                focused_tbl = tbl[version]
                fh.seek(main_pointer_table_offset + (32 * 4) + (focused_tbl * 4))
                tbl_size = int.from_bytes(fh.read(4),"big")
                fh.seek(main_pointer_table_offset + (focused_tbl * 4))
                tbl_start = main_pointer_table_offset + int.from_bytes(fh.read(4),"big")
                extractTable(tbl_start,tbl_size,f"{dump_path}/{geo_table_names[tbl_index]}",file_path,focused_tbl, subindex==0)
                tbl_index += 1
        with open(f"{dump_path}/unused.txt","w") as fh:
            for x in unused:
                fh.write(f"{hex(x)}\n")
        with open(f"{dump_path}/used.txt","w") as fh:
            for x in used:
                fh.write(f"{hex(x)}: {', '.join(used[x])}\n")

getROMTables()