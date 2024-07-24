"""Script which contains some library functions for scripts."""
import os
import tkinter as tk
from tkinter import filedialog
import shutil
from enum import IntEnum, auto

root = tk.Tk()
root.withdraw()

class Version:
    def __init__(self, name: str, pointer_offset: int):
        self.name = name
        self.pointer_offset = pointer_offset

versions = [
    Version("us", 0x101C50),
    Version("pal", 0x1038D0),
    Version("jp", 0x1039C0),
    Version("kiosk", 0x1A7C20),
    Version("lodgenet", 0x1037C0),
]

class TextureFormats(IntEnum):
    Unknown = auto()
    RGBA5551 = auto()
    RGBA32 = auto()
    IA16 = auto()
    IA8 = auto()
    IA4 = auto()
    I16 = auto()
    I8 = auto()
    I4 = auto()
    CI8 = auto()
    CI4 = auto()
    BPP = auto()

class TextureFile:

    def __init__(self, name:str, format: TextureFormats, table: int, file_index: int, width: int, height: int, *, gif:list=[]):
        if name == "":
            self.name = f"TBL{table}_{file_index}_{width}_{height}"
        else:
            self.name = name
        self.table = table
        self.file_index = file_index
        self.format = format
        self.width = width
        self.height = height
        self.convert = format != TextureFormats.Unknown and width is not None and height is not None and width > 0 and height > 0
        self.gif_listing = gif

maps = [
    "Test Map",  # 0
    "Funky's Store",
    "DK Arcade",
    "K. Rool Barrel: Lanky's Maze",
    "Jungle Japes: Mountain",
    "Cranky's Lab",
    "Jungle Japes: Minecart",
    "Jungle Japes",
    "Jungle Japes: Army Dillo",
    "Jetpac",
    "Kremling Kosh! (very easy)",  # 10
    "Stealthy Snoop! (normal, no logo)",
    "Jungle Japes: Shell",
    "Jungle Japes: Lanky's Cave",
    "Angry Aztec: Beetle Race",
    "Snide's H.Q.",
    "Angry Aztec: Tiny's Temple",
    "Hideout Helm",
    "Teetering Turtle Trouble! (very easy)",
    "Angry Aztec: Five Door Temple (DK)",
    "Angry Aztec: Llama Temple",  # 20
    "Angry Aztec: Five Door Temple (Diddy)",
    "Angry Aztec: Five Door Temple (Tiny)",
    "Angry Aztec: Five Door Temple (Lanky)",
    "Angry Aztec: Five Door Temple (Chunky)",
    "Candy's Music Shop",
    "Frantic Factory",
    "Frantic Factory: Car Race",
    "Hideout Helm (Level Intros, Game Over)",
    "Frantic Factory: Power Shed",
    "Gloomy Galleon",  # 30
    "Gloomy Galleon: K. Rool's Ship",
    "Batty Barrel Bandit! (very easy)",
    "Jungle Japes: Chunky's Cave",
    "DK Isles Overworld",
    "K. Rool Barrel: DK's Target Game",
    "Frantic Factory: Crusher Room",
    "Jungle Japes: Barrel Blast",
    "Angry Aztec",
    "Gloomy Galleon: Seal Race",
    "Nintendo Logo",  # 40
    "Angry Aztec: Barrel Blast",
    "Troff 'n' Scoff",  # 42
    "Gloomy Galleon: Shipwreck (Diddy, Lanky, Chunky)",
    "Gloomy Galleon: Treasure Chest",
    "Gloomy Galleon: Mermaid",
    "Gloomy Galleon: Shipwreck (DK, Tiny)",
    "Gloomy Galleon: Shipwreck (Lanky, Tiny)",
    "Fungi Forest",
    "Gloomy Galleon: Lighthouse",
    "K. Rool Barrel: Tiny's Mushroom Game",  # 50
    "Gloomy Galleon: Mechanical Fish",
    "Fungi Forest: Ant Hill",
    "Battle Arena: Beaver Brawl!",
    "Gloomy Galleon: Barrel Blast",
    "Fungi Forest: Minecart",
    "Fungi Forest: Diddy's Barn",
    "Fungi Forest: Diddy's Attic",
    "Fungi Forest: Lanky's Attic",
    "Fungi Forest: DK's Barn",
    "Fungi Forest: Spider",  # 60
    "Fungi Forest: Front Part of Mill",
    "Fungi Forest: Rear Part of Mill",
    "Fungi Forest: Mushroom Puzzle",
    "Fungi Forest: Giant Mushroom",
    "Stealthy Snoop! (normal)",
    "Mad Maze Maul! (hard)",
    "Stash Snatch! (normal)",
    "Mad Maze Maul! (easy)",
    "Mad Maze Maul! (normal)",  # 69
    "Fungi Forest: Mushroom Leap",  # 70
    "Fungi Forest: Shooting Game",
    "Crystal Caves",
    "Battle Arena: Kritter Karnage!",
    "Stash Snatch! (easy)",
    "Stash Snatch! (hard)",
    "DK Rap",
    "Minecart Mayhem! (easy)",  # 77
    "Busy Barrel Barrage! (easy)",
    "Busy Barrel Barrage! (normal)",
    "Main Menu",  # 80
    "Title Screen (Not For Resale Version)",
    "Crystal Caves: Beetle Race",
    "Fungi Forest: Dogadon",
    "Crystal Caves: Igloo (Tiny)",
    "Crystal Caves: Igloo (Lanky)",
    "Crystal Caves: Igloo (DK)",
    "Creepy Castle",
    "Creepy Castle: Ballroom",
    "Crystal Caves: Rotating Room",
    "Crystal Caves: Shack (Chunky)",  # 90
    "Crystal Caves: Shack (DK)",
    "Crystal Caves: Shack (Diddy, middle part)",
    "Crystal Caves: Shack (Tiny)",
    "Crystal Caves: Lanky's Hut",
    "Crystal Caves: Igloo (Chunky)",
    "Splish-Splash Salvage! (normal)",
    "K. Lumsy",
    "Crystal Caves: Ice Castle",
    "Speedy Swing Sortie! (easy)",
    "Crystal Caves: Igloo (Diddy)",  # 100
    "Krazy Kong Klamour! (easy)",
    "Big Bug Bash! (very easy)",
    "Searchlight Seek! (very easy)",
    "Beaver Bother! (easy)",
    "Creepy Castle: Tower",
    "Creepy Castle: Minecart",
    "Kong Battle: Battle Arena",
    "Creepy Castle: Crypt (Lanky, Tiny)",
    "Kong Battle: Arena 1",
    "Frantic Factory: Barrel Blast",  # 110
    "Gloomy Galleon: Puftoss",
    "Creepy Castle: Crypt (DK, Diddy, Chunky)",
    "Creepy Castle: Museum",
    "Creepy Castle: Library",
    "Kremling Kosh! (easy)",
    "Kremling Kosh! (normal)",
    "Kremling Kosh! (hard)",
    "Teetering Turtle Trouble! (easy)",
    "Teetering Turtle Trouble! (normal)",
    "Teetering Turtle Trouble! (hard)",  # 120
    "Batty Barrel Bandit! (easy)",
    "Batty Barrel Bandit! (normal)",
    "Batty Barrel Bandit! (hard)",
    "Mad Maze Maul! (insane)",
    "Stash Snatch! (insane)",
    "Stealthy Snoop! (very easy)",
    "Stealthy Snoop! (easy)",
    "Stealthy Snoop! (hard)",
    "Minecart Mayhem! (normal)",
    "Minecart Mayhem! (hard)",  # 130
    "Busy Barrel Barrage! (hard)",
    "Splish-Splash Salvage! (hard)",
    "Splish-Splash Salvage! (easy)",
    "Speedy Swing Sortie! (normal)",
    "Speedy Swing Sortie! (hard)",
    "Beaver Bother! (normal)",
    "Beaver Bother! (hard)",
    "Searchlight Seek! (easy)",
    "Searchlight Seek! (normal)",
    "Searchlight Seek! (hard)",  # 140
    "Krazy Kong Klamour! (normal)",
    "Krazy Kong Klamour! (hard)",
    "Krazy Kong Klamour! (insane)",
    "Peril Path Panic! (very easy)",
    "Peril Path Panic! (easy)",
    "Peril Path Panic! (normal)",
    "Peril Path Panic! (hard)",
    "Big Bug Bash! (easy)",
    "Big Bug Bash! (normal)",
    "Big Bug Bash! (hard)",  # 150
    "Creepy Castle: Dungeon",
    "Hideout Helm (Intro Story)",
    "DK Isles (DK Theatre)",
    "Frantic Factory: Mad Jack",
    "Battle Arena: Arena Ambush!",
    "Battle Arena: More Kritter Karnage!",
    "Battle Arena: Forest Fracas!",
    "Battle Arena: Bish Bash Brawl!",
    "Battle Arena: Kamikaze Kremlings!",
    "Battle Arena: Plinth Panic!",  # 160
    "Battle Arena: Pinnacle Palaver!",
    "Battle Arena: Shockwave Showdown!",
    "Creepy Castle: Basement",
    "Creepy Castle: Tree",
    "K. Rool Barrel: Diddy's Kremling Game",
    "Creepy Castle: Chunky's Toolshed",
    "Creepy Castle: Trash Can",
    "Creepy Castle: Greenhouse",
    "Jungle Japes Lobby",
    "Hideout Helm Lobby",  # 170
    "DK's House",
    "Rock (Intro Story)",
    "Angry Aztec Lobby",
    "Gloomy Galleon Lobby",
    "Frantic Factory Lobby",
    "Training Grounds",
    "Dive Barrel",
    "Fungi Forest Lobby",
    "Gloomy Galleon: Submarine",
    "Orange Barrel",  # 180
    "Barrel Barrel",
    "Vine Barrel",
    "Creepy Castle: Crypt",
    "Enguarde Arena",
    "Creepy Castle: Car Race",
    "Crystal Caves: Barrel Blast",
    "Creepy Castle: Barrel Blast",
    "Fungi Forest: Barrel Blast",
    "Fairy Island",
    "Kong Battle: Arena 2",  # 190
    "Rambi Arena",
    "Kong Battle: Arena 3",
    "Creepy Castle Lobby",
    "Crystal Caves Lobby",
    "DK Isles: Snide's Room",
    "Crystal Caves: Army Dillo",
    "Angry Aztec: Dogadon",
    "Training Grounds (End Sequence)",
    "Creepy Castle: King Kut Out",
    "Crystal Caves: Shack (Diddy, upper part)",  # 200
    "K. Rool Barrel: Diddy's Rocketbarrel Game",
    "K. Rool Barrel: Lanky's Shooting Game",
    "K. Rool Fight: DK Phase",
    "K. Rool Fight: Diddy Phase",
    "K. Rool Fight: Lanky Phase",
    "K. Rool Fight: Tiny Phase",
    "K. Rool Fight: Chunky Phase",
    "Bloopers Ending",
    "K. Rool Barrel: Chunky's Hidden Kremling Game",
    "K. Rool Barrel: Tiny's Pony Tail Twirl Game",  # 210
    "K. Rool Barrel: Chunky's Shooting Game",
    "K. Rool Barrel: DK's Rambi Game",
    "K. Lumsy Ending",
    "K. Rool's Shoe",
    "K. Rool's Arena",  # 215
    "UNKNOWN 216",
    "UNKNOWN 217",
    "UNKNOWN 218",
    "UNKNOWN 219",
    "UNKNOWN 220",
    "UNKNOWN 221",
]

object_modeltwo_types = [
	"Nothing", # "test" internal name
	"Thin Flame?", # 2D
	"-",
	"Tree", # 2D
	"-",
	"Yellow Flowers", # 2D
	"-",
	"-",
	"Xmas Holly?", # 2D
	"-",
	"CB Single (Diddy)",
	"Large Wooden Panel", # 2D
	"Flames", # 2D
	"CB Single (DK)",
	"Large Iron Bars Panel", # 2D
	"Goo Hand", # Castle
	"Flame", # 2D
	"Homing Ammo Crate",
	"Coffin Door",
	"Coffin Lid",
	"Skull", # Castle, it has a boulder in it
	"Wooden Crate",
	"CB Single (Tiny)",
	"Shield", # Castle
	"Metal thing",
	"Coffin",
	"Metal Panel",
	"Rock Panel",
	"Banana Coin (Tiny)",
	"Banana Coin (DK)",
	"CB Single (Lanky)",
	"CB Single (Chunky)",
	"Tree", # Japes?
	"-",
	"Metal Panel",
	"Banana Coin (Lanky)",
	"Banana Coin (Diddy)",
	"Metal Panel",
	"Metal Panel Red",
	"Banana Coin (Chunky)",
	"Metal Panel Grey",
	"Tree", # Japes?
	"-",
	"CB Bunch (DK)",
	"Hammock",
	"Small jungle bush plant",
	"-",
	"Small plant",
	"Bush", # Japes
	"-",
	"-",
	"-", # Fungi Lobby, Unknown
	"Metal Bridge", # Helm Lobby
	"Large Blue Crystal", # Crystal Caves Lobby
	"Plant",
	"Plant",
	"-",
	"White Flowers",
	"Stem 4 Leaves",
	"-",
	"-",
	"Small plant",
	"-",
	"-",
	"-",
	"-",
	"-",
	"Yellow Flower",
	"Blade of Grass Large",
	"Lilypad?",
	"Plant",
	"Iron Bars", # Castle Lobby Coconut Switch
	"Nintendo Coin", # Not sure if this is collectable
	"Metal Floor",
	"-",
	"-",
	"Bull Rush",
	"-",
	"-",
	"Metal box/platform",
	"K Crate", # DK Helm Target Barrel
	"-",
	"Wooden panel",
	"-",
	"-",
	"-",
	"Orange",
	"Watermelon Slice",
	"Tree", # Unused?
	"Tree", # Unused
	"Tree",
	"Tree (Black)", # Unused
	"-",
	"Light Green platform",
	"-",
	"-",
	"-",
	"-",
	"Brick Wall",
	"-",
	"-",
	"-",
	"-",
	"Wrinkly Door (Tiny)",
	"-",
	"-",
	"-",
	"Conveyor Belt",
	"Tree", # Japes?
	"Tree",
	"Tree",
	"-",
	"Primate Punch Switch", # Factory
	"Hi-Lo toggle machine",
	"Breakable Metal Grate", # Factory
	"Cranky's Lab",
	"Golden Banana",
	"Metal Platform",
	"Metal Bars",
	"-",
	"Metal fence",
	"Snide's HQ",
	"Funky's Armory",
	"-",
	"Blue lazer field",
	"-",
	"Bamboo Gate",
	"-",
	"Tree Stump",
	"Breakable Hut", # Japes
	"Mountain Bridge", # Japes
	"Tree Stump", # Japes
	"Bamboo Gate",
	"-",
	"Blue/green tree",
	"-",
	"Mushroom",
	"-",
	"Disco Ball",
	"2 Door (5DS)", # Galleon
	"3 Door (5DS)", # Galleon
	"Map of DK island",
	"Crystal Coconut",
	"Ammo Crate",
	"Banana Medal",
	"Peanut",
	"Simian Slam Switch (Chunky, Green)",
	"Simian Slam Switch (Diddy, Green)",
	"Simian Slam Switch (DK, Green)",
	"Simian Slam Switch (Lanky, Green)",
	"Simian Slam Switch (Tiny, Green)",
	"Baboon Blast Pad",
	"Film",
	"Chunky Rotating Room", # Aztec, Tiny Temple
	"Stone Monkey Face",
	"Stone Monkey Face",
	"Aztec Panel blue",
	"-", # templestuff, in Tiny Temple
	"Ice Floor",
	"Ice Pole", # I think this is a spotlight
	"Big Blue wall panel",
	"Big Blue wall panel",
	"Big Blue wall panel",
	"Big Blue wall panel",
	"KONG Letter (K)",
	"KONG Letter (O)",
	"KONG Letter (N)",
	"KONG Letter (G)",
	"Bongo Pad", # DK
	"Guitar Pad", # Diddy
	"Saxaphone Pad", # Tiny
	"Triangle Pad", # Chunky
	"Trombone Pad", # Lanky
	"Wood panel small",
	"Wood panel small",
	"Wood panel small",
	"Wood Panel small",
	"Wall Panel", # Aztec
	"Wall Panel", # Caves?
	"Stone Monkey Face (Not Solid)",
	"Feed Me Totem", # Aztec
	"Melon Crate",
	"Lava Platform", # Aztec, Llama temple
	"Rainbow Coin",
	"Green Switch",
	"Coconut Indicator", # Free Diddy
	"Snake Head", # Aztec, Llama temple
	"Matching Game Board", # Aztec, Llama temple
	"Stone Monkey Head", # Aztec
	"Large metal section",
	"Production Room Crusher", # Factory
	"Metal Platform",
	"Metal Object",
	"Metal Object",
	"Metal Object",
	"Gong", # Diddy Kong
	"Platform", # Aztec
	"Bamboo together",
	"Metal Bars",
	"Target", # Minigames
	"Wooden object",
	"Ladder",
	"Ladder",
	"Wooden pole",
	"Blue panel",
	"Ladder",
	"Grey Switch",
	"D Block for toy world",
	"Hatch (Factory)",
	"Metal Bars",
	"Raisable Metal Platform",
	"Metal Cage",
	"Simian Spring Pad",
	"Power Shed", # Factory
	"Metal platform",
	"Sun Lighting effect panel",
	"Wooden Pole",
	"Wooden Pole",
	"Wooden Pole",
	"-",
	"Question Mark Box",
	"Blueprint (Tiny)",
	"Blueprint (DK)",
	"Blueprint (Chunky)",
	"Blueprint (Diddy)",
	"Blueprint (Lanky)",
	"Tree Dark",
	"Rope",
	"-",
	"-",
	"Lever",
	"Green Croc Head (Minecart)",
	"Metal Gate with red/white stripes",
	"-",
	"Purple Croc Head (Minecart)",
	"Wood panel",
	"DK coin",
	"Wooden leg",
	"-",
	"Wrinkly Door (Lanky)",
	"Wrinkly Door (DK)",
	"Wrinkly Door (Chunky)",
	"Wrinkly Door (Diddy)",
	"Torch",
	"Number Game (1)", # Factory
	"Number Game (2)", # Factory
	"Number Game (3)", # Factory
	"Number Game (4)", # Factory
	"Number Game (5)", # Factory
	"Number Game (6)", # Factory
	"Number Game (7)", # Factory
	"Number Game (8)", # Factory
	"Number Game (9)", # Factory
	"Number Game (10)", # Factory
	"Number Game (11)", # Factory
	"Number Game (12)", # Factory
	"Number Game (13)", # Factory
	"Number Game (14)", # Factory
	"Number Game (15)", # Factory
	"Number Game (16)", # Factory
	"Bad Hit Detection Wheel", # Factory
	"Breakable Gate", # Galleon Primate Punch
	"-",
	"Picture of DK island",
	"White flashing thing",
	"Barrel", # Galleon Ship
	"Gorilla Gone Pad",
	"Monkeyport Pad",
	"Baboon Balloon Pad",
	"Light", # Factory?
	"Light", # Factory?
	"Barrel", # Galleon Ship
	"Barrel", # Galleon Ship
	"Barrel", # Galleon Ship
	"Barrel", # Galleon Ship
	"Pad", # TODO: Empty blue pad? Where is this used?
	"Red Light", # Factory?
	"Breakable X Panel", # To enter Japes underground
	"Power Shed Screen", # Factory
	"Crusher", # Factory
	"Floor Panel",
	"Metal floor panel mesh",
	"Metal Door", # Factory or Car Race
	"Metal Door", # Factory or Car Race
	"Metal Door", # Factory or Car Race
	"Metal Door", # Factory or Car Race
	"Metal Door", # Factory or Car Race
	"Metal Door", # Factory or Car Race
	"Toyz Box",
	"O Pad", # Aztec Chunky Puzzle
	"Bonus Barrel Trap", # Aztec
	"Sun Idol", # Aztec, top of "feed me" totem
	"Candy's Shop",
	"Pineapple Switch",
	"Peanut Switch",
	"Feather Switch",
	"Grape Switch",
	"Coconut Switch",
	"-",
	"Kong Pad",
	"Boss Door", # Troff'n'Scoff
	"Troff n Scoff Feed Pad",
	"Metal Bars horizontal",
	"Metal Bars",
	"Harbour Gate", # Galleon
	"K. Rool's Ship", # Galleon
	"Metal Platform",
	"-",
	"Flame",
	"Flame",
	"Scoff n Troff platform",
	"Troff n Scoff Banana Count Pad (DK)",
	"Torch",
	"-",
	"-",
	"-",
	"Boss Key",
	"Machine",
	"Metal Door", # Factory or Car Race - Production Room & Lobby - Unused?
	"Metal Door", # Factory or Car Race - Testing Dept. & Krem Storage
	"Metal Door", # Factory or Car Race - R&D
	"Metal Door", # Factory or Car Race - Testing Dept.
	"Piano Game", # Factory, Lanky
	"Troff n Scoff Banana Count Pad (Diddy)",
	"Troff n Scoff Banana Count Pad (Lanky)",
	"Troff n Scoff Banana Count Pad (Chunky)",
	"Troff n Scoff Banana Count Pad (Tiny)",
	"Door 1342",
	"Door 3142",
	"Door 4231",
	"1 Switch (Red)",
	"2 Switch (Blue)",
	"3 Switch (Orange)",
	"4 Switch (Green)",
	"-",
	"Metal Archway",
	"Green Crystal thing",
	"Red Crystal thing",
	"Propeller",
	"Large Metal Bar",
	"Ray Sheild?",
	"-",
	"-",
	"-",
	"-",
	"Light",
	"Target", # Fungi/Castle minigames
	"Ladder",
	"Metal Bars",
	"Red Feather",
	"Grape",
	"Pinapple",
	"Coconut",
	"Rope",
	"On Button",
	"Up Button",
	"Metal barrel or lid",
	"Simian Slam Switch (Chunky, Red)",
	"Simian Slam Switch (Diddy, Red)",
	"Simian Slam Switch (DK, Red)",
	"Simian Slam Switch (Lanky, Red)",
	"Simian Slam Switch (Tiny, Red)",
	"Simian Slam Switch (Chunky, Blue)",
	"Simian Slam Switch (Diddy, Blue)",
	"Simian Slam Switch (DK, Blue)",
	"Simian Slam Switch (Lanky, Blue)",
	"Simian Slam Switch (Tiny, Blue)",
	"Metal Grate", # Lanky Attic
	"Pendulum", # Fungi Clock
	"Weight", # Fungi Clock
	"Door", # Fungi Clock
	"Day Switch", # Fungi Clock
	"Night Switch", # Fungi Clock
	"Hands", # Fungi Clock
	"Bell", # (Minecart?)
	"Grate", # (Minecart?)
	"Crystal", # Red - No Hitbox (Minecart)
	"Crystal", # Blue - No Hitbox (Minecart)
	"Crystal", # Green - No Hitbox (Minecart)
	"Door", # Fungi
	"Gate", # Fungi, angled
	"Breakable Door", # Fungi
	"Night Gate", # Fungi, angled
	"Night Grate", # Fungi
	"Unknown", # Internal name is "minecart"
	"Metal Grate", # Fungi, breakable, well
	"Mill Pulley Mechanism", # Fungi
	"Metal Bar", # No Hitbox (Unknown Location)
	"Water Wheel", # Fungi
	"Crusher", # Fungi Mill
	"Coveyor Belt",
	"Night Gate",
	"Question Mark Box", # Factory Lobby, probably other places too
	"Spider Web", # Door
	"Grey Croc Head", # Minecart?
	"Caution Sign (Falling Rocks)", # Minecart
	"Door", # Minecart
	"Battle Crown",
	"-",
	"-",
	"Dogadon Arena Background",
	"Skull Door (Small)", # Minecart
	"Skull Door (Big)", # Minecart
	"-",
	"Tombstone", # RIP, Minecart
	"-",
	"DK Star", # Baboon Blast
	"K. Rool's Throne",
	"Bean", # Fungi
	"Power Beam", # Helm (Lanky - BoM)
	"Power Beam", # Helm (Diddy - BoM)
	"Power Beam", # Helm (Tiny - Medal Room)
	"Power Beam", # Helm (Tiny - BoM)
	"Power Beam", # Helm (Chunky - Medal Room)
	"Power Beam", # Helm (Chunky - BoM)
	"Power Beam", # Helm (Lanky - Medal Room)
	"Power Beam", # Helm (DK - Medal Room)
	"Power Beam", # Helm (DK - BoM)
	"Power Beam", # Helm (Diddy - Medal Room)
	"Warning Lights", # Helm Wheel Room
	"K. Rool Door", # Helm
	"Metal Grate",
	"Crown Door", # Helm
	"Coin Door", # Helm
	"Medal Barrier (DK)", # Helm
	"Medal Barrier (Diddy)", # Helm
	"Medal Barrier (Tiny)", # Helm
	"Medal Barrier (Chunky)", # Helm
	"Medal Barrier (Lanky)", # Helm
	"I Door (Helm, DK)",
	"V Door (Helm, Diddy)",
	"III Door (Helm, Tiny)",
	"II Door (Helm, Chunky)",
	"IV Door (Helm, Lanky)",
	"Metal Door", # Helm CS
	"Stone Wall", # Helm
	"Pearl", # Galleon
	"Small Door", # Fungi
	"-",
	"Cloud", # Castle, Fungi?
	"Warning Lights", # Crusher/Grinder
	"Door", # Fungi
	"Mushroom (Yellow)",
	"Mushroom (Purple)",
	"Mushroom (Blue)",
	"Mushroom (Green)",
	"Mushroom (Red)",
	"Mushroom Puzzle Instructions",
	"Face Puzzle Board", # Fungi
	"Mushroom", # Climbable, Fungi
	"Small Torch", # Internal name "test", interestingly
	"DK Arcade Machine",
	"Simian Slam Switch (Any Kong?)", # Mad Jack fight
	"Spotlight (Crown Arena?)",
	"Battle Crown Pad",
	"Seaweed",
	"Light", # Galleon Lighthouse
	"Dust?",
	"Moon Trapdoor", # Fungi
	"Ladder", # Fungi
	"Mushroom Board", # 5 gunswitches, Fungi
	"DK Star",
	"Wooden Box", # Galleon?
	"Yellow CB Powerup", # Multiplayer
	"Blue CB Powerup", # Multiplayer
	"Coin Powerup?", # Multiplayer, causes burp
	"DK Coin", # Multiplayer?
	"Snide's Mechanism",
	"Snide's Mechanism",
	"Snide's Mechanism",
	"Snide's Mechanism",
	"Snide's Mechanism",
	"Snide's Mechanism",
	"Snide's Mechanism",
	"Snide's Mechanism",
	"Snide's Mechanism",
	"Snide's Mechanism",
	"Snide's Mechanism",
	"Blue Flowers", # 2D
	"Plant (Green)", # 2D
	"Plant (Brown)", # 2D
	"Plant", # 2D
	"Pink Flowers", # 2D
	"Pink Flowers", # 2D
	"Plant", # 2D
	"Yellow Flowers", # 2D
	"Yellow Flowers", # 2D
	"Plant", # 2D
	"Blue Flowers", # 2D
	"Blue Flower", # 2D
	"Plant", # 2D
	"Plant", # 2D
	"Red Flowers", # 2D
	"Red Flower", # 2D
	"Mushrooms (Small)", # 2D
	"Mushrooms (Small)", # 2D
	"Purple Flowers", # 2D
	"Tree", # Castle?
	"Cactus", # Unused
	"Cactus", # Unused
	"Ramp", # Car Race?
	"Submerged Pot", # Unused
	"Submerged Pot", # Unused
	"Ladder", # Fungi
	"Ladder", # Fungi
	"Floor Texture?", # Fungi
	"Iron Gate", # Fungi
	"Day Gate", # Fungi
	"Night Gate", # Fungi
	"Cabin Door", # Caves
	"Ice Wall (Breakable)", # Caves
	"Igloo Door", # Caves
	"Castle Top", # Caves
	"Ice Dome", # Caves
	"Boulder Pad", # Caves
	"Target", # Caves, Tiny 5DI
	"Metal Gate",
	"CB Bunch (Lanky)",
	"CB Bunch (Chunky)",
	"CB Bunch (Tiny)",
	"CB Bunch (Diddy)",
	"Blue Aura",
	"Ice Maze", # Caves
	"Rotating Room", # Caves
	"Light + Barrier", # Caves
	"Light", # Caves
	"Trapdoor", # Caves
	"Large Wooden Door", # Aztec, Llama Temple?
	"Warp 5 Pad",
	"Warp 3 Pad",
	"Warp 4 Pad",
	"Warp 2 Pad",
	"Warp 1 Pad",
	"Large Door", # Castle
	"Library Door (Revolving?)", # Castle
	"Blue Platform", # Factory / K. Rool, Unused?
	"White Platform", # Factory / K. Rool, Unused?
	"Wooden Platform", # Castle
	"Wooden Bridge", # Castle
	"Wooden Door", # Castle
	"Metal Grate", # Castle Pipe
	"Metal Door", # Castle Greenhouse
	"Large Metal Door", # Castle?
	"Rotating Chair", # Castle
	"Baboon Balloon Pad (with platform)",
	"Large Aztec Door",
	"Large Aztec Door",
	"Large Wooden Door", # Castle Tree
	"Large Breakable Wooden Door", # Castle Tree
	"Pineapple Switch (Rotating)", # Castle Tree
	": Pad", # Aztec Chunky Puzzle
	"Triangle Pad", # Aztec Chunky Puzzle
	"+ Pad", # Aztec Chunky Puzzle
	"Stone Monkey Head", # Aztec
	"Stone Monkey Head", # Aztec
	"Stone Monkey Head", # Aztec
	"Door", # Caves Beetle Race
	"Broken Ship Piece", # Galleon
	"Broken Ship Piece", # Galleon
	"Broken Ship Piece", # Galleon
	"Flotsam", # Galleon
	"Metal Grate", # Factory, above crown pad
	"Treasure Chest", # Galleon
	"Up Switch", # Galleon
	"Down Switch",
	"DK Star", # Caves
	"Enguarde Door", # Galleon
	"Trash Can", # Castle
	"Fluorescent Tube", # Castle Toolshed?
	"Wooden Door Half", # Castle
	"Stone Platform", # Aztec Lobby?
	"Stone Panel", # Aztec Lobby?
	"Stone Panel (Rotating)", # Aztec Lobby
	"Wrinkly Door Wheel", # Fungi Lobby
	"Wooden Door", # Fungi Lobby
	"Wooden Panel", # Fungi? Lobby?
	"Electricity Shields?", # One for each kong, roughly in shape of Wrinkly Door wheel # TODO: Unused?
	"Unknown", # Internal name is "torches"
	"Boulder Pad (Red)", # Caves
	"Candelabra", # Castle?
	"Banana Peel", # Slippery
	"Skull+Candle", # Castle?
	"Metal Box",
	"1 Switch",
	"2 Switch",
	"3 Switch",
	"4 Switch",
	"Metal Grate (Breakable?)",
	"Pound The X Platform", # DK Isles
	"Wooden Door", # Castle Shed
	"Chandelier", # Castle
	"Bone Door", # Castle
	"Metal Bars", # Galleon
	"4 Door (5DS)",
	"5 Door (5DS)",
	"Door (Llama Temple)", # Aztec
	"Coffin Door", # Breakable?
	"Metal Bars",
	"Metal Grate", # Galleon
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"Boulder", # DK Isles, covering cannon to Fungi
	"Boulder", # DK Isles
	"K. Rool Ship Jaw Bottom", # DK Isles
	"Blast-O-Matic Cover?", # DK Isles
	"Blast-O-Matic Cover", # DK Isles
	"Door", # DK Isles, covering factory lobby, not solid
	"Platform", # DK Isles, up to Factory Lobby
	"Propeller", # K. Rool's Ship
	"K. Rool's Ship", # DK Isles, Intro Story
	"Mad Jack Platform (White)",
	"Mad Jack Platform (White)", # Factory
	"Mad Jack Platform (Blue)", # Factory
	"Mad Jack Platform (Blue)", # Factory
	"Skull Gate (Minecart)", # 2D
	"Dogadon Arena Outer",
	"Boxing Ring Corner (Red)",
	"Boxing Ring Corner (Green)",
	"Boxing Ring Corner (Blue)",
	"Boxing Ring Corner (Yellow)",
	"Lightning Rod", # Pufftoss Fight, DK Isles for some reason
	"Green Electricity", # Helm? Chunky BoM stuff?
	"Blast-O-Matic",
	"Target", # K. Rool Fight (Diddy Phase)
	"Spotlight", # K. Rool Fight
	"-",
	"Vine", # Unused?
	"Director's Chair", # Blooper Ending
	"Spotlight", # Blooper Ending
	"Spotlight", # Blooper Ending
	"Boom Microphone", # Blooper Ending
	"Auditions Sign", # Blooper Ending
	"Banana Hoard",
	"Boulder", # DK Isles, covering Caves lobby
	"Boulder", # DK Isles, covering Japes lobby
	"Rareware GB",
	"-",
	"-",
	"-",
	"-",
	"Platform (Crystal Caves Minigame)", # Tomato game
	"King Kut Out Arm (Bloopers)",
	"Rareware Coin", # Not collectable?
	"Golden Banana", # Not collectable?
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"-",
	"Rock", # DK Isles, Covering Castle Cannon?
	"K. Rool's Ship", # DK Isles, Entrance to final fight
	"-",
	"-",
	"-",
	"Wooden Door", # BFI Guarding Rareware GB
	"-",
	"-",
	"-",
	"Nothing?",
	"Troff n Scoff Portal",
	"Level Entry/Exit",
	"K. Lumsy Key Indicator?",
	"-",
	"-",
	"-",
	"-",
	"-",
	"Red Bell", # 2D, Minecart
	"Green Bell", # 2D, Minecart
	"Race Checkpoint",
	# Tested up to 0x2CF inclusive, all crashes so far
]

def getDirectoryLevel() -> str:
    """Get directory level, and what additional information is needed to ensure you get the right bin directory."""
    if os.path.exists("run_all.bat"):
        # Is on parent directory
        return "./"
    return "../"

def getFilePath() -> str:
    """Get file path of ROM."""
    pre = getDirectoryLevel()
    if not os.path.exists(f"{pre}bin/"):
        os.mkdir(f"{pre}bin/")
    if os.path.exists(f"{pre}ROM"):
        # Is running from BAT file
        with open(f"{pre}ROM","r") as fh:
            return fh.read().replace("\n","").strip()
    return filedialog.askopenfilename()

def getROMData(rom_path: str, folder: str) -> tuple:
    version = -1
    with open(rom_path,"rb") as fh:
        endianness = int.from_bytes(fh.read(1),"big")
        if endianness != 0x80:
            print("File is little endian. Convert to big endian and re-run")
            return (None, None, None, False)
        else:
            fh.seek(0x3D)
            release_or_kiosk = int.from_bytes(fh.read(1),"big")
            region = int.from_bytes(fh.read(1),"big")
            if release_or_kiosk == 0x50:
                version = 3 # Kiosk
            else:
                if region == 0x45:
                    version = 0 # US
                elif region == 0x4A:
                    version = 2 # JP
                elif region == 0x50:
                    version = 1 # PAL
                elif region == 0x47:
                    version = 4 # Lodgenet
                else:
                    print("Invalid version")
                    return (None, None, None, False)
            version_info = versions[version]
            pointer_table_offset = version_info.pointer_offset
            append = version_info.name
        if version < 0 or version > 4:
            print("Invalid version")
            return (None, None, None, False)
        sub_dump_path = f"{getDirectoryLevel()}bin/{folder}/"
        if not os.path.exists(sub_dump_path):
            os.mkdir(sub_dump_path)
        dump_path = f"{getDirectoryLevel()}bin/{folder}/{append}"
        if os.path.exists(dump_path):
            shutil.rmtree(dump_path)
        os.mkdir(dump_path)
    return (pointer_table_offset, version, dump_path, version >= 0 and version <= 4)

def getSafeFileName(name):
    """Get file name without invalid characters."""
    return name.replace("/","").replace("?","").replace(":","")

def getSafeFolderName(name):
    """Get folder name without invalid characters."""
    return name.replace(":"," -").replace(" ","_").replace("?","_")