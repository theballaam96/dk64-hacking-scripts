import zlib
import os
import struct
import json
from lib import getFilePath, getROMData

def getIconDB(version):
    if version != 3:
        return {
            0x0: "waterfall_tall",
            0x1: "waterfall_short",
            0x2: "water",
            0x3: "lava",
            0x4: "sparkles",
            0x5: "pop_explosion",
            0x6: "lava_explosion",
            0x7: "green_leaf?",
            0x8: "brown_smoke_explosion",
            0x9: "small_explosion",
            0xA: "solar_flare?",
            0xB: "splash",
            0xC: "bubble",
            0xD: "purple_sparkle",
            0xE: "yellow_sparkle",
            0xF: "green_sparkle",
            0x10: "purple_sparkle",
            0x11: "yellow_sparkle",
            0x12: "green_sparkle",
            0x13: "large_smoke_explosion",
            0x14: "pink_implosion",
            0x15: "brown_horizontal_spinning_plank",
            0x16: "birch_horizontal_spinning_plank",
            0x17: "brown_vertical_spinning_plank",
            0x18: "star_water_ripple",
            0x19: "circle_water_ripple",
            0x1A: "small_smoke_explosion",
            0x1B: "static_star",
            0x1C: "static_z",
            0x1D: "white_flare?",
            0x1E: "static_rain?",
            0x1F: "medium_smoke_explosion",
            0x20: "bouncing_melon",
            0x21: "vertical_rolling_melon",
            0x22: "red_flare?",
            0x23: "sparks",
            0x24: "peanut",
            0x25: "star_flare?",
            0x26: "peanut_shell",
            0x27: "small_explosion",
            0x28: "large_smoke_implosion",
            0x29: "blue_lazer",
            0x2A: "pineapple",
            0x2B: "fireball",
            0x2C: "orange",
            0x2D: "grape",
            0x2E: "grape_splatter",
            0x2F: "tnt_sparkle",
            0x30: "fire_explosion",
            0x31: "small_fireball",
            0x32: "diddy_coin",
            0x33: "chunky_coin",
            0x34: "lanky_coin",
            0x35: "dk_coin",
            0x36: "tiny_coin",
            0x37: "dk_coloured_banana",
            0x38: "film",
            0x39: "bouncing_orange",
            0x3A: "crystal_coconut",
            0x3B: "gb",
            0x3C: "banana_medal",
            0x3D: "diddy_coloured_banana",
            0x3E: "chunky_coloured_banana",
            0x3F: "lanky_coloured_banana",
            0x40: "dk_coloured_banana",
            0x41: "tiny_coloured_banana",
            0x42: "exploded_krash_barrel_enemy",
            0x43: "white_explosion_thing",
            0x44: "coconut",
            0x45: "coconut_shell",
            0x46: "spinning_watermelon_slice",
            0x47: "tooth",
            0x48: "ammo_crate",
            0x49: "race_coin",
            0x4A: "lanky_bp",
            0x4B: "cannonball",
            0x4C: "crystal_coconut",
            0x4D: "feather",
            0x4E: "guitar_gazump",
            0x4F: "bongo_blast",
            0x50: "saxophone",
            0x51: "triangle",
            0x52: "trombone",
            0x53: "waving_yellow_double_eighth_note",
            0x54: "waving_yellow_single_eighth_note",
            0x55: "waving_green_single_eighth_note",
            0x56: "waving_purple_double_eighth_note",
            0x57: "waving_red_double_eighth_note",
            0x58: "waving_red_single_eighth_note",
            0x59: "waving_white_double_eighth_note",
            0x5A: "diddy_bp",
            0x5B: "chunky_bp",
            0x5C: "dk_bp",
            0x5D: "tiny_bp",
            0x5E: "spinning_sparkle",
            0x5F: "static_rain?",
            0x60: "translucent_water",
            0x61: "unk61",
            0x62: "black_screen",
            0x63: "white_cloud",
            0x64: "thin_lazer",
            0x65: "blue_bubble",
            0x66: "white_faded_circle",
            0x67: "white_circle",
            0x68: "grape_particle?",
            0x69: "spinning_blue_sparkle",
            0x6A: "white_smoke_explosion",
            0x6B: "l-r_joystick",
            0x6C: "fire_wall",
            0x6D: "static_rain_bubble",
            0x6E: "a_button",
            0x6F: "b_button",
            0x70: "z_button",
            0x71: "c_down_button",
            0x72: "c_up_button",
            0x73: "c_left_button",
            0x74: "acid",
            0x75: "acid_explosion",
            0x76: "race_hoop",
            0x77: "acid_goop?",
            0x78: "unk78",
            0x79: "broken_bridge?",
            0x7A: "white_pole?",
            0x7B: "bridge_chip?",
            0x7C: "wooden_beam_with_rivets",
            0x7D: "chunky_bunch",
            0x7E: "diddy_bunch",
            0x7F: "lanky_bunch",
            0x80: "dk_bunch",
            0x81: "tiny_bunch",
            0x82: "chunky_balloon",
            0x83: "diddy_balloon",
            0x84: "dk_balloon",
            0x85: "lanky_balloon",
            0x86: "tiny_balloon",
            0x87: "r_button",
            0x88: "l_button",
            0x89: "fairy",
            0x8A: "boss_key",
            0x8B: "crown",
            0x8C: "rareware_coin",
            0x8D: "nintendo_coin",
            0x8E: "no_symbol",
            0x8F: "headphones",
            0x90: "opaque_blue_water",
            0x91: "start_button",
            0x92: "white_question_mark",
            0x93: "candy_face",
            0x94: "cranky_face",
            0x95: "snide_face",
            0x96: "funky_face",
            0x97: "left_arrow",
            0x98: "white_spark?",
            0x99: "black_boulder_chunk",
            0x9A: "green_boulder_chunk",
            0x9B: "wood_chip",
            0x9C: "snowflake/dandelion",
            0x9D: "static_water?",
            0x9E: "spinning_leaf",
            0x9F: "flashing_water?",
            0xA0: "rainbow_coin",
            0xA1: "shockwave_orange_particle",
            0xA2: "implosion?",
            0xA3: "rareware_employee_face",
            0xA4: "smoke",
            0xA5: "static_smoke?",
            0xA6: "barrel_bottom_chunk",
            0xA7: "scoff_face",
            0xA8: "multicoloured_bunch",
            0xA9: "dk_face",
            0xAA: "diddy_face",
            0xAB: "lanky_face",
            0xAC: "tiny_face",
            0xAD: "chunky_face",
            0xAE: "fairy_tick",
            0xAF: "wrinkly",
        }
    return {
        10: "explosion",
        14: "sparkle",
        20: "explosion_0",
        38: "ammo_peanut",
        44: "ammo_pineapple",
        47: "ammo_47",
        52: "coin_diddy",
        53: "coin_chunky",
        54: "coin_lanky",
        55: "coin_dk",
        56: "coin_tiny",
        58: "pickup_film",
        59: "pickup_orange",
        60: "pickup_crystal",
        61: "pickup_gb_single",
        62: "pickup_gb_multi",
        63: "pickup_medal",
        64: "single_diddy",
        65: "single_chunky",
        66: "single_lanky",
        67: "single_dk",
        68: "single_tiny",
        69: "klobber_pile",
        71: "ammo_coconut",
        76: "pickup_racecoin",
        77: "blueprint_lanky",
        84: "ammo_feather",
        85: "instrument_guitar",
        86: "instrument_bongos",
        87: "instrument_sax",
        88: "instrument_triangle",
        89: "instrument_trombone",
        97: "blueprint_diddy",
        98: "blueprint_chunky",
        99: "blueprint_dk",
        100: "blueprint_tiny",
        117: "l_r_joystick",
        120: "a_button",
        121: "b_button",
        122: "z_button",
        123: "c_down_button",
        124: "c_up_button",
        125: "c_left_button",
        147: "pickup_fairy",
        148: "pickup_key",
        149: "pickup_crown",
        150: "pickup_rwcoin",
        151: "pickup_nincoin",
        153: "pickup_headphones",
    }

def getFileNameDB(version):
    if version != 3:
        return [
            "Bonus Instructions",
            "Story Level Intro Text",
            "Kong Names",
            "Diddy",
            "Tiny",
            "Chunky",
            "Lanky",
            "Funky",
            "Cranky",
            "Candy",
            "Llama",
            "Snide",
            "DK TV Screen",
            "Dolby",
            "Beetle",
            "Vulture",
            "Squawks",
            "Factory Car Race",
            "Seal Race",
            "Misc & Microbuffer",
            "Rabbit",
            "Owl",
            "Worm",
            "Mermaid",
            "DK",
            "Training Grounds",
            "Bonus Encouragement Text",
            "K. Lumsy",
            "Seal Race 2",
            "B. Locker",
            "Fairy Queen",
            "Beanstalk",
            "Unused Lanky NPC",
            "Ice Tomato",
            "Castle Car Race",
            "Location and Level Names",
            "Pause Menu",
            "Main Menu",
            "Race Positions",
            "Move Names",
            "Fairy Queen Rareware Door",
            "Wrinkly",
            "Snide's Bonus Games",
        ]
    return [
        "Bonus Instructions",
        "Army Dillo",
        "George",
        "Diddy",
        "Tiny",
        "Chunky",
        "Lanky",
        "Funky",
        "Cranky",
        "Candy",
        "Llama",
        "Snide",
        "James Bond Reference",
        "Vulture_Shooting",
        "Beetle",
        "Vulture_Race",
        "Squawks",
        "Factory Car Race",
        "Seal Race",
        "Miscellaneous",
        "Rabbit Race",
        "Owl Race",
        "Worm",
    ]

main_pointer_table_offset = 0
temp_file = "decodedtext.bin"

def float_to_hex(f):
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


def grabText():
    """Pull text from ROM."""
    global main_pointer_table_offset
    file_path = getFilePath()
    main_pointer_table_offset, version, dump_path, valid = getROMData(file_path, "text")
    text_table_index = 12 - (version == 3)
    if valid:
        with open(file_path, "rb") as fh:
            fh.seek(main_pointer_table_offset + (text_table_index * 4) + (32 * 4))
            text_table_count = int.from_bytes(fh.read(4), "big")
            fh.seek(main_pointer_table_offset + (text_table_index * 4))
            text_table = main_pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
            for file_index in range(text_table_count):
                fh.seek(text_table + (file_index * 4))
                text_start = main_pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
                text_end = main_pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
                text_size = text_end
                fh.seek(text_start)
                indic = int.from_bytes(fh.read(2), "big")
                fh.seek(text_start)
                with open(temp_file, "wb") as fg:
                    if indic == 0x1F8B:
                        fg.write(zlib.decompress(fh.read(text_size), (15 + 32)))
                    else:
                        fg.write(fh.read(text_size))

                with open(temp_file, "rb") as fi:
                    fi.seek(0)
                    count = int.from_bytes(fi.read(1), "big")
                    text = []
                    text_data = []
                    text_start = (count * 0xF) + 3
                    data_start = 1
                    for i in range(count):
                        fi.seek(data_start)
                        section_1_count = int.from_bytes(fi.read(1), "big")
                        section_2_count = int.from_bytes(fi.read(1), "big")
                        section_3_count = int.from_bytes(fi.read(1), "big")
                        # print(str(section_1_count) + " > " + str(section_2_count) + " > " + str(section_3_count))
                        fi.seek(data_start + 5)
                        start = int.from_bytes(fi.read(2), "big")
                        size = int.from_bytes(fi.read(2), "big")
                        block_start = 1
                        blocks = []
                        for k in range(section_1_count):
                            fi.seek(data_start + block_start)
                            sec2ct = int.from_bytes(fi.read(1), "big")
                            offset = 0
                            if (sec2ct & 4) != 0:
                                # print("Adding offset")
                                offset += 4
                            text_blocks = []
                            if (sec2ct & 1) == 0:
                                if (sec2ct & 2) != 0:
                                    fi.seek(data_start + block_start + offset + 1)
                                    sec3ct = int.from_bytes(fi.read(1), "big")
                                    for j in range(sec3ct):
                                        _block = block_start + 2 + offset + (4 * j) - 1
                                        fi.seek(data_start + _block)
                                        _pos = int.from_bytes(fi.read(2), "big")
                                        fi.seek(data_start + _block)
                                        _dat = int.from_bytes(fi.read(4), "big")
                                        sprite_index = (_dat >> 8) & 0xFF
                                        text_blocks.append({"type": "sprite", "position": _pos, "data": hex(_dat), "sprite": getIconDB(version).get(sprite_index,f"unk{hex(sprite_index)}")})
                                    added = block_start + 2 + offset + (4 * sec3ct) + 4
                            else:
                                fi.seek(data_start + block_start + offset + 1)
                                sec3ct = int.from_bytes(fi.read(1), "big")
                                for j in range(sec3ct):
                                    _block = block_start + 2 + offset + (8 * j) - 1
                                    fi.seek(data_start + _block + 3)
                                    _start = int.from_bytes(fi.read(2), "big")
                                    fi.seek(data_start + _block + 5)
                                    _size = int.from_bytes(fi.read(2), "big")
                                    text_blocks.append({"type": "normal", "start": _start, "size": _size})
                                added = block_start + 2 + offset + (8 * sec3ct) + 4
                            blocks.append({"block_start": hex(block_start + data_start), "section2count": sec2ct, "section3count": sec3ct, "offset": offset, "text": text_blocks})
                            block_start = added
                        fi.seek(data_start)
                        if added < data_start:
                            info = b""
                        else:
                            info = fi.read(added - data_start)
                        text_data.append({"arr": info, "text": blocks, "section1count": section_1_count, "section2count": section_2_count, "section3count": section_3_count, "data_start": hex(data_start)})
                        text_start += added - data_start
                        data_start += block_start
                    for item in text_data:
                        text_block = []
                        # print(item)
                        for item2 in item["text"]:
                            # print(item2)
                            temp = []
                            for item3 in item2["text"]:
                                if item3["type"] == "normal":
                                    start = item3["start"] + data_start + 2
                                    # print(hex(start))
                                    end = start + item3["size"]
                                    fi.seek(start)
                                    temp.append(fi.read(item3["size"]).decode())
                                elif item3["type"] == "sprite":
                                    temp.append(item3["sprite"])
                                    # print(fi.read(item3["size"]))
                            text_block.append(temp)
                        text.append(text_block)
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                formatted_text = []
                for t in text:
                    y = []
                    for x in t:
                        y.append({"text": x})
                    formatted_text.append(y)
                with open(f"{dump_path}/[{file_index}] - {getFileNameDB(version)[file_index]}.json","w") as j:
                    j.write(json.dumps(formatted_text, indent=4))

grabText()