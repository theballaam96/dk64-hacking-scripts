import math
import zlib
import os
import shutil
from enum import IntEnum, auto

SCALE_UP = 3

class Maps(IntEnum):
    """Maps Enum."""

    TestMap = 0x0
    Funky = 0x1
    DKArcade = 0x2
    HelmBarrel_LankyMaze = 0x3
    JapesMountain = 0x4
    Cranky = 0x5
    JapesMinecart = 0x6
    Japes = 0x7
    JapesDillo = 0x8
    Jetpac = 0x9
    Kosh_VEasy = 0xA
    Snoop_NormalNoLogo = 0xB
    JapesShell = 0xC
    JapesPainting = 0xD
    AztecBeetle = 0xE
    Snide = 0xF
    AztecTinyTemple = 0x10
    Helm = 0x11
    Turtles_VEasy = 0x12
    Aztec5DTDK = 0x13
    AztecLlamaTemple = 0x14
    Aztec5DTDiddy = 0x15
    Aztec5DTTiny = 0x16
    Aztec5DTLanky = 0x17
    Aztec5DTChunky = 0x18
    Candy = 0x19
    Factory = 0x1A
    FactoryCarRace = 0x1B
    Helm_IntrosGameOver = 0x1C
    FactoryPowerShed = 0x1D
    Galleon = 0x1E
    GalleonSeasickShip = 0x1F
    BattyBarrel_VEasy = 0x20
    JapesUnderground = 0x21
    Isles = 0x22
    HelmBarrel_Target = 0x23
    FactoryCrusher = 0x24
    JapesBBlast = 0x25
    Aztec = 0x26
    GalleonSealRace = 0x27
    NintendoLogo = 0x28
    AztecBBlast = 0x29
    TroffNScoff = 0x2A
    Galleon5DSDiddyLankyChunky = 0x2B
    GalleonTreasureChest = 0x2C
    GalleonMermaid = 0x2D
    Galleon5DSDKTiny = 0x2E
    Galleon2DS = 0x2F
    Fungi = 0x30
    GalleonLighthouse = 0x31
    HelmBarrel_MushroomBounce = 0x32
    GalleonMechFish = 0x33
    FungiAntHill = 0x34
    BattleArena_BeaverBrawl = 0x35
    GalleonBBlast = 0x36
    FungiMinecart = 0x37
    FungiDiddyBarn = 0x38
    FungiDiddyAttic = 0x39
    FungiLankyAttic = 0x3A
    FungiDKBarn = 0x3B
    FungiSpider = 0x3C
    FungiMillFront = 0x3D
    FungiMillRear = 0x3E
    FungiMushroomSlam = 0x3F
    FungiGiantMushroom = 0x40
    Snoop_Normal = 0x41
    Maul_Hard = 0x42
    Snatch_Normal = 0x43
    Maul_Easy = 0x44
    Maul_Normal = 0x45
    FungiMushroomLeap = 0x46
    FungiShootingGame = 0x47
    Caves = 0x48
    BattleArena_KritterKarnage = 0x49
    Snatch_Easy = 0x4A
    Snatch_Hard = 0x4B
    DKRap = 0x4C
    MMayhem_Easy = 0x4D
    Barrage_Easy = 0x4E
    Barrage_Normal = 0x4F
    MainMenu = 0x50
    NFRTitleScreen = 0x51
    CavesBeetleRace = 0x52
    FungiDogadon = 0x53
    Caves5DITiny = 0x54
    Caves5DILanky = 0x55
    Caves5DIDK = 0x56
    Castle = 0x57
    CastleBallroom = 0x58
    CavesRotatingRoom = 0x59
    Caves5DCChunky = 0x5A
    Caves5DCDK = 0x5B
    Caves5DCDiddyLow = 0x5C
    Caves5DCTiny = 0x5D
    Caves1DC = 0x5E
    Caves5DIChunky = 0x5F
    Salvage_Normal = 0x60
    KLumsy = 0x61
    CavesTileFlip = 0x62
    Sortie_Easy = 0x63
    Caves5DIDiddy = 0x64
    Klamour_Easy = 0x65
    Bash_VEasy = 0x66
    Searchlight_VEasy = 0x67
    BBother_Easy = 0x68
    CastleTower = 0x69
    CastleMinecart = 0x6A
    MultiplayerBattleArena = 0x6B
    CastleCryptLankyTiny = 0x6C
    MultiplayerArena1 = 0x6D
    FactoryBBlast = 0x6E
    GalleonPufftoss = 0x6F
    CastleCryptDKDiddyChunky = 0x70
    CastleMuseum = 0x71
    CastleLibrary = 0x72
    Kosh_Easy = 0x73
    Kosh_Normal = 0x74
    Kosh_Hard = 0x75
    Turtles_Easy = 0x76
    Turtles_Normal = 0x77
    Turtles_Hard = 0x78
    BattyBarrel_Easy = 0x79
    BattyBarrel_Normal = 0x7A
    BattyBarrel_Hard = 0x7B
    Maul_Insane = 0x7C
    Snatch_Insane = 0x7D
    Snoop_VEasy = 0x7E
    Snoop_Easy = 0x7F
    Snoop_Hard = 0x80
    MMayhem_Normal = 0x81
    MMayhem_Hard = 0x82
    Barrage_Hard = 0x83
    Salvage_Hard = 0x84
    Salvage_Easy = 0x85
    Sortie_Normal = 0x86
    Sortie_Hard = 0x87
    BBother_Normal = 0x88
    BBother_Hard = 0x89
    Searchlight_Easy = 0x8A
    Searchlight_Normal = 0x8B
    Searchlight_Hard = 0x8C
    Klamour_Normal = 0x8D
    Klamour_Hard = 0x8E
    Klamour_Insane = 0x8F
    PPPanic_VEasy = 0x90
    PPPanic_Easy = 0x91
    PPPanic_Normal = 0x92
    PPPanic_Hard = 0x93
    Bash_Easy = 0x94
    Bash_Normal = 0x95
    Bash_Hard = 0x96
    CastleDungeon = 0x97
    Helm_IntroStory = 0x98
    Isles_DKTheatre = 0x99
    FactoryJack = 0x9A
    BattleArena_ArenaAmbush = 0x9B
    BattleArena_MoreKritterKarnage = 0x9C
    BattleArena_ForestFracas = 0x9D
    BattleArena_BishBashBrawl = 0x9E
    BattleArena_KamikazeKremlings = 0x9F
    BattleArena_PlinthPanic = 0xA0
    BattleArena_PinnaclePalaver = 0xA1
    BattleArena_ShockwaveShowdown = 0xA2
    CastleBasement = 0xA3
    CastleTree = 0xA4
    HelmBarrel_RandomKremling = 0xA5
    CastleShed = 0xA6
    CastleTrash = 0xA7
    CastleGreenhouse = 0xA8
    JapesLobby = 0xA9
    HelmLobby = 0xAA
    Treehouse = 0xAB
    Isles_IntroStoryRock = 0xAC
    AztecLobby = 0xAD
    GalleonLobby = 0xAE
    FactoryLobby = 0xAF
    TrainingGrounds = 0xB0
    TBarrel_Dive = 0xB1
    FungiLobby = 0xB2
    GalleonSubmarine = 0xB3
    TBarrel_Orange = 0xB4
    TBarrel_Barrel = 0xB5
    TBarrel_Vine = 0xB6
    CastleCrypt = 0xB7
    EnguardeArena = 0xB8
    CastleCarRace = 0xB9
    CavesBBlast = 0xBA
    CastleBBlast = 0xBB
    FungiBBlast = 0xBC
    FairyIsland = 0xBD
    MultiplayerArena2 = 0xBE
    RambiArena = 0xBF
    MultiplayerArena3 = 0xC0
    CastleLobby = 0xC1
    CavesLobby = 0xC2
    Isles_SnideRoom = 0xC3
    CavesDillo = 0xC4
    AztecDogadon = 0xC5
    TrainingGrounds_EndSequence = 0xC6
    CastleKutOut = 0xC7
    CavesShackDiddyHigh = 0xC8
    HelmBarrel_Rocketbarrel = 0xC9
    HelmBarrel_LankyShooting = 0xCA
    KRoolDK = 0xCB
    KRoolDiddy = 0xCC
    KRoolLanky = 0xCD
    KRoolTiny = 0xCE
    KRoolChunky = 0xCF
    BloopersEnding = 0xD0
    HelmBarrel_HiddenKremling = 0xD1
    HelmBarrel_FloorIsLava = 0xD2
    HelmBarrel_ChunkyShooting = 0xD3
    HelmBarrel_Rambi = 0xD4
    KLumsyEnding = 0xD5
    KRoolShoe = 0xD6
    KRoolArena = 0xD7

class Color:
    def __init__(self, red: int, green: int, blue: int, alpha: int = 0xFF):
        self.red = red if red < 255 else 255
        self.green = green if green < 255 else 255
        self.blue = blue if blue < 255 else 255
        self.alpha = alpha if alpha < 255 else 255

    def asRatioString(self) -> str:
        channels = [self.red, self.green, self.blue, self.alpha]
        return " ".join([str(int(x / 25.5) / 10) for x in channels])

def add_cylinder_to_obj(file_path: str, r, h, x=0.0, y=0.0, z=0.0, color: Color = Color(255, 0, 0, 10), segments=32):
    """
    Adds a cylinder to an existing .obj file at a specified position.

    Parameters:
        file_path (str): Path to the input .obj file.
        r (float): Radius of the cylinder.
        h (float): Height of the cylinder.
        x (float): X-coordinate of the cylinder's base center.
        y (float): Y-coordinate of the cylinder's base center.
        z (float): Z-coordinate of the cylinder's base center.
        segments (int): Number of segments for the cylinder's circular base.
    """
    
    x *= SCALE_UP
    y *= SCALE_UP
    z *= SCALE_UP
    r *= SCALE_UP
    h *= SCALE_UP
    r_outer = r
    r_inner = r

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Find the starting index for new vertices
    max_vertex_index = 0
    for line in lines:
        if line.startswith('v '):
            max_vertex_index += 1

    # Generate vertices
    vertices = []
    faces = []

    # Generate vertices for outer and inner circles
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        # Outer circle (bottom and top)
        vertices.append((x + r_outer * cos_a, y, z + r_outer * sin_a))  # Bottom outer
        vertices.append((x + r_outer * cos_a, y + h, z + r_outer * sin_a))  # Top outer
        # Inner circle (bottom and top)
        vertices.append((x + r_inner * cos_a, y, z + r_inner * sin_a))  # Bottom inner
        vertices.append((x + r_inner * cos_a, y + h, z + r_inner * sin_a))  # Top inner

    # Generate side faces
    for i in range(segments):
        next_i = (i + 1) % segments

        # Outer side faces
        faces.append((
            4 * i + 1, 4 * next_i + 1, 4 * next_i + 2, 4 * i + 2
        ))
        # Inner side faces (reversed for proper normals)
        faces.append((
            4 * i + 4, 4 * next_i + 4, 4 * next_i + 3, 4 * i + 3
        ))

    # Generate cap faces (top and bottom)
    for i in range(segments):
        next_i = (i + 1) % segments

        # Bottom cap (outer to inner)
        faces.append((
            4 * i + 1, 4 * next_i + 1, 4 * next_i + 3, 4 * i + 3
        ))
        # Top cap (outer to inner)
        faces.append((
            4 * i + 2, 4 * i + 4, 4 * next_i + 4, 4 * next_i + 2
        ))

    # Convert vertices and faces to OBJ format strings
    vertex_lines = [f"v {vx} {vy} {vz} {color.asRatioString()}\n" for vx, vy, vz in vertices]
    face_lines = [
        f"f {a + max_vertex_index} {b + max_vertex_index} {c + max_vertex_index} {d + max_vertex_index}\n"
        for a, b, c, d in faces
    ]

    # Append the new vertices and faces to the OBJ file
    with open(file_path, 'a') as f:
        f.writelines(vertex_lines)
        f.writelines(face_lines)

TRIGGER_TEMP_FILE = "temp_triggers.bin"

class TriggerGeneralTypes(IntEnum):
    LoadingZone = auto()
    Cutscene = auto()
    Autowalk = auto()
    State = auto()
    Weather = auto()
    ObjectControl = auto()
    Cheat = auto()
    Undefined = auto()

colors = {
    TriggerGeneralTypes.LoadingZone: 0xFF0000,
    TriggerGeneralTypes.Cutscene: 0x00FF00,
    TriggerGeneralTypes.Autowalk: 0x0000FF,
    TriggerGeneralTypes.State: 0xFF00FF,
    TriggerGeneralTypes.Weather: 0x00FFFF,
    TriggerGeneralTypes.ObjectControl: 0xFFFF00,
    TriggerGeneralTypes.Cheat: 0xFFFFFF,
    TriggerGeneralTypes.Undefined: 0x000000,
}

viewer_types = [
    TriggerGeneralTypes.ObjectControl, # 0x00: Spawn Trigger (0x12 - Character Spawner "Spawn Trigger")
    TriggerGeneralTypes.Undefined, # 0x01
    TriggerGeneralTypes.ObjectControl, # 0x02: Despawn Trigger (0x12 - Character Spawner "Spawn Trigger")
    TriggerGeneralTypes.ObjectControl, # 0x03: Boss Door Trigger
    TriggerGeneralTypes.ObjectControl, # 0x04: Update Actor Trigger (0x14 - Actor Spawner ID. Makes Rock fall in Fungi Minecart)
    TriggerGeneralTypes.Cutscene, # 0x05: Cutscene Trigger
    TriggerGeneralTypes.Weather, # 0x06: Weather Overlay Force Trigger (Spawns DK in treehouse?)
    TriggerGeneralTypes.Weather, # 0x07: Weather Overlay Set Trigger
    TriggerGeneralTypes.Weather, # 0x08: Weather Overlay Remove Trigger
    TriggerGeneralTypes.LoadingZone, # 0x09: Loading Zone
    TriggerGeneralTypes.Cutscene, # 0x0A: Cutscene Trigger
    TriggerGeneralTypes.ObjectControl, # 0x0B: Init TNT Minecart (Minecart Mayhem)
    TriggerGeneralTypes.LoadingZone, # 0x0C: Loading Zone + Objects
    TriggerGeneralTypes.LoadingZone, # 0x0D: Loading Zone
    TriggerGeneralTypes.Undefined, # 0x0E
    TriggerGeneralTypes.LoadingZone, # 0x0F: Warp Trigger
    TriggerGeneralTypes.LoadingZone, # 0x10: Loading Zone
    TriggerGeneralTypes.LoadingZone, # 0x11: Parent Map Loading Zone
    TriggerGeneralTypes.State, # 0x12: Coin Shower Trigger
    TriggerGeneralTypes.State, # 0x13: Detransform Trigger
    TriggerGeneralTypes.LoadingZone, # 0x14: Boss Door LZ
    TriggerGeneralTypes.Autowalk, # 0x15: Autowalk Trigger
    TriggerGeneralTypes.State, # 0x16: Sound Trigger
    TriggerGeneralTypes.Cutscene, # 0x17: Cutscene Trigger
    TriggerGeneralTypes.Undefined, # 0x18: In Fungi Minecart? Unsure on function
    TriggerGeneralTypes.Undefined, # 0x19: Everywhere in Seal Race. Unsure on function?
    TriggerGeneralTypes.State, # 0x1A: Gravity Trigger
    TriggerGeneralTypes.State, # 0x1B: Slide Trigger
    TriggerGeneralTypes.State, # 0x1C: Unslide Trigger
    TriggerGeneralTypes.LoadingZone, # 0x1D: Zipper Trigger
    TriggerGeneralTypes.State, # 0x1E: Song Trigger
    TriggerGeneralTypes.Undefined, # 0x1F
    TriggerGeneralTypes.Cutscene, # 0x20: Cutscene Trigger
    TriggerGeneralTypes.Undefined, # 0x21
    TriggerGeneralTypes.Undefined, # 0x22
    TriggerGeneralTypes.Undefined, # 0x23
    TriggerGeneralTypes.State, # 0x24: Detransform Trigger
    TriggerGeneralTypes.State, # 0x25: Load Chunk Textures Trigger
    TriggerGeneralTypes.Cheat, # 0x26: K. Lumsy Cheat Trigger
    TriggerGeneralTypes.State,  # 0x27: Destroy Object Trigger
]

extra_triggers = {
    
}

def add_triggers_to_file(fh, input_geo_obj, map_index, pointer_offset):
    if not os.path.exists(input_geo_obj):
        return
    fh.seek(pointer_offset + (18 * 4))
    trigger_tbl = pointer_offset + int.from_bytes(fh.read(4), "big")
    fh.seek(trigger_tbl + (map_index * 4))
    trigger_file_start = pointer_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
    trigger_file_end = pointer_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
    trigger_file_size = trigger_file_end - trigger_file_start
    if trigger_file_size <= 0:
        return
    fh.seek(trigger_file_start)
    data = zlib.decompress(fh.read(trigger_file_size), (15 + 32))
    with open(TRIGGER_TEMP_FILE, "wb") as fk:
        fk.write(data)
    triggers_to_plot =  []
    with open(TRIGGER_TEMP_FILE, "rb") as fk:
        count = int.from_bytes(fk.read(2), "big")
        for trigger in range(count):
            trigger_start = 2 + (trigger * 0x38)
            fk.seek(trigger_start)
            coords = []
            for i in range(3):
                coords.append(int.from_bytes(fk.read(2), "big"))
            radius = int.from_bytes(fk.read(2), "big")
            height = int.from_bytes(fk.read(2), "big")
            if height == 65535:
                height = 300
            fk.seek(trigger_start + 0x10)
            t_type = int.from_bytes(fk.read(2), "big")
            master_type = viewer_types[t_type]
            color_data = colors[master_type]
            blue = color_data & 0xFF
            green = (color_data >> 8) & 0xFF
            red = (color_data >> 16) & 0xFF
            # print(hex(t_type), master_type.name, hex(color_data), hex(red), hex(green), hex(blue))
            triggers_to_plot.append({
                "coords": coords,
                "radius": radius,
                "height": height,
                "color": Color(red, green, blue, 50),
            })
    output_geo_obj = input_geo_obj.replace("Geometry.obj", "Event Triggers.obj")
    shutil.copyfile(input_geo_obj, output_geo_obj)
    for trigger in triggers_to_plot:
        add_cylinder_to_obj(output_geo_obj, trigger["radius"], trigger["height"], trigger["coords"][0], trigger["coords"][1], trigger["coords"][2], trigger["color"])
    if os.path.exists(TRIGGER_TEMP_FILE):
        os.remove(TRIGGER_TEMP_FILE)