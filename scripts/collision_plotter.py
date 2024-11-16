import os
import zlib
import shutil
import gzip
import zipfile
from typing import BinaryIO
from enum import IntEnum, auto
import math

from lib import getFilePath, getROMData, maps, getSafeFolderName, getSafeFileName, object_modeltwo_types
from geo_dumper import dump_geometry_map
from geo_plotters import add_triggers_to_file

SHOW_FLOOR_UNUSED = False
SHOW_WALL_UNUSED = False
used_version = None

DUMP_ADDITIONAL_DATA = False

class TriangleNorms(IntEnum):
    Up = auto()
    Down = auto()
    XZParallel = auto()

def triangle_normal_facing(coord_set):
    # Unpack the coordinates
    (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = coord_set
    
    # Compute the vectors
    vector1 = (x2 - x1, y2 - y1, z2 - z1)
    vector2 = (x3 - x1, y3 - y1, z3 - z1)
    
    # Compute the cross product
    cross_product = (
        vector1[1] * vector2[2] - vector1[2] * vector2[1],
        vector1[2] * vector2[0] - vector1[0] * vector2[2],
        vector1[0] * vector2[1] - vector1[1] * vector2[0]
    )
    
    # Check the z-component of the cross product
    if cross_product[1] > 0:
        return TriangleNorms.Up
    elif cross_product[1] < 0:
        return TriangleNorms.Down
    else:
        return TriangleNorms.XZParallel

angle_data = [
    [
        0x8000,   0x7EBA,   0x7D74,   0x7C2D,
        0x7AE7,   0x79A0,   0x7859,   0x7711,
        0x75C9,   0x7480,   0x7337,   0x71EC,
        0x70A1,   0x6F55,   0x6E07,   0x6CB8,
        0x6B68,   0x6A17,   0x68C4,   0x6770,
        0x661A,   0x64C1,   0x6367,   0x620B,
        0x60AD,   0x5F4C,   0x5DE9,   0x5C83,
        0x5B1A,   0x59AE,   0x583E,   0x56CB,
        0x5555,   0x53DB,   0x525C,   0x50D9,
        0x4F51,   0x4DC5,   0x4C32,   0x4A9A,
        0x48FC,   0x4757,   0x45AB,   0x43F7,
        0x423A,   0x4075,   0x3EA5,   0x3CCB,
        0x3AE5,   0x38F1,   0x36EF,   0x34DC,
        0x32B7,   0x307D,   0x2E2B,   0x2BBD,
        0x292E,   0x2678,   0x2391,   0x206C,
        0x1CF6,   0x0000,
    ],
    [
        0x1CF6,   0x1CBB,   0x1C80,   0x1C45,
        0x1C08,   0x1BCC,   0x1B8F,   0x1B51,
        0x1B13,   0x1AD4,   0x1A95,   0x1A55,
        0x1A14,   0x19D3,   0x1992,   0x194F,
        0x190C,   0x18C9,   0x1884,   0x183F,
        0x17F9,   0x17B3,   0x176B,   0x1723,
        0x16DA,   0x1690,   0x1645,   0x15F9,
        0x15AC,   0x155E,   0x150F,   0x14BE,
        0x146D,   0x141A,   0x13C6,   0x1370,
        0x1319,   0x12C1,   0x1267,   0x120B,
        0x11AD,   0x114E,   0x10EC,   0x1088,
        0x1022,   0x0FB9,   0x0F4D,   0x0EDE,
        0x0E6C,   0x0DF7,   0x0D7D,   0x0D00,
        0x0C7D,   0x0BF4,   0x0B66,   0x0AD0,
        0x0A31,   0x0989,   0x08D3,   0x080E,
        0x0734,   0x063D,   0x0518,   0x039A,
    ],
    [
        0x039A,   0x031E,   0x028C,   0x01CD,
        0x0000,   0x0000,   0x0000,   0x0000,
        0x0000,   0x0000,   0x0000,   0x0000,
        0xFF00,   0x0000,   0x0000,   0x0000,
        0x0000,   0x0000,   0x0000,   0x0000,
        0x0000,   0x0000,   0x0000,   0x0000,
        0x0000,   0x0000
    ],
]

def getStickAngle_subd20(a):
    u = 7
    if a < 0x7FE0:
        u = 0x1FF
        if a < 0x7800:
            i = 9
            n = 0
        else:
            u = 0x1F
            i = 5
            n = 1
            a -= 0x7800
    else:
        i = 3
        n = 2
        a -= 0x7FE0
    t0 = angle_data[n][a >> i]
    t1 = angle_data[n][(a >> i) + 1]
    return t0 - (((t0 - t1) * (a & u)) >> i)



def getStickAngle_subda0(a):
    u = getStickAngle_subd20(abs(a))
    if a < 0:
        u = 0xFFFF - u
    return u & 0xFFFF

def getStickAngle_sub(a):
    if a >= 1:
        s = 0x7FFF
    else:
        if a <= -1:
            s = -0x7FFF
        else:
            s = a * 32767
    u = getStickAngle_subda0(int(s))
    return (u * math.pi) / 65535

def getStickAngle(y, x):
    if y == 0:
        return 0 if x >= 0 else math.pi
    elif x == 0:
        return (math.pi * 1.5) if y <= 0 else (math.pi / 2)
    f = math.sqrt((y * y) + (x * x))
    if x < y:
        f = getStickAngle_sub(x / f)
        if y < 0:
            f = (2 * math.pi) - f
    else:
        f = getStickAngle_sub(y / f)
        f = (math.pi / 2) - f
        if x < 0:
            f = math.pi - f
        if f < 0:
            f += (2 * math.pi)
    return f

SLOPE_TOLERANCES = [
    0x5A, 0x35, 0x2D, 0x2D,
    0x35, 0x2D, 0x5A, 0x5A,
    0x5A, 0x35, 0x4B, 0x4B,
    0x50, 0x00, 0x00, 0x14,
    0x19, 0x4B, 0x4B,
]

SLOPE_DIVISORS = [
    0x0001, 0x0020, 0x0020, 0x0020,
    0x0020, 0x0020, 0x0400, 0x0400,
    0x0400, 0x0020, 0x0008, 0x0010,
    0x0004, 0x0010, 0x0400, 0x0020,
    0x0020, 0x0008, 0x0008,
]

# Normal: 0x35
# 2: 0x2D
# 3: 0x2D
# 6: 0x5A
# 10: 0x4B
# 17: 0x4B
# 18: 0x4B

class SlipTypes(IntEnum):
    NonSlippery = auto()
    Slippery = auto()
    PersistSlip = auto()

def willSlip(coord_set: tuple, floor_type: int = 1, is_ostanding: bool = False):
    dx1 = coord_set[1][0] - coord_set[0][0]
    dx2 = coord_set[2][0] - coord_set[0][0]
    dy1 = coord_set[1][1] - coord_set[0][1]
    dy2 = coord_set[2][1] - coord_set[0][1]
    dz1 = coord_set[1][2] - coord_set[0][2]
    dz2 = coord_set[2][2] - coord_set[0][2]
    a1 = dy2 * dz1 - dy1 * dz2
    a2 = dz2 * dx1 - dz1 * dx2
    a3 = dx2 * dy1 - dx1 * dy2
    a = math.sqrt((a1 * a1) + (a3 * a3))
    if a < 0.01:
        return SlipTypes.NonSlippery
    cap = int((getStickAngle(abs(a2), a) / math.pi) * 2048)
    if is_ostanding:
        floor_type = 16
    slope_tolerance = SLOPE_TOLERANCES[floor_type]
    delta = 0x400 - cap
    dec_rate = int(delta / SLOPE_DIVISORS[floor_type])
    if cap < int((slope_tolerance << 0xC) / 0x168):
        if dec_rate == 0:
            return SlipTypes.PersistSlip
        return SlipTypes.Slippery
    return SlipTypes.NonSlippery

Y_CUTOFF = 1700
X_CUTOFF_MIN = 500
X_CUTOFF_MAX = 1000
Z_CUTOFF_MIN = 1000
Z_CUTOFF_MAX = 2000
SCALE_UP = 5
ISOLATE_SEGMENTS = False

def isValidCoordSet(coord_set: list) -> bool:
    """Returns whether the coordinate set is valid."""
    if not ISOLATE_SEGMENTS:
        return True
    for x in coord_set:
        if x[1] > Y_CUTOFF:
            if x[0] > X_CUTOFF_MIN and x[0] < X_CUTOFF_MAX:
                if x[2] > Z_CUTOFF_MIN and x[2] < Z_CUTOFF_MAX:
                    return True
    return False

def parseCoordSet(coord_set: list) -> list:
    """Alter the coord set based on special parameters."""
    if ISOLATE_SEGMENTS:
        for x in coord_set:
            x[1] -= Y_CUTOFF
            x[0] -= X_CUTOFF_MIN
            x[2] -= Z_CUTOFF_MIN
            x[0] *= SCALE_UP
            x[1] *= SCALE_UP
            x[2] *= SCALE_UP
    return coord_set

class DumpModes(IntEnum):
    # For floors only
    Null = auto()
    Properties = auto()
    Slip = auto()
    Slip_forceostandslip = auto()
    EnumerableType = auto()

class Triangle:
    def __init__(self, coord_set_0: list, coord_set_1: list, coord_set_2: list, properties: int, sfx: int, brightness: int, unk17: int, table: int, dump_mode: DumpModes, rgba: tuple = None):
        self.coords = (coord_set_0, coord_set_1, coord_set_2)
        self.properties = hex(properties)
        self.is_wall = table == 2
        self.is_floor = table == 3
        self.sfx = sfx
        self.brightness = brightness
        self.unk17 = unk17
        # Floor Props
        if self.is_floor:
            self.floor_dump_mode = dump_mode
            if dump_mode == DumpModes.Properties:
                self.is_void = (properties & 0x4000) != 0
                self.is_nonsolid = (properties & 0x800) != 0
                self.is_damage = (properties & 0x40) != 0
                self.is_instadeath = (properties & 0x10) != 0
                self.is_water = (properties & 0x1) != 0
            elif dump_mode in (DumpModes.Slip, DumpModes.Slip_forceostandslip):
                coord_set = (coord_set_0, coord_set_1, coord_set_2)
                self.force_slip = willSlip(coord_set, sfx >> 8, False) == SlipTypes.Slippery
                self.persist_slip = willSlip(coord_set, sfx >> 8, False) == SlipTypes.PersistSlip
                self.ostand_slip = willSlip(coord_set, sfx >> 8, dump_mode == DumpModes.Slip) == SlipTypes.Slippery
            elif dump_mode == DumpModes.EnumerableType:
                self.enumerable_type = sfx >> 8
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
        self.rgba = rgba

floor_max_y_data = {}
type_containers = {}

class CollisionInfo:
    def __init__(self, pointer_table: int, name: str, count_0: int, count_1: int, compressed_bit: int, divisor: int):
        self.pointer_table = pointer_table
        self.name = name
        self.counts = [count_0, count_1]
        self.compressed_bit = compressed_bit
        self.divisor = divisor
        
    def dumpTris(self, fh: BinaryIO, map: int, pointer_offset: int, count: int, is_compressed: bool, dump_mode: DumpModes = DumpModes.Null) -> list:
        highest_point = None
        highest_point_xyz = None
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
                        if self.pointer_table == 3:
                            # Ditch Ceilings
                            # if triangle_normal_facing(coord_set) == TriangleNorms.Down:
                            #     continue
                            if DUMP_ADDITIONAL_DATA:
                                max_y = max([x[1] for x in coord_set])
                                max_idx = None
                                for xi, x in enumerate(coord_set):
                                    if x[1] == max_y:
                                        max_idx = xi
                                if highest_point is None or max_y > highest_point:
                                    if triangle_normal_facing(coord_set) == TriangleNorms.Up and not willSlip(coord_set) and (properties & 0x4811) == 0:
                                        highest_point = max_y
                                        highest_point_xyz = coord_set[max_idx]
                                        # print(max_y, highest_point_xyz, coord_set, hex(properties), sfx >> 8, unk17)
                        allow_mesh_population = False
                        if dump_mode not in (DumpModes.Slip, DumpModes.EnumerableType):
                            allow_mesh_population = True
                        if triangle_normal_facing(coord_set) == TriangleNorms.Up and (properties & 0x4811) == 0:
                            allow_mesh_population = True
                        if dump_mode == DumpModes.EnumerableType:
                            en_type = sfx >> 8
                            if en_type != 1:
                                if en_type not in type_containers:
                                    type_containers[en_type] = []
                                if map not in type_containers[en_type]:
                                    type_containers[en_type].append(map)
                        if not isValidCoordSet(coord_set):
                            allow_mesh_population = False
                        else:
                            coord_set = parseCoordSet(coord_set)
                        applied_dump_mode = dump_mode
                        if dump_mode == DumpModes.Slip and map in (0xB7, 0x97):
                            # These two maps have a map property which bans Orangstand behaving normally
                            applied_dump_mode = DumpModes.Slip_forceostandslip
                        if allow_mesh_population:
                            mesh.append(Triangle(coord_set[0], coord_set[1], coord_set[2], properties, sfx, brightness, unk17, self.pointer_table, applied_dump_mode))
                    meshes.append(mesh)
                    start = block_end + 4
        global_mesh = []
        for mesh in meshes:
            global_mesh.extend(mesh)
        if self.pointer_table == 3 and DUMP_ADDITIONAL_DATA:
            floor_max_y_data[map] = {"y": highest_point, "xyz": highest_point_xyz}
        return global_mesh
    
class Vert:
    def __init__(self, coords: list, u: list, rgba: list):
        self.position = coords
        self.u = u
        self.rgba = rgba

class GeometryInfo:
    def __init__(self, pointer_table: int, name: str, ):
        self.pointer_table = pointer_table
        self.name = name
        self.divisor = 1

    def dumpTris(self, fh: BinaryIO, map: int, pointer_offset: int):
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
        meshes = []
        if map_size > 0:
            fh.seek(map_start)
            compressed = int.from_bytes(fh.read(2), "big") == 0x1F8B
            fh.seek(map_start)
            map_data = fh.read(map_size)
            if compressed:
                map_data = zlib.decompress(map_data, (15 + 32))
            with open("temp.bin","wb") as fg:
                fg.write(map_data)
            with open("temp.bin", "rb") as fg:
                verts = []
                vert_block_start = None
                vert_block_end = None
                chunk_count = None
                dl_layers = []
                vert_offsets = []
                vert_caps = []
                chunk_increments = []
                chunk_layers = []
                vert_cache = [None] * 32
                if self.pointer_table == 1:
                    fg.seek(0x34)
                    for _ in range(2):
                        dl_layers.append(int.from_bytes(fg.read(4), "big"))
                    fg.seek(0x38)
                    vert_block_start = int.from_bytes(fg.read(4), "big")
                    fg.seek(0x40)
                    vert_block_end = int.from_bytes(fg.read(4), "big")
                    fg.seek(0x64)
                    fg.seek(int.from_bytes(fg.read(4), "big"))
                    chunk_count = int.from_bytes(fg.read(4), "big")
                    if chunk_count == 0:
                        vert_offsets = [0]
                        vert_caps = [0xFFFFFFFF]
                        chunk_increments = [0xFFFFFFFF]
                    fg.seek(0x68)
                    chunk_rendering_offsets = int.from_bytes(fg.read(4), "big")
                    for x in range(chunk_count):
                        fg.seek(chunk_rendering_offsets + (0x34 * x) + 0x2C)
                        vert_offset = int.from_bytes(fg.read(4), "big")
                        vert_offsets.append(vert_offset)
                        vert_caps.append(vert_offset + int.from_bytes(fg.read(4), "big"))
                        layers_total = []
                        fg.seek(chunk_rendering_offsets + (0x34 * x) + 0xC)
                        max_layer_end = 0xFFFFFFFF
                        for y in range(4):
                            layer_start = int.from_bytes(fg.read(4), "big")
                            layer_size = int.from_bytes(fg.read(4), "big")
                            if layer_start != 0xFFFFFFFF:
                                max_layer_end = layer_start + layer_size
                                layers_total.append({
                                    "start": layer_start,
                                    "size": layer_size,
                                })
                            else:
                                layers_total.append(None)
                            if y == 3:
                                chunk_increments.append(max_layer_end)
                        chunk_layers.append(layers_total)
                    fg.seek(0x70)
                    dl_expansion_start = int.from_bytes(fg.read(4), "big")
                        
                    print(chunk_count)
                elif self.pointer_table == 4:
                    fg.seek(0x40)
                    for _ in range(3):
                        dl_layers.append(int.from_bytes(fg.read(4), "big"))
                    fg.seek(0x48)
                    vert_block_start = int.from_bytes(fg.read(4), "big")
                    vert_block_end = int.from_bytes(fg.read(4), "big")
                if vert_block_start is not None and vert_block_end is not None:
                    vert_block_size = int((vert_block_end - vert_block_start) / 0x10)
                    for x in range(vert_block_size):
                        fg.seek(vert_block_start + (x * 0x10))
                        coords = []
                        u = []
                        rgba = []
                        for _ in range(3):
                            value = int.from_bytes(fg.read(2), "big")
                            if value > 0x7FFF:
                                value -= 0x10000
                            coords.append(value / self.divisor)
                        for _ in range(3):
                            u.append(int.from_bytes(fg.read(2), "big"))
                        for _ in range(4):
                            rgba.append(int.from_bytes(fg.read(1), "big"))
                        verts.append(Vert(coords, u, rgba))
                    if len(dl_layers) > 1 and len(verts) > 0:
                        chunk_index = 0
                        if self.pointer_table == 1:
                            print("Starting chunk 0")
                            print([hex(x) for x in chunk_increments])
                        else:
                            print(map)
                        for mesh_index in range(len(dl_layers) - 1):
                            mesh = []
                            mesh_start = dl_layers[mesh_index]
                            mesh_end = dl_layers[mesh_index + 1]
                            instruction_count = int((mesh_end - mesh_start) / 8)
                            # print(instruction_count)
                            for x in range(instruction_count):
                                reading_position = mesh_start + (8 * x)
                                fg.seek(reading_position)
                                i_hi = int.from_bytes(fg.read(4), "big")
                                i_lo = int.from_bytes(fg.read(4), "big")
                                i_type = (i_hi >> 24) & 0xFF
                                if self.pointer_table == 1:
                                    if chunk_count > 1:
                                        if reading_position >= chunk_increments[chunk_index]:
                                            chunk_index += 1
                                            if chunk_index == chunk_count: # Not sure if this is the way to do it
                                                print("-", map, x, instruction_count, hex((instruction_count - x) * 8))
                                                break
                                    # print(f"Starting chunk {chunk_index}")
                                if i_type == 1:
                                    # G_VTX
                                    # print(hex(mesh_start + (8 * x)), hex(i_hi), hex(i_lo))
                                    i_vert_count = (i_hi >> 12) & 0xFF
                                    i_vert_buffer_end = i_hi & 0xFF
                                    i_vert_buffer_start = i_vert_buffer_end - (i_vert_count * 2)
                                    i_load_position = i_lo & 0xFFFFFF
                                    offset = 0
                                    vert_cap = 0xFFFFFFFFF
                                    if self.pointer_table == 1:
                                        offset = vert_offsets[chunk_index]
                                        vert_cap = vert_caps[chunk_index] >> 4
                                    i_load_vert = (i_load_position + offset) >> 4
                                    i_load_vert_end = min(i_load_vert + i_vert_count, vert_cap)
                                    verts_loaded = verts[i_load_vert: i_load_vert_end]                                    
                                    for yi, y in enumerate(verts_loaded):
                                        vert_cache[i_vert_buffer_start + yi] = y
                                elif i_type == 5:
                                    # G_TRI
                                    tri_buffer_positions = [
                                        ((i_hi >> 16) & 0xFF) >> 1,
                                        ((i_hi >> 8) & 0xFF) >> 1,
                                        ((i_hi >> 0) & 0xFF) >> 1,
                                    ]
                                    rgba = None
                                    tbp_count = 0
                                    tbp_sum = [0, 0, 0, 0]
                                    for tbp in (0, 1, 2):
                                        if vert_cache[tri_buffer_positions[tbp]].rgba is not None:
                                            tbp_count += 1
                                            for ch in range(4):
                                                tbp_sum[ch] += vert_cache[tri_buffer_positions[tbp]].rgba[ch]
                                    if tbp_count > 0:
                                        rgba = tbp_sum.copy()
                                        for ch in range(4):
                                            rgba[ch] = int(rgba[ch] / tbp_count)
                                    mesh.append(Triangle(
                                        vert_cache[tri_buffer_positions[0]].position,
                                        vert_cache[tri_buffer_positions[1]].position,
                                        vert_cache[tri_buffer_positions[2]].position,
                                        0,
                                        0,
                                        0,
                                        0,
                                        None,
                                        DumpModes.Null,
                                        rgba
                                    ))
                                elif i_type in (6, 7):
                                    # G_TRI2 / # G_QUAD
                                    tri_buffer_positions = [
                                        ((i_hi >> 16) & 0xFF) >> 1,
                                        ((i_hi >> 8) & 0xFF) >> 1,
                                        ((i_hi >> 0) & 0xFF) >> 1,
                                        ((i_lo >> 16) & 0xFF) >> 1,
                                        ((i_lo >> 8) & 0xFF) >> 1,
                                        ((i_lo >> 0) & 0xFF) >> 1,
                                    ]
                                    rgba = None
                                    tbp_count = 0
                                    tbp_sum = [0, 0, 0, 0]
                                    for tbp in (0, 1, 2):
                                        if vert_cache[tri_buffer_positions[tbp]].rgba is not None:
                                            tbp_count += 1
                                            for ch in range(4):
                                                tbp_sum[ch] += vert_cache[tri_buffer_positions[tbp]].rgba[ch]
                                    if tbp_count > 0:
                                        rgba = tbp_sum.copy()
                                        for ch in range(4):
                                            rgba[ch] = int(rgba[ch] / tbp_count)
                                    mesh.append(Triangle(
                                        vert_cache[tri_buffer_positions[0]].position,
                                        vert_cache[tri_buffer_positions[1]].position,
                                        vert_cache[tri_buffer_positions[2]].position,
                                        0,
                                        0,
                                        0,
                                        0,
                                        None,
                                        DumpModes.Null,
                                        rgba
                                    ))
                                    rgba = None
                                    tbp_count = 0
                                    tbp_sum = [0, 0, 0, 0]
                                    for tbp in (3, 4, 5):
                                        if vert_cache[tri_buffer_positions[tbp]].rgba is not None:
                                            tbp_count += 1
                                            for ch in range(4):
                                                tbp_sum[ch] += vert_cache[tri_buffer_positions[tbp]].rgba[ch]
                                    if tbp_count > 0:
                                        rgba = tbp_sum.copy()
                                        for ch in range(4):
                                            rgba[ch] = int(rgba[ch] / tbp_count)
                                    mesh.append(Triangle(
                                        vert_cache[tri_buffer_positions[3]].position,
                                        vert_cache[tri_buffer_positions[4]].position,
                                        vert_cache[tri_buffer_positions[5]].position,
                                        0,
                                        0,
                                        0,
                                        0,
                                        None,
                                        DumpModes.Null,
                                        rgba
                                    ))
                                elif i_type == 0xDF:
                                    meshes.append(mesh)
                                    mesh = []
                                # else:
                                #     # print(hex(i_type))
                            meshes.append(mesh)
        #global_mesh = meshes[0]
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
USE_VERTEX_COLORS = True

class Color:
    def __init__(self, red: int, green: int, blue: int, alpha: int = 0xFF):
        self.red = red if red < 255 else 255
        self.green = green if green < 255 else 255
        self.blue = blue if blue < 255 else 255
        self.alpha = alpha if alpha < 255 else 255

    def asRatioString(self) -> str:
        channels = [self.red, self.green, self.blue, self.alpha]
        return " ".join([str(int(x / 25.5) / 10) for x in channels])

def getColorString(triangle: Triangle):
    if USE_COLORS:
        if triangle.is_floor:
            if triangle.floor_dump_mode == DumpModes.Properties:
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
            elif triangle.floor_dump_mode in (DumpModes.Slip, DumpModes.Slip_forceostandslip):
                if triangle.force_slip:
                    if not triangle.ostand_slip:
                        return Color(0x21, 0xB5, 0xB8).asRatioString()
                    return Color(255, 0, 0).asRatioString()
                elif triangle.persist_slip:
                    return Color(0x89, 0x32, 0xA8).asRatioString()
            elif triangle.floor_dump_mode == DumpModes.EnumerableType:
                if triangle.enumerable_type == 2:  # Dungeon/Tree floor detection. Also used in other maps????
                    return Color(240, 128, 128).asRatioString() # LightCoral
                elif triangle.enumerable_type == 3:  # ?? - In painting/underground???
                    return Color(34, 139, 34).asRatioString() # ForestGreen
                elif triangle.enumerable_type == 6: # Sloped surfaces?
                    return Color(50, 205, 50).asRatioString() # LimeGreen
                elif triangle.enumerable_type == 10:  # Kong floor reflection
                    return Color(240, 230, 140).asRatioString() # Khaki
                elif triangle.enumerable_type == 17:  # Bananas (for the meme slip)
                    return Color(127, 255, 212).asRatioString() # Aquamarine
                elif triangle.enumerable_type == 18:  # is at the start of caves beetle race
                    return Color(255, 140, 0).asRatioString() # DarkOrange
                elif triangle.enumerable_type != 1:  # Unknown format
                    return Color(255, 0, 0).asRatioString()
        if triangle.is_wall:
            if triangle.has_unused_wall and SHOW_WALL_UNUSED:
                return Color(0, 255, 0).asRatioString()
            elif triangle.is_solid:
                return Color(52, 235, 174).asRatioString()
        if not triangle.is_wall and not triangle.is_floor:
            if USE_VERTEX_COLORS:
                rgba = triangle.rgba
                if rgba is not None:
                    return Color(rgba[0], rgba[1], rgba[2]).asRatioString()
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
            adding = Triangle(coord_set[0], coord_set[1], coord_set[2], 0, 0, 0, 0, 4, DumpModes.Null)
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
            mesh.append(Triangle(coord_set[0], coord_set[1], coord_set[2], 0, 0, 0, 0, 4, DumpModes.Null))
    return mesh

def createPack(dump_directory: str, path: str, is_directory: bool, new_name: str="", update_name: bool=False):
    files = [path]
    if is_directory:
        files = list(map(lambda x: os.path.join(os.path.abspath(path), x),os.listdir(path)))
        if path[-1] == "/":
            path = path[:-1]
    else:
        path = path.replace(".obj","")
    filename = path.split("/")[-1]
    if update_name:
        for fi, f in enumerate(files):
            data = None
            with open(f, "rb") as fh:
                data = fh.read()
            if data is not None:
                with open(new_name, "wb") as fh:
                    fh.write(data)
                files[fi] = new_name
    print(filename, len(files))
    if len(files) == 0:
        return
    with zipfile.ZipFile(f"{dump_directory}/{filename}.objzip", "w") as zipped_pack:
        for f in files:
            zipped_pack.write(f)
            if update_name:
                if os.path.exists(f):
                    os.remove(f)

DUMP_MAPS = True
DUMP_COLLISION = True
DUMP_OBJS = True
DUMP_GEOMETRY = True
CREATE_OBJ_PACKS = True
DUMP_EVENT_TRIGGERS = True
PACKS_DIR = "objzips"
TEST_OBJ = 685

MAP_GEO_INFO = GeometryInfo(1, "Map Geometry")
OBJ_GEO_INFO = GeometryInfo(4, "Object Geometry")

def handleMaps(file: str, dump: str, pointer_offset: int):
    pack_directory = f"{dump}/{PACKS_DIR}"
    if os.path.exists(pack_directory):
        shutil.rmtree(pack_directory)
    os.mkdir(pack_directory)
    # Kiosk Corrections
    MAP_GEO_INFO.pointer_table = getPointerIndex(1)
    OBJ_GEO_INFO.pointer_table = getPointerIndex(4)
    with open(file, "rb") as fh:
        if DUMP_MAPS:
            fh.seek(pointer_offset + ((getPointerIndex(1) + 32) << 2))
            limit = int.from_bytes(fh.read(4), "big")
            for map_index in range(limit):
                total_tris = []
                directory = getSafeFolderName(f"{dump}/{maps[map_index]}/")
                if DUMP_COLLISION:
                    for col in collision_info:
                        counts = [getGeoRead(fh, x, 2, pointer_offset, map_index) for x in col.counts]
                        compressed = getGeoRead(fh, 9, 1, pointer_offset, map_index) & col.compressed_bit
                        dump_mode = DumpModes.Properties if col.pointer_table == 3 else DumpModes.Null
                        tris = col.dumpTris(fh, map_index, pointer_offset, counts[0] * counts[1], compressed != 0, dump_mode)
                        if col.pointer_table == 3:
                            slip_tris = col.dumpTris(fh, map_index, pointer_offset, counts[0] * counts[1], compressed != 0, DumpModes.Slip)
                            en_tris = col.dumpTris(fh, map_index, pointer_offset, counts[0] * counts[1], compressed != 0, DumpModes.EnumerableType)
                        if len(tris) > 0:
                            total_tris.extend(tris)
                            if not os.path.exists(directory):
                                os.mkdir(directory)
                            write_obj_file(tris, f"{directory}/{col.name}.obj")
                            if col.pointer_table == 3:
                                write_obj_file(slip_tris, f"{directory}/Slippable Floors.obj")
                                write_obj_file(en_tris, f"{directory}/Enum Type Floors.obj")
                            write_obj_file(total_tris, f"{directory}/Walls and Floors.obj")
                if DUMP_GEOMETRY and used_version != 3:
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                    print(f"Creating Geometry Map for map {map_index}")
                    dump_geometry_map(map_index, file, f"{directory}/Geometry.obj")
                    if DUMP_EVENT_TRIGGERS:
                        add_triggers_to_file(fh, f"{directory}/Geometry.obj", map_index, pointer_offset)
                    # tris = MAP_GEO_INFO.dumpTris(fh, map_index, pointer_offset)
                    # if len(tris) > 0:
                    #     raw_tris = [x.coords for x in tris]
                    #     if not os.path.exists(directory):
                    #         os.mkdir(directory)
                    #     write_obj_file(tris, f"{directory}/Geometry.obj")
                if CREATE_OBJ_PACKS:
                    if os.path.exists(directory):
                        createPack(getSafeFolderName(f"{pack_directory}"), directory, True)
            if DUMP_ADDITIONAL_DATA:
                with open(f"{dump}/max_floors.txt", "w") as fk:
                    for map_idx in floor_max_y_data:
                        xyz = floor_max_y_data[map_idx]['xyz']
                        fk.write(f"{maps[map_idx]}:\n")
                        fk.write(f"- Y: {floor_max_y_data[map_idx]['y']}\n")
                        fk.write(f"- Achievable at: {xyz}\n")
                        if xyz is not None:
                            if xyz[0] is not None:
                                fk.write(f"- ScriptHawk: Game.setPosition({', '.join([str(a) for a in xyz])})\n\n")
        if DUMP_OBJS:
            fh.seek(pointer_offset + ((getPointerIndex(4) + 32) << 2))
            limit = int.from_bytes(fh.read(4), "big")
            obj_dump = f"{dump}/objects/"
            if os.path.exists(obj_dump):
                shutil.rmtree(obj_dump)
            os.mkdir(obj_dump)
            for obj_index in range(limit): # 695
                directory = getSafeFolderName(f"{obj_dump}/[{obj_index}] - {getSafeFileName(object_modeltwo_types[obj_index])}/")
                if not os.path.exists(directory):
                    os.mkdir(directory)
                if DUMP_COLLISION:
                    tris = dumpObjTris(fh, obj_index, pointer_offset)
                    if len(tris) > 0:
                        write_obj_file(tris, f"{directory}/Collision.obj")
                if DUMP_GEOMETRY:
                    tris = OBJ_GEO_INFO.dumpTris(fh, obj_index, pointer_offset)
                    if len(tris) > 0:
                        write_obj_file(tris, f"{directory}/Geometry.obj")
                if CREATE_OBJ_PACKS:
                    createPack(pack_directory, directory, True)
        print(type_containers)
                        

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