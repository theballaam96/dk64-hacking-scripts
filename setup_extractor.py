import zlib
import os
import shutil
import tkinter as tk
from tkinter import filedialog
import json
import struct

root = tk.Tk()
root.withdraw()

maps = [
    "Test Map", # 0
    "Funky's Store",
    "DK Arcade",
    "K. Rool Barrel: Lanky's Maze",
    "Jungle Japes: Mountain",
    "Cranky's Lab",
    "Jungle Japes: Minecart",
    "Jungle Japes",
    "Jungle Japes: Army Dillo",
    "Jetpac",
    "Kremling Kosh! (very easy)", # 10
    "Stealthy Snoop! (normal, no logo)",
    "Jungle Japes: Shell",
    "Jungle Japes: Lanky's Cave",
    "Angry Aztec: Beetle Race",
    "Snide's H.Q.",
    "Angry Aztec: Tiny's Temple",
    "Hideout Helm",
    "Teetering Turtle Trouble! (very easy)",
    "Angry Aztec: Five Door Temple (DK)",
    "Angry Aztec: Llama Temple", # 20
    "Angry Aztec: Five Door Temple (Diddy)",
    "Angry Aztec: Five Door Temple (Tiny)",
    "Angry Aztec: Five Door Temple (Lanky)",
    "Angry Aztec: Five Door Temple (Chunky)",
    "Candy's Music Shop",
    "Frantic Factory",
    "Frantic Factory: Car Race",
    "Hideout Helm (Level Intros, Game Over)",
    "Frantic Factory: Power Shed",
    "Gloomy Galleon", # 30
    "Gloomy Galleon: K. Rool's Ship",
    "Batty Barrel Bandit! (very easy)",
    "Jungle Japes: Chunky's Cave",
    "DK Isles Overworld",
    "K. Rool Barrel: DK's Target Game",
    "Frantic Factory: Crusher Room",
    "Jungle Japes: Barrel Blast",
    "Angry Aztec",
    "Gloomy Galleon: Seal Race",
    "Nintendo Logo", # 40
    "Angry Aztec: Barrel Blast",
    "Troff 'n' Scoff", # 42
    "Gloomy Galleon: Shipwreck (Diddy, Lanky, Chunky)",
    "Gloomy Galleon: Treasure Chest",
    "Gloomy Galleon: Mermaid",
    "Gloomy Galleon: Shipwreck (DK, Tiny)",
    "Gloomy Galleon: Shipwreck (Lanky, Tiny)",
    "Fungi Forest",
    "Gloomy Galleon: Lighthouse",
    "K. Rool Barrel: Tiny's Mushroom Game", # 50
    "Gloomy Galleon: Mechanical Fish",
    "Fungi Forest: Ant Hill",
    "Battle Arena: Beaver Brawl!",
    "Gloomy Galleon: Barrel Blast",
    "Fungi Forest: Minecart",
    "Fungi Forest: Diddy's Barn",
    "Fungi Forest: Diddy's Attic",
    "Fungi Forest: Lanky's Attic",
    "Fungi Forest: DK's Barn",
    "Fungi Forest: Spider", # 60
    "Fungi Forest: Front Part of Mill",
    "Fungi Forest: Rear Part of Mill",
    "Fungi Forest: Mushroom Puzzle",
    "Fungi Forest: Giant Mushroom",
    "Stealthy Snoop! (normal)",
    "Mad Maze Maul! (hard)",
    "Stash Snatch! (normal)",
    "Mad Maze Maul! (easy)",
    "Mad Maze Maul! (normal)", # 69
    "Fungi Forest: Mushroom Leap", # 70
    "Fungi Forest: Shooting Game",
    "Crystal Caves",
    "Battle Arena: Kritter Karnage!",
    "Stash Snatch! (easy)",
    "Stash Snatch! (hard)",
    "DK Rap",
    "Minecart Mayhem! (easy)", # 77
    "Busy Barrel Barrage! (easy)",
    "Busy Barrel Barrage! (normal)",
    "Main Menu", # 80
    "Title Screen (Not For Resale Version)",
    "Crystal Caves: Beetle Race",
    "Fungi Forest: Dogadon",
    "Crystal Caves: Igloo (Tiny)",
    "Crystal Caves: Igloo (Lanky)",
    "Crystal Caves: Igloo (DK)",
    "Creepy Castle",
    "Creepy Castle: Ballroom",
    "Crystal Caves: Rotating Room",
    "Crystal Caves: Shack (Chunky)", # 90
    "Crystal Caves: Shack (DK)",
    "Crystal Caves: Shack (Diddy, middle part)",
    "Crystal Caves: Shack (Tiny)",
    "Crystal Caves: Lanky's Hut",
    "Crystal Caves: Igloo (Chunky)",
    "Splish-Splash Salvage! (normal)",
    "K. Lumsy",
    "Crystal Caves: Ice Castle",
    "Speedy Swing Sortie! (easy)",
    "Crystal Caves: Igloo (Diddy)", # 100
    "Krazy Kong Klamour! (easy)",
    "Big Bug Bash! (very easy)",
    "Searchlight Seek! (very easy)",
    "Beaver Bother! (easy)",
    "Creepy Castle: Tower",
    "Creepy Castle: Minecart",
    "Kong Battle: Battle Arena",
    "Creepy Castle: Crypt (Lanky, Tiny)",
    "Kong Battle: Arena 1",
    "Frantic Factory: Barrel Blast", # 110
    "Gloomy Galleon: Pufftoss",
    "Creepy Castle: Crypt (DK, Diddy, Chunky)",
    "Creepy Castle: Museum",
    "Creepy Castle: Library",
    "Kremling Kosh! (easy)",
    "Kremling Kosh! (normal)",
    "Kremling Kosh! (hard)",
    "Teetering Turtle Trouble! (easy)",
    "Teetering Turtle Trouble! (normal)",
    "Teetering Turtle Trouble! (hard)", # 120
    "Batty Barrel Bandit! (easy)",
    "Batty Barrel Bandit! (normal)",
    "Batty Barrel Bandit! (hard)",
    "Mad Maze Maul! (insane)",
    "Stash Snatch! (insane)",
    "Stealthy Snoop! (very easy)",
    "Stealthy Snoop! (easy)",
    "Stealthy Snoop! (hard)",
    "Minecart Mayhem! (normal)",
    "Minecart Mayhem! (hard)", # 130
    "Busy Barrel Barrage! (hard)",
    "Splish-Splash Salvage! (hard)",
    "Splish-Splash Salvage! (easy)",
    "Speedy Swing Sortie! (normal)",
    "Speedy Swing Sortie! (hard)",
    "Beaver Bother! (normal)",
    "Beaver Bother! (hard)",
    "Searchlight Seek! (easy)",
    "Searchlight Seek! (normal)",
    "Searchlight Seek! (hard)", # 140
    "Krazy Kong Klamour! (normal)",
    "Krazy Kong Klamour! (hard)",
    "Krazy Kong Klamour! (insane)",
    "Peril Path Panic! (very easy)",
    "Peril Path Panic! (easy)",
    "Peril Path Panic! (normal)",
    "Peril Path Panic! (hard)",
    "Big Bug Bash! (easy)",
    "Big Bug Bash! (normal)",
    "Big Bug Bash! (hard)", # 150
    "Creepy Castle: Dungeon",
    "Hideout Helm (Intro Story)",
    "DK Isles (DK Theatre)",
    "Frantic Factory: Mad Jack",
    "Battle Arena: Arena Ambush!",
    "Battle Arena: More Kritter Karnage!",
    "Battle Arena: Forest Fracas!",
    "Battle Arena: Bish Bash Brawl!",
    "Battle Arena: Kamikaze Kremlings!",
    "Battle Arena: Plinth Panic!", # 160
    "Battle Arena: Pinnacle Palaver!",
    "Battle Arena: Shockwave Showdown!",
    "Creepy Castle: Basement",
    "Creepy Castle: Tree",
    "K. Rool Barrel: Diddy's Kremling Game",
    "Creepy Castle: Chunky's Toolshed",
    "Creepy Castle: Trash Can",
    "Creepy Castle: Greenhouse",
    "Jungle Japes Lobby",
    "Hideout Helm Lobby", # 170
    "DK's House",
    "Rock (Intro Story)",
    "Angry Aztec Lobby",
    "Gloomy Galleon Lobby",
    "Frantic Factory Lobby",
    "Training Grounds",
    "Dive Barrel",
    "Fungi Forest Lobby",
    "Gloomy Galleon: Submarine",
    "Orange Barrel", # 180
    "Barrel Barrel",
    "Vine Barrel",
    "Creepy Castle: Crypt",
    "Enguarde Arena",
    "Creepy Castle: Car Race",
    "Crystal Caves: Barrel Blast",
    "Creepy Castle: Barrel Blast",
    "Fungi Forest: Barrel Blast",
    "Fairy Island",
    "Kong Battle: Arena 2", # 190
    "Rambi Arena",
    "Kong Battle: Arena 3",
    "Creepy Castle Lobby",
    "Crystal Caves Lobby",
    "DK Isles: Snide's Room",
    "Crystal Caves: Army Dillo",
    "Angry Aztec: Dogadon",
    "Training Grounds (End Sequence)",
    "Creepy Castle: King Kut Out",
    "Crystal Caves: Shack (Diddy, upper part)", # 200
    "K. Rool Barrel: Diddy's Rocketbarrel Game",
    "K. Rool Barrel: Lanky's Shooting Game",
    "K. Rool Fight: DK Phase",
    "K. Rool Fight: Diddy Phase",
    "K. Rool Fight: Lanky Phase",
    "K. Rool Fight: Tiny Phase",
    "K. Rool Fight: Chunky Phase",
    "Bloopers Ending",
    "K. Rool Barrel: Chunky's Hidden Kremling Game",
    "K. Rool Barrel: Tiny's Pony Tail Twirl Game", # 210
    "K. Rool Barrel: Chunky's Shooting Game",
    "K. Rool Barrel: DK's Rambi Game",
    "K. Lumsy Ending",
    "K. Rool's Shoe",
    "K. Rool's Arena", # 215
    "UNKNOWN 216",
    "UNKNOWN 217",
    "UNKNOWN 218",
    "UNKNOWN 219",
    "UNKNOWN 220",
    "UNKNOWN 221",
]

pointer_table_offsets = [0x101C50,0x1038D0,0x1039C0, 0x1A7C20]
main_pointer_table_offset = pointer_table_offsets[0]
folder_append = ["_us","_pal","_jp","_kiosk"]
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

def extractMaps(src_file: str):
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
                mapPath = f"map_setup{folder_append[version]}/{make_safe_filename(mapName)}"
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
    global pointer_table_offsets
    global main_pointer_table_offset
    global folder_append
    global version

    append = folder_append[0]

    # file_path = filedialog.askopenfilename()
    file_path = "dk64_kiosk.z64"
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
    if version < 0 or version > 3:
        print("Invalid version")
        exit()
    folder_removal = []
    dump_path = f"./map_setup{append}"
    if os.path.exists(dump_path):
        shutil.rmtree(dump_path)
    os.mkdir(f"./map_setup{append}")
    extractMaps(file_path)
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