from dk64_lib.rom import Rom
from dk64_lib.data_types.geometry import GeometryData
from dk64_lib.components.vertex import Vertex
import pathlib

# Makes some modifications to the library
# https://github.com/ThomasJRyan/dk64_lib

class Color:
    def __init__(self, red: int, green: int, blue: int, alpha: int = 0xFF):
        self.red = red if red < 255 else 255
        self.green = green if green < 255 else 255
        self.blue = blue if blue < 255 else 255
        self.alpha = alpha if alpha < 255 else 255

    def asRatioString(self) -> str:
        channels = [self.red, self.green, self.blue, self.alpha]
        return " ".join([str(int(x / 25.5) / 10) for x in channels])

def getVtxColor(vertex: Vertex) -> str:
    return Color(vertex.xr, vertex.yg, vertex.zb, vertex.alpha).asRatioString()

def create_obj(geo_table: GeometryData) -> str:
    """Creates an obj file out of the geometry data

    Returns:
        str: Obj file data
    """
    obj_data = str()
    tri_offset = 1

    if geo_table.is_pointer:
        return obj_data

    for dl_num, dl in enumerate(geo_table.display_lists, 1):
        if dl.is_branched:
            continue

        obj_data += f"# Display List {dl_num}, Offset: {dl.offset}\n\n"

        for group_num, (verticies, triangles) in enumerate(
            zip(dl.verticies, dl.triangles), 1
        ):

            obj_data += f"# Vertex Group {group_num}\n\n"

            # Write vertecies to file
            for vertex in verticies:
                obj_line = f"v {vertex.x} {vertex.y} {vertex.z} {getVtxColor(vertex)}\n"
                obj_data += obj_line
            obj_data += "\n"

            obj_data += f"# Triangle Group {group_num}\n\n"

            # Write triangles/faces to file
            for tri in triangles:
                obj_line = f"f {tri.v1 + tri_offset} {tri.v2 + tri_offset} {tri.v3 + tri_offset}\n"
                obj_data += obj_line
            obj_data += "\n"

            # The triangle offset is used to globally identify the vertex due to
            # Display Lists reading them with local positions
            tri_offset += len(verticies)
    return obj_data

def save_to_obj(geo_table, filename: str, folderpath: str = ".") -> None:
    """Save geometry data to obj format

    Args:
        filename (str): Name of obj file
        folderpath (str, optional): Folder path to save obj to. Defaults to ".".
    """
    filepath = pathlib.Path(folderpath, filename)
    with open(filepath, "w") as obj_file:
        obj_file.write(create_obj(geo_table))

def dump_geometry_map(map_index, rom_file: str, output_file: str):
    rom = Rom(rom_file)
    rom.REGIONS_AND_POINTER_TABLE_OFFSETS[0x47] = ("lodgenet", 0x1037C0)
    if len(rom.geometry_tables) <= map_index:
        return
    save_to_obj(rom.geometry_tables[map_index], output_file)