import os
import json
import shutil
from lib import getSafeFileName, getSafeFolderName

TEMP_FILE = "temp.bin"
DUMP_PATH = "../bin/collision_code"

actor_names = [
    "Unknown",
    "Unknown",
    "DK",
    "Diddy",
    "Lanky",
    "Tiny",
    "Chunky",
    "Krusha",
    "Rambi",
    "Enguarde",
    "Unknown Controller",
    "Character Spawning Controller",
    "Loading Zone Controller",
    "Object Model 2 Controller",
    "Unknown Controller",
    "Unknown Controller",
    "Unknown",
    "Cannon Barrel",
    "Rambi Crate",
    "Barrel (Diddy 5DI)",
    "Camera Focus Point",
    "Pushable Box",
    "Barrel Spawner",
    "Cannon",
    "Race Hoop",
    "Hunky Chunky Barrel",
    "TNT Barrel",
    "TNT Barrel Spawner",
    "Bonus Barrel",
    "Minecart",
    "Fireball",
    "Bridge (Castle)",
    "Swinging Light",
    "Vine",
    "Kremling Kosh Controller",
    "Melon (Projectile)",
    "Peanut",
    "Rocketbarrel",
    "Pineapple",
    "Large Brown Bridge",
    "Mini Monkey Barrel",
    "Orange",
    "Grape",
    "Feather",
    "Laser",
    "Golden Banana",
    "Barrel Gun",
    "Watermelon Slice",
    "Coconut",
    "Rocketbarrel",
    "Lime",
    "Ammo Crate",
    "Orange Pickup",
    "Banana Coin",
    "DK Coin",
    "Small Explosion",
    "Orangstand Sprint Barrel",
    "Strong Kong Barrel",
    "Swinging Light",
    "Fireball",
    "Bananaporter",
    "Boulder",
    "Minecart",
    "Vase (O)",
    "Vase (:)",
    "Vase (Triangle)",
    "Vase (+)",
    "Cannon Ball",
    "Unknown Swingable",
    "Vine",
    "Counter",
    "Kremling (Red)",
    "Boss Key",
    "Cannon",
    "Cannon Ball",
    "Blueprint (Diddy)",
    "Blueprint (Chunky)",
    "Blueprint (Lanky)",
    "Blueprint (DK)",
    "Blueprint (Tiny)",
    "Minecart",
    "Fire Spawner? (Dogadon)",
    "Boulder Debris",
    "Spider Web",
    "Steel Keg Spawner",
    "Steel Keg",
    "Crown",
    "Minecart",
    "Unknown Number Display",
    "Fire",
    "Ice Wall?",
    "Balloon (Diddy)",
    "Stalactite",
    "Rock Debris",
    "Car",
    "Pause Menu",
    "Hunky Chunky Barrel (Dogadon)",
    "TNT Barrel Spawner (Dogadon)",
    "Tag Barrel",
    "Fireball",
    "1 Pad (Diddy 5DI)",
    "2 Pad (Diddy 5DI)",
    "3 Pad (Diddy 5DI)",
    "4 Pad (Diddy 5DI)",
    "5 Pad (Diddy 5DI)",
    "6 Pad (Diddy 5DI)",
    "Kong Reflection",
    "Bonus Barrel (Hideout Helm)",
    "Unknown Fireball",
    "Race Checkpoint",
    "CB Bunch",
    "Balloon (Chunky)",
    "Balloon (Tiny)",
    "Balloon (Lanky)",
    "Balloon (DK)",
    "K. Lumsy's Cage",
    "Chain",
    "Beanstalk",
    "Yellow ?(",
    "CB Single (Blue)",
    "CB Single (Yellow)",
    "Crystal Coconut",
    "DK Coin",
    "Kong Mirror",
    "Barrel Gun",
    "Barrel Gun",
    "Fly Swatter",
    "Searchlight",
    "Headphones",
    "Enguarde Crate",
    "Apple",
    "Worm",
    "Enguarde Crate (Unused?)",
    "Barrel",
    "Training Barrel",
    "Boombox",
    "Tag Barrel",
    "Tag Barrel",
    "B. Locker",
    "Rainbow Coin Patch",
    "Rainbow Coin",
    "Unknown",
    "Unknown",
    "Unknown",
    "Unknown",
    "Cannon (Seasick Chunky)",
    "Unknown",
    "Balloon (Unused - K. Rool)",
    "Rope",
    "Banana Barrel",
    "Banana Barrel Spawner",
    "Unknown",
    "Unknown",
    "Unknown",
    "Unknown",
    "Unknown",
    "Wrinkly",
    "Unknown",
    "Unknown",
    "Unknown",
    "Unknown",
    "Unknown",
    "Unknown",
    "Banana Fairy (BFI)",
    "Ice Tomato",
    "Tag Barrel (King Kut Out)",
    "King Kut Out Part",
    "Cannon",
    "Unknown Fairy Something?",
    "Pufftup",
    "Damage Source",
    "Orange",
    "Unknown",
    "Cutscene Controller",
    "Unknown",
    "Kaboom",
    "Timer",
    "Timer Controller",
    "Beaver",
    "Shockwave (Mad Jack)",
    "Krash",
    "Book",
    "Klobber",
    "Zinger",
    "Snide",
    "Army Dillo",
    "Kremling",
    "Klump",
    "Camera",
    "Cranky",
    "Funky",
    "Candy",
    "Beetle",
    "Mermaid",
    "Vulture",
    "Squawks",
    "Cutscene DK",
    "Cutscene Diddy",
    "Cutscene Lanky",
    "Cutscene Tiny",
    "Cutscene Chunky",
    "Llama",
    "Fairy Picture",
    "Padlock (T&S)",
    "Mad Jack",
    "Klaptrap",
    "Zinger",
    "Vulture (Race)",
    "Klaptrap (Purple)",
    "Klaptrap (Red)",
    "GETOUT Controller",
    "Klaptrap (Skeleton)",
    "Beaver (Gold)",
    "Fire Column Spawner",
    "Minecart (TNT)",
    "Minecart (TNT)",
    "Pufftoss",
    "RW Employee Picture",
    "Handle",
    "Slot",
    "Cannon (Seasick Chunky)",
    "Light Piece",
    "Banana Peel",
    "Fireball Spawner",
    "Mushroom Man",
    "Unknown",
    "Troff",
    "K. Rool's Foot",
    "Bad Hit Detection Man",
    "K. Rool's Toe",
    "Ruler",
    "Toy Box",
    "Text Overlay",
    "Squawks",
    "Scoff",
    "Robo-Kremling",
    "Dogadon",
    "Krossbones Head",
    "Kremling",
    "Bongos",
    "Spotlight Fish",
    "Kasplat (DK)",
    "Kasplat (Diddy)",
    "Kasplat (Lanky)",
    "Kasplat (Tiny)",
    "Kasplat (Chunky)",
    "Mechanical Fish",
    "Seal",
    "Banana Fairy",
    "Squawks with spotlight",
    "Owl",
    "Spider miniBoss",
    "Rabbit",
    "Nintendo Logo",
    "Cutscene Object",
    "Shockwave",
    "Minigame Controller",
    "Fire Breath Spawner",
    "Shockwave",
    "Guard",
    "Text Overlay",
    "Robo-Zinger",
    "Krossbones",
    "Fire Shockwave (Dogadon)",
    "Squawks",
    "Light beam",
    "DK Rap Controller",
    "Shuri",
    "Gimpfish",
    "Mr. Dice",
    "Sir Domino",
    "Mr. Dice",
    "Rabbit",
    "Fireball (With Glasses)",
    "Unknown Fire Spawner something",
    "K. Lumsy",
    "Spiderling",
    "Squawks",
    "Projectile",
    "Trap Bubble (279",
    "Spider Silk String",
    "K. Rool (DK Phase)",
    "Retexturing Controller",
    "Skeleton Head",
    "Unknown Minecart Something",
    "Bat",
    "Giant Clam",
    "Unknown Minecart Something",
    "Tomato",
    "Kritter-in-a-Sheet",
    "Pufftup",
    "Kosha",
    "K. Rool (Diddy Phase)",
    "K. Rool (Lanky Phase)",
    "K. Rool (Tiny Phase)",
    "K. Rool (Chunky Phase)",
    "Unknown",
    "Battle Crown Controller",
    "Unknown",
    "Textbox",
    "Snake",
    "Turtle",
    "Toy Car",
    "Toy Car",
    "Camera",
    "Missile",
    "Race Controller",
    "Unknown Race Something",
    "Seal",
    "Kong Logo (Instrument)",
    "Spotlight",
    "Race Checkpoint",
    "Minecart (TNT)",
    "Idle Particle",
    "Rareware Logo",
    "Unknown Race Something",
    "Kong (Tag Barrel)",
    "Locked Kong (Tag Barrel)",
    "Unknown Multiplayer Something",
    "Propeller (Boat)",
    "Potion",
    "Fairy (Refill)",
    "Car",
    "Enemy Car",
    "Text Overlay Controller",
    "Shockwave",
    "Main Menu Controller",
    "Kong",
    "Klaptrap",
    "Fairy",
    "Bug",
    "Klaptrap",
    "Big Bug Bash Controller?",
    "Barrel (Main Menu)",
    "Padlock (K. Lumsy)",
    "Snide's Menu",
    "Training Barrel Controller",
    "Multiplayer Model (Main Menu)",
    "End Sequence Controller",
    "Arena Controller",
    "Bug",
    "Unknown",
    "Try Again Dialog",
    "Pause Menu",
]

extra_enemies = {
    "Bug (Kiosk)": 0x8074B240,
    "Jack in the Box (Kiosk)": 0x8074BBB8,
    "Boxing Glove in the Box (Kiosk)": 0x8074BBB8,
    "Army (Kiosk)": 0x8074B6FC,
    "Unknown (Kiosk)": 0x8074B3E8,
#
}

def parseArray(data: bytes, offset: int):
    """Parses collision array."""
    actor_collisions = []
    with open(TEMP_FILE, "wb") as fh:
        fh.write(data)
    with open(TEMP_FILE, "rb") as fh:
        extra_keys = list(extra_enemies.keys())
        for x in range(344 + len(extra_enemies.keys())):
            if x < 344:
                fh.seek(0x8074C604 - offset + (8 * x))
                data_pointer = int.from_bytes(fh.read(4), "big")
                byte_4 = int.from_bytes(fh.read(1), "big")
                local_data = {
                    "index": x,
                    "name": actor_names[x],
                    "byte_4": byte_4,
                    "has_trees": data_pointer != 0
                }
                print(f"Dumping actor {x}")
                actor_name = actor_names[x]
            else:
                selected_extra = extra_keys[x - 344]
                local_data = {
                    "index": -1,
                    "name": selected_extra,
                    "byte_4": 1,
                    "has_trees": True
                }
                data_pointer = extra_enemies[selected_extra]
                print(f"Dumping {selected_extra}")
                actor_name = selected_extra
            if data_pointer != 0:
                folder_name = getSafeFolderName(actor_name)
                has_duplicates = len([v for v in actor_names if v == actor_name]) > 1
                if has_duplicates:
                    folder_name = getSafeFolderName(f"{actor_name} ({x})")
                folder_path = f"{DUMP_PATH}/{folder_name}"
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                y = 0
                trees = []
                while True:
                    fh.seek(data_pointer - offset + (y * 8))
                    target_type = int.from_bytes(fh.read(2), "big")
                    
                    unk0 = int.from_bytes(fh.read(2), "big")
                    target_pointer = int.from_bytes(fh.read(4), "big")
                    local_tree = {}
                    filename = "default"
                    if target_type < 0x8000:
                        if target_type != 0:
                            local_tree["target_actor"] = target_type
                            filename = actor_names[target_type]
                            has_duplicates = len([v for v in actor_names if v == actor_names[target_type]]) > 1
                            if has_duplicates:
                                filename = f"{actor_names[target_type]} ({target_type})"
                    else:
                        signed_value = target_type - 65536
                        local_tree["target_interaction"] = (1 << (abs(signed_value) - 1))
                        filename = f"Interaction {local_tree['target_interaction']}"
                    if target_pointer:
                        instructions = []
                        args = []
                        z = 0
                        while True:
                            fh.seek(target_pointer - offset + (0xC * z))
                            targ_bitfield_0 = int.from_bytes(fh.read(2), "big")
                            targ_bitfield_1 = int.from_bytes(fh.read(2), "big")
                            code = int.from_bytes(fh.read(4), "big")
                            collision_type = int.from_bytes(fh.read(1), "big")
                            unk9 = int.from_bytes(fh.read(1), "big")
                            force_break = int.from_bytes(fh.read(1), "big")
                            original_force_break = force_break
                            arg_data = {
                                "actor_interaction": -1 if targ_bitfield_0 == 0xFFFF else hex(targ_bitfield_0),
                                "target_interaction": -1 if targ_bitfield_1 == 0xFFFF else hex(targ_bitfield_1),
                            }
                            if code != 0:
                                arg_data["function"] = hex(code)
                            if collision_type != 0:
                                arg_data["collision_type"] = hex(collision_type)
                            if unk9 != 0:
                                arg_data["unk9"] = hex(unk9)
                            if force_break != 0:
                                arg_data["force_break"] = hex(force_break)
                            args.append(arg_data)
                            conditions = []
                            if targ_bitfield_0 != 0xFFFF:
                                conditions.append(f"(actor->0x132 & {hex(targ_bitfield_0)})")
                            if targ_bitfield_1 != 0xFFFF:
                                conditions.append(f"(target->0x132 & {hex(targ_bitfield_1)})")
                            if targ_bitfield_0 and targ_bitfield_1:
                                if len(conditions) > 0:
                                    instructions.append(f"if ({' && '.join(conditions)}) {{")
                                if code != 0:
                                    instructions.append(f"if (FUN_{hex(code)[2:]}(actor, target, collision_queue)) {{")
                                instructions.append(f"if (CollisionData.collision_type_0 < {collision_type}) {{")
                                instructions.append(f"CollisionData.collision_type_0 = {collision_type};")
                                instructions.append(f"CollisionData.collision_source = target;")
                                instructions.append("}")
                                instructions.append("if (CollisionData.counter_0 < 0xF) {")
                                instructions.append("CollisionData.0x204[CollisionData.counter_0] = target;")
                                instructions.append(f"CollisionData.0x244[CollisionData.counter_0] = {unk9};")
                                if byte_4 == 0 or unk9 not in (5, 15):
                                    instructions.append("CollisionData.counter_0++;")
                                else:
                                    if local_tree.get("target_interaction", None) == 1 or "target_interaction" not in local_tree:
                                        if "target_interaction" not in local_tree:
                                            instructions.append("if ((target->interaction_bitfield & 1) == 0) {")
                                        instructions.append("// Not Player")
                                        instructions.append("CollisionData.counter_0++;")
                                        if "target_interaction" not in local_tree:
                                            instructions.append("} else {")
                                    if local_tree.get("target_interaction", 0) != 1:
                                        if byte_4 == 0:
                                            instructions.append("CollisionData.counter_0++;")
                                        elif unk9 not in (5, 15):
                                            instructions.append("CollisionData.counter_0++;")
                                            force_break = unk9
                                        else:
                                            instructions.append("if (target->paad->invulnerability_timer == 0) {")
                                            instructions.append("CollisionData.counter_0++;")
                                            instructions.append("}")
                                    if "target_interaction" not in local_tree:
                                        instructions.append("}")
                                if x in (0xBB, 0xEB, 0x123):
                                    instructions.append("if (actor->interactable_bitfield & 2) {")
                                    instructions.append("target->0x64 |= 0x1000;")
                                    instructions.append("}")
                                if force_break in (0, 2):
                                    force_break = 0
                                else:
                                    force_break = original_force_break
                                instructions.append("}")
                                if force_break == 0:
                                    instructions.append("return;")
                                if code != 0:
                                    instructions.append("}")
                                if len(conditions) > 0:
                                    instructions.append("}")
                            z += 1
                            if original_force_break == 0:
                                break
                        local_tree["instructions"] = instructions
                        local_tree["arg_data"] = args
                        # Parse Instructions
                        with open(f"{folder_path}/{getSafeFileName(filename)}.c", "w") as fg:
                            local_indent = 0
                            for instruction in instructions:
                                if instruction[0] == "}":
                                    local_indent -= 1
                                output_str = ""
                                if local_indent > 0:
                                    indent_lst = ["\t"] * local_indent
                                    output_str += "".join(indent_lst)
                                output_str += instruction
                                fg.write(f"{output_str}\n")
                                if instruction[-1] == "{":
                                    local_indent += 1
                        # Parse Args
                        with open(f"{folder_path}/{getSafeFileName(filename)}.h", "w") as fg:
                            for arg in args:
                                fg.write("{")
                                prop_segs = []
                                for prop in arg:
                                    if prop == "function":
                                        prop_segs.append(f".{prop}=(void*){arg[prop]}")
                                    else:
                                        prop_segs.append(f".{prop}={arg[prop]}")
                                fg.write(", ".join(prop_segs))
                                fg.write("},\n")
                    trees.append(local_tree)
                    if target_type == 0:
                        break
                    y += 1
                local_data["trees"] = trees

            actor_collisions.append(local_data)
    with open("../bin/collision_output.json", "w") as fh:
        fh.write(json.dumps(actor_collisions, indent=4))

if os.path.exists(DUMP_PATH):
    shutil.rmtree(DUMP_PATH)
os.mkdir(DUMP_PATH)
with open("../data/actor_collision_data.bin", "rb") as fh:
    parseArray(fh.read(), 0x80000000)
if os.path.exists(TEMP_FILE):
    os.remove(TEMP_FILE)