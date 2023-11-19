import os
import zlib
import shutil
import gzip
from typing import BinaryIO
import math

from lib import getFilePath, getROMData, maps, getSafeFolderName, getSafeFileName, object_modeltwo_types

SHOW_FLOOR_UNUSED = False
SHOW_WALL_UNUSED = True
used_version = None

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
        if self.is_floor:
            self.is_void = (properties & 0x4000) != 0
            self.is_nonsolid = (properties & 0x800) != 0
            self.is_damage = (properties & 0x40) != 0
            self.is_instadeath = (properties & 0x10) != 0
            self.is_water = (properties & 0x1) != 0
        # Unused
        self.has_unused_floor = False
        if self.is_floor and ((properties & 0xB7AE) != 0):
            if SHOW_FLOOR_UNUSED:
                print(f"Triangle has unaccounted for properties {hex(properties & 0xB7AE)}")
            self.has_unused_floor = True
        # Wall Props
        if self.is_wall:
            self.is_solid = (properties & 0x10) != 0
        # Unused
        self.has_unused_wall = False
        if self.is_wall and ((properties & 0xFFEF) == 0) and properties not in (0x418, 0x8):
            if SHOW_WALL_UNUSED and properties != 0x18:
                print(f"Triangle has unaccounted for properties {hex(properties)}")
            self.has_unused_wall = True


class CollisionInfo:
    def __init__(self, pointer_table: int, name: str, count_0: int, count_1: int, compressed_bit: int, divisor: int):
        self.pointer_table = pointer_table
        self.name = name
        self.counts = [count_0, count_1]
        self.compressed_bit = compressed_bit
        self.divisor = divisor
        
    def dumpTris(self, fh: BinaryIO, map: int, pointer_offset: int, count: int, is_compressed: bool) -> list:
        meshes = []
        fh.seek(pointer_offset + (getPointerIndex(self.pointer_table) << 2))
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
                        if self.pointer_table == 3:
                            properties = int.from_bytes(fg.read(2), "big")
                            sfx = int.from_bytes(fg.read(2), "big")
                            brightness = int.from_bytes(fg.read(1), "big")
                            unk17 = int.from_bytes(fg.read(1), "big")
                        else:
                            angle = int.from_bytes(fg.read(2), "big")
                            is_fake_wall_0 = int.from_bytes(fg.read(1), "big")
                            is_fake_wall_1 = int.from_bytes(fg.read(1), "big")
                            properties = int.from_bytes(fg.read(2), "big")
                            sfx = 0
                            brightness = 0
                            unk17 = 0
                        mesh.append(Triangle(coord_set[0], coord_set[1], coord_set[2], properties, sfx, brightness, unk17, self.pointer_table))
                    meshes.append(mesh)
                    start = block_end + 4
        global_mesh = []
        for mesh in meshes:
            global_mesh.extend(mesh)
        return global_mesh
        
def getPointerIndex(index: int):
    if used_version == 3:
        return index - 1
    return index

folder_removal = []

def getGeoRead(fh: BinaryIO, offset: int, offset_size: int, pointer_offset: int, map: int):
    fh.seek(pointer_offset + (getPointerIndex(1) << 2))
    table_start = pointer_offset + int.from_bytes(fh.read(4), "big")
    fh.seek(table_start + (map << 2))
    map_start = pointer_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
    map_end = pointer_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
    map_size = map_end - map_start
    if map_size <= 0:
        return 0
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
            if triangle.has_unused_floor and SHOW_FLOOR_UNUSED:
                return Color(0, 255, 0).asRatioString()
            elif triangle.is_void:
                return Color(0, 0, 0).asRatioString()
            elif triangle.is_damage:
                return Color(122, 16, 19).asRatioString()
            elif triangle.is_water:
                return Color(52, 168, 235).asRatioString()
            elif triangle.is_instadeath:
                return Color(112, 16, 122).asRatioString()
        if triangle.is_wall:
            if triangle.has_unused_wall and SHOW_WALL_UNUSED:
                return Color(0, 255, 0).asRatioString()
            elif triangle.is_solid:
                return Color(52, 235, 174).asRatioString()  
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

def dumpObjTris(fh: BinaryIO, obj_index: int, pointer_offset: int) -> list:
    mesh = []
    fh.seek(pointer_offset + (getPointerIndex(4) << 2))
    table_start = pointer_offset + int.from_bytes(fh.read(4), "big")
    fh.seek(table_start + (obj_index << 2))
    file_start = pointer_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
    file_end = pointer_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
    file_size = file_end - file_start
    if file_size <= 0:
        return []
    fh.seek(file_start)
    compressed = int.from_bytes(fh.read(2), "big") == 0x1F8B
    fh.seek(file_start)
    file_data = fh.read(file_size)
    if compressed:
        file_data = zlib.decompress(file_data, (15 + 32))
    with open("temp.bin", "wb") as fg:
        fg.write(file_data)
    with open("temp.bin", "rb") as fg:
        # Walls
        fg.seek(0x4C)
        wall_start = int.from_bytes(fg.read(4), "big")
        fg.seek(wall_start)
        wall_tri_count = int.from_bytes(fg.read(4), "big")
        for x in range(wall_tri_count):
            fg.seek(wall_start + 4 + (0x16 * x))
            coord_set = []
            for vert in range(3):
                points = []
                for _ in range(3):
                    value = int.from_bytes(fg.read(2), "big")
                    if value > 32767:
                        value -= 65536
                    points.append(value)
                coord_set.append(points)
            adding = Triangle(coord_set[0], coord_set[1], coord_set[2], 0, 0, 0, 0, 4)
            mesh.append(adding)
        # Floors
        fg.seek(0x50)
        collision_start = int.from_bytes(fg.read(4), "big")
        fg.seek(collision_start)
        tri_count = int.from_bytes(fg.read(4), "big")
        for x in range(tri_count):
            fg.seek(collision_start + 0x10 + (0x18 * x))
            coord_set = []
            for vert in range(3):
                points = []
                for _ in range(3):
                    value = int.from_bytes(fg.read(2), "big")
                    if value > 32767:
                        value -= 65536
                    points.append(value)
                coord_set.append(points)
            mesh.append(Triangle(coord_set[0], coord_set[1], coord_set[2], 0, 0, 0, 0, 4))
    return mesh

DUMP_MAPS = True
DUMP_OBJS = True
TEST_OBJ = 685

def handleMaps(file: str, dump: str, pointer_offset: int):
    with open(file, "rb") as fh:
        if DUMP_MAPS:
            fh.seek(pointer_offset + ((getPointerIndex(1) + 32) << 2))
            limit = int.from_bytes(fh.read(4), "big")
            for map_index in range(limit):
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
        if DUMP_OBJS:
            fh.seek(pointer_offset + ((getPointerIndex(4) + 32) << 2))
            limit = int.from_bytes(fh.read(4), "big")
            for obj_index in range(limit): # 695
                tris = dumpObjTris(fh, obj_index, pointer_offset)
                if len(tris) > 0:
                    file_name = getSafeFileName(f"[{obj_index}] - {object_modeltwo_types[obj_index]}.obj")
                    write_obj_file(tris, f"{dump}/{file_name}")
                        

def extractCollision():
    global folder_removal
    global main_pointer_table_offset
    global used_version

    file_path = getFilePath()
    main_pointer_table_offset, version, dump_path, valid = getROMData(file_path, "collision")
    if valid:
        used_version = version
        handleMaps(file_path, dump_path, main_pointer_table_offset)
    # for map_index in range(216):
    #     if os.path.exists(f"{dump_path}/{maps[map_index]}"):
    #         os.remove(f"{dump_path}/{maps[map_index]}")
        
extractCollision()