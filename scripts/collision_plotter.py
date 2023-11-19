import os
import zlib
import shutil
import gzip
from typing import BinaryIO
import math

from lib import getFilePath, getROMData, maps, getSafeFolderName

class Triangle:
    def __init__(self, coord_set_0: list, coord_set_1: list, coord_set_2: list, properties: int, sfx: int, brightness: int, unk17: int, table: int):
        self.coords = (coord_set_0, coord_set_1, coord_set_2)
        self.properties = hex(properties)
        self.is_wall = table == 2
        self.is_floor = table == 3
        self.sfx = sfx
        self.brightness = brightness
        self.unk17 = unk17
        # Floor Props
        self.is_void = (properties & 0x4000) != 0
        self.is_nonsolid = (properties & 0x800) != 0
        self.is_damage = (properties & 0x40) != 0
        self.is_instadeath = (properties & 0x10) != 0
        self.is_water = (properties & 0x1) != 0

class CollisionInfo:
    def __init__(self, pointer_table: int, name: str, count_0: int, count_1: int, compressed_bit: int, divisor: int):
        self.pointer_table = pointer_table
        self.name = name
        self.counts = [count_0, count_1]
        self.compressed_bit = compressed_bit
        self.divisor = divisor
        
    def dumpTris(self, fh: BinaryIO, map: int, pointer_offset: int, count: int, is_compressed: bool) -> list:
        meshes = []
        fh.seek(pointer_offset + (self.pointer_table << 2))
        table_start = pointer_offset + int.from_bytes(fh.read(4), "big")
        fh.seek(table_start + (map << 2))
        map_start_raw = int.from_bytes(fh.read(4), "big")
        map_end_raw = int.from_bytes(fh.read(4), "big")
        if map_start_raw & 0x80000000:
            return []
        map_start = pointer_offset + (map_start_raw & 0x7FFFFFFF)
        map_end = pointer_offset + (map_end_raw & 0x7FFFFFFF)
        map_size = map_end - map_start
        if map_size > 0:
            fh.seek(map_start)
            compressed = int.from_bytes(fh.read(2), "big") == 0x1F8B
            fh.seek(map_start)
            map_data = fh.read(map_size)
            if compressed:
                map_data = zlib.decompress(map_data, (15 + 32))
            with open("temp.bin","wb") as fg:
                fg.write(map_data)
            start = 8
            print(f"Block count: {count}")
            with open("temp.bin", "rb") as fg:
                total_tris = int.from_bytes(fg.read(4))
                print(f"Parsing table {self.pointer_table} for map {map}. Total Tris: {total_tris}")
                for index in range(count):
                    if fg.tell() >= len(map_data):
                        continue
                    mesh = []
                    fg.seek(start - 4)
                    block_end = int.from_bytes(fg.read(4), "big")
                    block_count = int((block_end - start) / 0x18)
                    # print(f"Mesh {index} Tri Count: {block_count}")
                    for tri_index in range(block_count):
                        if fg.tell() % 4 != 0:
                            print("Something is wrong")
                            print(map, self.pointer_table)
                            exit()
                        coord_set = [[None, None, None], [None, None, None], [None, None, None]]
                        for cs in range(3):
                            points = []
                            for _ in range(3):
                                points.append(int.from_bytes(fg.read(2), "big"))
                            for pi, p in enumerate(points):
                                if p > 32767:
                                    p -= 65536
                                points[pi] = p / self.divisor
                            for y in range(3):
                                if self.pointer_table == 3:
                                    # Floors
                                    coord_set[y][cs] = points[y]
                                elif self.pointer_table == 2:
                                    # Walls
                                    coord_set[cs][y] = points[y]
                                else:
                                    print("Invalid pointer table")
                                    exit()
                        properties = int.from_bytes(fg.read(2), "big")
                        sfx = int.from_bytes(fg.read(2), "big")
                        brightness = int.from_bytes(fg.read(1), "big")
                        unk17 = int.from_bytes(fg.read(1), "big")
                        mesh.append(Triangle(coord_set[0], coord_set[1], coord_set[2], properties, sfx, brightness, unk17, self.pointer_table))
                    meshes.append(mesh)
                    start = block_end + 4
        global_mesh = []
        for mesh in meshes:
            global_mesh.extend(mesh)
        return global_mesh
        

folder_removal = []

def getGeoRead(fh: BinaryIO, offset: int, offset_size: int, pointer_offset: int, map: int):
    fh.seek(pointer_offset + (1 << 2))
    table_start = pointer_offset + int.from_bytes(fh.read(4), "big")
    fh.seek(table_start + (map << 2))
    map_start = pointer_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
    map_end = pointer_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
    map_size = map_end - map_start
    fh.seek(map_start)
    compressed = int.from_bytes(fh.read(2), "big") == 0x1F8B
    fh.seek(map_start)
    map_data = fh.read(map_size)
    if compressed:
        map_data = zlib.decompress(map_data, (15 + 32))
    with open("temp.bin", "wb") as fg:
        fg.write(map_data)
    with open("temp.bin", "rb") as fg:
        fg.seek(offset)
        return int.from_bytes(fg.read(offset_size), "big")


collision_info = [
    CollisionInfo(2, "Walls", 0x10, 0x12, 1, 1),
    CollisionInfo(3, "Floors", 0x18, 0x1A, 2, 6),
]

MAX = 999999999

USE_COLORS = True

class Color:
    def __init__(self, red: int, green: int, blue: int):
        self.red = red if red < 255 else 255
        self.green = green if green < 255 else 255
        self.blue = blue if blue < 255 else 255

    def asRatioString(self) -> str:
        channels = [self.red, self.green, self.blue]
        return " ".join([str(int(x / 25.5) / 10) for x in channels])

def getColorString(triangle: Triangle):
    if USE_COLORS:
        if triangle.is_floor:
            if triangle.is_void:
                return Color(0, 0, 0).asRatioString()
            elif triangle.is_damage:
                return Color(122, 16, 19).asRatioString()
            elif triangle.is_water:
                return Color(52, 168, 235).asRatioString()
            elif triangle.is_instadeath:
                return Color(112, 16, 122).asRatioString()
        return Color(255, 255, 255).asRatioString()
    return ""

def write_obj_file(triangles, output_file):
    coordinate_order = [0, 1, 2]
    with open(output_file, 'w') as obj_file:
        for triangle in triangles:
            for x in range(3):
                obj_file.write(f'v {triangle.coords[x][coordinate_order[0]]} {triangle.coords[x][coordinate_order[1]]} {triangle.coords[x][coordinate_order[2]]} {getColorString(triangle)}\n')

        obj_file.write('o MyObject\n')
        
        for i in range(1, len(triangles) * 3 + 1, 3):
            obj_file.write(f'f {i} {i + 1} {i + 2}\n')

def handleMaps(file: str, dump: str, pointer_offset: int):
    with open(file, "rb") as fh:
        for map_index in range(216):
            total_tris = []
            for col in collision_info:
                counts = [getGeoRead(fh, x, 2, pointer_offset, map_index) for x in col.counts]
                compressed = getGeoRead(fh, 9, 1, pointer_offset, map_index) & col.compressed_bit
                tris = col.dumpTris(fh, map_index, pointer_offset, counts[0] * counts[1], compressed != 0)
                if len(tris) > 0:
                    total_tris.extend(tris)
                    raw_tris = [x.coords for x in tris]
                    raw_total_tris = [x.coords for x in total_tris]
                    directory = getSafeFolderName(f"{dump}/{maps[map_index]}/")
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                    write_obj_file(tris, f"{directory}/{col.name}.obj")
                    write_obj_file(total_tris, f"{directory}/Both.obj")
                
                        

def extractCollision():
    global folder_removal
    global main_pointer_table_offset
    global version

    file_path = getFilePath()
    main_pointer_table_offset, version, dump_path, valid = getROMData(file_path, "collision")
    if valid:
        handleMaps(file_path, dump_path, main_pointer_table_offset)
    # for map_index in range(216):
    #     if os.path.exists(f"{dump_path}/{maps[map_index]}"):
    #         os.remove(f"{dump_path}/{maps[map_index]}")
        
extractCollision()