import zlib
import os
import struct
import json
from typing import BinaryIO
from lib import getFilePath, getROMData

ANIMATION_TABLE = 11
TEMP_FILE = "decoded_anim.bin"
DEF_FILE = "anim_def_file.bin"
TEMP_CODE_FILE = "anim_code_file.bin"

def int_to_float(val):
    """Convert a hex int to a float."""
    if val == 0:
        return 0
    return struct.unpack("!f", bytes.fromhex(f"{val:#010x}".split("0x")[1]))[0]

def parseSubAnimationCode(sub_command: int, cmd_list: list, fh: BinaryIO):
    match sub_command:
        case 0:
            cmd_list.append("// return;")
        case 1:
            param_1 = int.from_bytes(fh.read(4), "big") # Buffer?
        case 2:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 3:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 4:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 5:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 6:
            param_1 = int.from_bytes(fh.read(4), "big")
            param_2 = int.from_bytes(fh.read(1), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1}, {param_2})"])
        case 7:
            param_1 = int.from_bytes(fh.read(1), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 8:
            param_1 = int.from_bytes(fh.read(4), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 9:
            cmd_list.append("// return;")
        case 10:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 11:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 12:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 13:
            param_1 = int.from_bytes(fh.read(2), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 14:
            param_1 = int.from_bytes(fh.read(1), "big")
            param_2 = int.from_bytes(fh.read(1), "big")
            param_3 = int.from_bytes(fh.read(2), "big")
            param_4 = int.from_bytes(fh.read(2), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1}, {param_2}, {param_3}, {param_4})"])
        case 15:
            param_1 = int.from_bytes(fh.read(1), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 16:
            param_1 = int.from_bytes(fh.read(1), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 17:
            param_1 = int.from_bytes(fh.read(1), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 18:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 19:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 20:
            param_1 = int.from_bytes(fh.read(2), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 21:
            param_1 = int.from_bytes(fh.read(2), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 22:
            param_1 = int.from_bytes(fh.read(2), "big")
            param_2 = int.from_bytes(fh.read(2), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1}, {param_2})"]) # Buffer?
        case 23:
            param_1 = int.from_bytes(fh.read(1), "big")
            param_2 = int.from_bytes(fh.read(1), "big")
            param_3 = int.from_bytes(fh.read(2), "big")
            param_4 = int.from_bytes(fh.read(2), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1}, {param_2}, {param_3}, {param_4})"])
        case 24:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 25:
            param_1 = int.from_bytes(fh.read(1), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 26:
            param_1 = int.from_bytes(fh.read(1), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 27:
            param_1 = int.from_bytes(fh.read(1), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 28:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 29:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 30:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 31:
            cmd_list.extend([f"subcmd_{sub_command}()"])
        case 32:
            param_1 = int.from_bytes(fh.read(4), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1})"])
        case 33:
            param_1 = int.from_bytes(fh.read(1), "big")
            param_2 = int.from_bytes(fh.read(1), "big")
            if param_1 < param_2:
                cmd_list.extend([
                    "int const_val = 0.2f; // Defined at 80757460",
                    f"sprite_data** sprite = &GeneralParticles[{param_1}]; // 80746B80",
                    f"int counter = {param_1};",
                    "do {",
                    "FUN_8071498C(FUN_8071D28C);",
                    "FUN_807149FC(-1);",
                    "FUN_807149B8(1);",
                    "FUN_8071496C(1);",
                    "FUN_80714950(1);",
                    "FUN_80714A28(0x20);",
                    "int unk0 = FUN_80714C08(*sprite, const_val, actor, 7, 0);",
                    "counter++;",
                    "sprite++;",
                    f"}} while (counter < {param_2});"
                ])
            cmd_list.append(f"return {param_1};")
        case 34:
            param_1 = int.from_bytes(fh.read(1), "big")
            if param_1 == 0:
                cmd_list.extend([
                    "actor->obj_props_bitfield |= 0x40000000;",
                    "LevelStateBitfield &= 0xFFFEFFCF;",
                    "FUN_806D9924(actor);"
                ])
            else:
                cmd_list.extend([
                    "actor->obj_props_bitfield &= 0xBFFFFFFF;",
                    "LevelStateBitfield |= 0x10030;"
                ])
        case 35:
            param_1 = int.from_bytes(fh.read(1), "big")
            cmd_list.extend([
                "spawnActorWrapper(ACTOR_INSTRUMENTLOGO, KongLogoModels[actor->actor_type - 2]); // Array at 80746E14",
                "FUN_8067B238(LastSpawnedActor, actor, actor->rendering_parameters->scale_x);",
                "LastSpawnedActor->rot_z = actor->rot_z;",
                "LastSpawnedActor->rot_x = actor->rot_x;",
                f"LastSpawnedActor->paad->field_0x6 = {param_1};"
            ])
        case 36:
            param_1 = int.from_bytes(fh.read(1), "big")
            if param_1 == 0:
                cmd_list.extend([
                    "actorData* vehicle = player_paad->vehicle_actor_pointer;",
                    "if ((vehicle) && (vehicle->actor_type == ACTOR_SPOTLIGHT)) {",
                    "deleteActorContainer(vehicle);",
                    "player_paad->vehicle_actor_pointer = 0;",
                    "}"
                ])
            else:
                cmd_list.extend([
                    "spawnActorWrapper(ACTOR_SPOTLIGHT, 0xA8);",
                    "FUN_8067B238(LastSpawnedActor, actor, actor->rendering_parameters->scale_x);",
                    "player_paad->vehicle_actor_pointer = LastSpawnedActor;"
                ])
        case 37:
            param_1 = int.from_bytes(fh.read(1), "big")
            if param_1 == 0:
                cmd_list.extend([
                    "if (actor->chunk != -1) {",
                    "setChunkLighting(StoredChunkLightR, StoredChunkLightG, StoredChunkLightB, actor->chunk);",
                    "}"
                ])
            else:
                cmd_list.extend([
                    "if (actor->chunk != -1) {",
                    "storeChunkLighting(&StoredChunkLightR, &StoredChunkLightG, &StoredChunkLightB, actor->chunk);",
                    "setChunkLighting(107.0f, 48.0f, 80.0f, actor->chunk);",
                    "}"
                ])
        case 38:
            param_1 = int.from_bytes(fh.read(2), "big")
            param_2 = int.from_bytes(fh.read(2), "big")
            param_3 = int.from_bytes(fh.read(1), "big")
            param_4 = int.from_bytes(fh.read(1), "big")
            param_5 = int.from_bytes(fh.read(1), "big")
            param_6 = int.from_bytes(fh.read(1), "big")
            param_7 = int.from_bytes(fh.read(2), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1}, {param_2}, {param_3}, {param_4}, {param_5}, {param_6}, {param_7})"])
        case 39:
            param_1 = int.from_bytes(fh.read(2), "big")
            param_2 = int.from_bytes(fh.read(2), "big")
            param_3 = int.from_bytes(fh.read(2), "big")
            param_4 = int.from_bytes(fh.read(2), "big")
            cmd_list.extend([f"subcmd_{sub_command}({param_1}, {param_2}, {param_3}, {param_4})"])
        case 40:
            cmd_list.append("deleteActorContainer(actor);")
        case 41:
            param_1 = int.from_bytes(fh.read(1), "big")
            cmd_list.extend([
                "seal_paad* paad = getSealPaad(actor);",
                "if (paad) {",
                f"paad->field_0x35 = {param_1};",
                "}"
            ])
        case 42:
            cmd_list.extend([
                "seal_paad* paad = getSealPaad(actor);",
                "if (paad) {",
                "paad->field_0x35 += 1;",
                "}"
            ])
        case 43:
            cmd_list.append("actor->rendering_parameters->field_0x88 = (actor->field_0xDE < 0x3DA) ^ 1;")

def parseAnimationCode(code_size: int, index: int):
    with open(TEMP_CODE_FILE, "rb") as fh:
        cmd_list = []
        start = fh.tell()
        while fh.tell() < code_size:
            command = int.from_bytes(fh.read(1), "big")
            ret = 0
            cmd_list.append(f"// Command {command}, Offset: {hex(fh.tell() - start)}")
            match command:
                case 0:
                    cmd_list.append("return 0;")
                case 1:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([
                        f"actor->rendering_parameters->field_0x88 = {param_1};",
                        "return 1;"
                    ])
                case 2:
                    cmd_list.extend([
                        "if (actor->rendering_parameters->field_0x88) {",
                        "actor->rendering_parameters->field_0x88 -= 1;",
                        "}",
                        "return 1;"
                    ])
                case 3:
                    # Note: This one is a little weird
                    cmd_list.extend([
                        "while (actor->rendering_parameters->field_0x88) {",
                        "actor->rendering_parameters->field_0x88 -= 1;",
                        "}",
                        "return 1;"
                    ])
                case 4:
                    cmd_list.extend([
                        "render* pointer = actor->rendering_parameters;",
                        "if (!pointer->field_0x84) {",
                        "anim_file* file = pointer->animation_files[0];",
                        "} else {",
                        "anim_file* file = pointer->animation_files[1];",
                        "}",
                        "if (file->field_0x24 == 0.0f) {",
                        "if (file->field_0x2C == 0.0f) {",
                        "return 0;",
                        "}",
                        "if (file->field_0x34 == 0.0f) {",
                        "return 0;",
                        "}",
                        "}",
                        "pointer->sub_counter |= 1;",
                        "return 0;"
                    ])
                    # Unfinished from this point down
                case 5:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    if param_1 != 0:
                        cmd_list.extend([
                            f"actor->rendering_parameters->idle_animation_counter = {param_1 - 1};",
                            "actor->rendering_parameters->sub_counter |= 2;"
                        ])
                    cmd_list.append(f"return {1 if param_1 == 0 else 0};")
                case 6:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    difference = (param_2 - param_1) + 1
                    cmd_list.extend([
                        "int rng = (getRNGLower31() >> 0xF) %% 0x7FFF;",
                        f"unsigned char interval = rng % {difference + param_1};",
                    ])
                    if difference == 0:
                        cmd_list.append("trap(0x1C00);")
                    if difference == -1:
                        cmd_list.extend([
                            "if (rng == -0x80000000) {",
                            "trap(0x1800);"
                            "}"
                        ])
                    cmd_list.extend([
                        "char boolean = interval == 0;",
                        "if (!boolean) {",
                        "actor->rendering_parameters->idle_animation_counter = interval - 1;",
                        "actor->rendering_parameters->sub_counter |= 2;",
                        "}",
                        "return boolean;"
                    ])
                case 7:
                    cmd_list.append("actor->rendering_parameters->sub_counter |= 4;")
                case 8:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.append(f"actor->rendering_parameters->sub_counter |= {param_1};")
                case 9:
                    param_1 = int_to_float(int.from_bytes(fh.read(4), "big"))
                    if param_1 < 0:
                        param_1 = "actor->rendering_parameters->field_0x88"
                    cmd_list.extend([
                        f"actor->rendering_parameters->sound_timer = {param_1};",
                        "actor->rendering_parameters->sub_counter |= 8;"
                    ])
                case 10:
                    param_1 = int_to_float(int.from_bytes(fh.read(4), "big"))
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 11:
                    cmd_list.extend([f"cmd_{command}()"])
                case 12:
                    param_1 = int.from_bytes(fh.read(4), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 13:
                    cmd_list.extend([f"cmd_{command}()"])
                case 14:
                    cmd_list.extend([f"cmd_{command}()"])
                case 15:
                    cmd_list.extend([f"cmd_{command}()"])
                case 16:
                    cmd_list.extend([f"cmd_{command}()"])
                case 17:
                    param_1 = int.from_bytes(fh.read(4), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 18:
                    param_1 = int.from_bytes(fh.read(4), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 19:
                    param_1 = int.from_bytes(fh.read(4), "big")
                    param_2 = int.from_bytes(fh.read(4), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 20:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 21:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(4), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 22:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 23:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 24:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 25:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(4), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 26:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 27:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 28:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 29:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 30:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 31:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 32:
                    param_1 = int.from_bytes(fh.read(4), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 33:
                    param_1 = int.from_bytes(fh.read(4), "big")
                    param_2 = int.from_bytes(fh.read(4), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 34:
                    cmd_list.extend([f"cmd_{command}()"])
                case 35:
                    cmd_list.extend([f"cmd_{command}()"])
                case 36:
                    param_1 = int.from_bytes(fh.read(4), "big")
                    param_2 = int.from_bytes(fh.read(4), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 37:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 38:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 39:
                    cmd_list.extend([f"cmd_{command}()"])
                case 40:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 41:
                    cmd_list.extend([f"cmd_{command}()"])
                case 42:
                    param_1 = int.from_bytes(fh.read(4), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 43:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 44:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 45:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 46:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 47:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 48:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 49:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 50:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 51:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 52:
                    cmd_list.extend([f"cmd_{command}()"])
                case 53:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 54:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    parseSubAnimationCode(param_1, cmd_list, fh)
                    cmd_list.append("return *(int*)(0x807F5AF4);")
                case 55:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                    parseSubAnimationCode(param_1, cmd_list, fh)
                case 56:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    param_3 = int.from_bytes(fh.read(1), "big")
                    param_4 = int.from_bytes(fh.read(2), "big")
                    param_5 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2}, {param_3}, {param_4}, {param_5})"])
                case 57:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 58:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    param_3 = int.from_bytes(fh.read(1), "big")
                    param_4 = int.from_bytes(fh.read(1), "big")
                    param_5 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2}, {param_3}, {param_4}, {param_5})"])
                case 59:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    param_3 = int.from_bytes(fh.read(1), "big")
                    param_4 = int.from_bytes(fh.read(1), "big")
                    param_5 = int.from_bytes(fh.read(1), "big")
                    param_6 = int.from_bytes(fh.read(4), "big")
                    param_7 = int.from_bytes(fh.read(1), "big")
                    param_8 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2}, {param_3}, {param_4}, {param_5}, {param_6}, {param_7}, {param_8})"])
                case 60:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 61:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    param_3 = int.from_bytes(fh.read(2), "big")
                    param_4 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2}, {param_3}, {param_4})"])
                case 62:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    param_3 = int.from_bytes(fh.read(1), "big")
                    param_4 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2}, {param_3}, {param_4})"])
                case 63:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    param_3 = int.from_bytes(fh.read(1), "big")
                    param_4 = int.from_bytes(fh.read(1), "big")
                    param_5 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2}, {param_3}, {param_4}, {param_5})"])
                case 64:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 65:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    param_3 = int.from_bytes(fh.read(1), "big")
                    param_4 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2}, {param_3}, {param_4})"])
                case 66:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    param_2 = int.from_bytes(fh.read(4), "big")
                    param_3 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2}, {param_3})"])
                case 67:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    songs_cmd67 = [
                        "Move Get",
                        "Baboon Balloon",
                        "Gun Get",
                        "Twinkly Sounds",
                    ]
                    songs_cmd67_name = f"unk_song_array_{param_1}"
                    if param_1 < len(songs_cmd67):
                        songs_cmd67_name = songs_cmd67[param_1]
                    print(index, param_1)
                    cmd_list.append(f"playSong({songs_cmd67_name}, {param_2 / 255}); // Song defined from array 80746D60")
                case 68:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 69:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 70:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    param_3 = int.from_bytes(fh.read(1), "big")
                    param_4 = int.from_bytes(fh.read(1), "big")
                    param_5 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2}, {param_3}, {param_4}, {param_5})"])
                case 71:
                    cmd_list.extend([f"cmd_{command}()"])
                case 72:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 73:
                    cmd_list.extend([f"cmd_{command}()"])
                case 74:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1})"])
                case 75:
                    cmd_list.extend([f"cmd_{command}()"])
                case 76:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    param_2 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([f"cmd_{command}({param_1}, {param_2})"])
                case 77:
                    cmd_list.extend([
                        "render* pointer = actor->rendering_parameters;",
                        "if (!pointer->field_0x84) {",
                        "anim_file* file = pointer->animation_files[0];",
                        "} else {",
                        "anim_file* file = pointer->animation_files[1];",
                        "}",
                        "FUN_80617DFC(actor, file->animation_timers[0]);"
                    ])
                case 78:
                    # TODO: Fully decomp this
                    param_1 = int.from_bytes(fh.read(1), "big")
                    param_2 = int.from_bytes(fh.read(2), "big")
                    extra_params = []
                    if param_1 in [1, 2, 3, 4, 5, 6, 7]:
                        extra_params = [int.from_bytes(fh.read(2), "big")]
                    cmd_list.append("FUN_80617DFC(actor, actor->rendering_parameters->field_0x8A);")
                case 79:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.append(f"FUN_80613CA8(actor, {param_1}, 0.0f, 0);")
                case 80:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.append(f"FUN_80613BA0(actor, {param_1}, 0.0f, 1.0f);")
                case 81:
                    cmd_list.append("actor->rendering_parameters->field_0x84 = 1;")
                case 82:
                    cmd_list.append("actor->rendering_parameters->field_0x84 = 0;")
                case 83:
                    cmd_list.extend([
                        "render* pointer = actor->rendering_parameters;",
                        "if (!pointer->field_0x84) {",
                        "anim_file* file = pointer->animation_files[0];",
                        "} else {",
                        "anim_file* file = pointer->animation_files[1];",
                        "}",
                        "file->field_0x14 = 0.0f;",
                        "file->field_0x18 = file->field_0x12 - 1;",
                        "file->field_0x1C = file->field_0x4;",
                        "return 1;"
                    ])
                case 84:
                    cmd_list.append("return 0;")
                case 85:
                    cmd_list.append("actor->field_0x11C->control_state_progress += 1;")
                case 86:
                    param_1 = int.from_bytes(fh.read(4), "big")
                    cmd_list.append(f"actor->rendering_parameters->field_0x8C = {param_1};")
                case 87:
                    cmd_list.extend([
                        "render* pointer = actor->rendering_parameters;",
                        "float fvar = 1.0f;",
                        "if (pointer->field_0x30 & 1) {",
                        "fvar = CurrentLagSpeedBoost;",
                        "fvar *= 0.5f;",
                        "}",
                        "pointer->field_0x8C -= fvar;",
                        "if (pointer->field_0x8C > 0.0f) {",
                        "return 0;",
                        "}",
                        "return 1;"
                    ])
                case 88:
                    param_1 = int.from_bytes(fh.read(2), "big")
                    cmd_list.extend([
                        "render* pointer = actor->rendering_parameters;",
                        "pointer->field_0x5C = pointer->animation;",
                        "pointer->field_0x60 = AnimationPointer - pointer->animation_start;",
                        f"playAnimation(actor, {param_1});",
                        "AnimationPointer = pointer->animation_current;",
                        "return *(int*)(0x807F5AF4);"
                    ])
                case 89:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    cmd_list.append(f"actor->field_0x17C->field_0xD |= {param_1};")
                case 90:
                    param_1 = int.from_bytes(fh.read(1), "big")
                    cmd_list.extend([
                        "render* pointer = actor->rendering_parameters;",
                        "if (!pointer->field_0x84) {",
                        "anim_file* file = pointer->animation_files[0];",
                        "} else {",
                        "anim_file* file = pointer->animation_files[1];",
                        "}",
                        "FUN_80614644(actor, file, *(char*)(0x80746D5C));",
                        "char boolean = *(char*)(0x80746D5C) == 0;",
                        f"*(char*)(0x80746D5C) += {param_1};",
                        "if (boolean) {",
                        "*(char*)(0x80746D5C) = 0;",
                        "}",
                        "return 1;"
                    ])
                case 91:
                    cmd_list.append("return 1;")
        if fh.tell() != code_size:
            print("ERROR:",index, fh.tell(), code_size)
        tabbing = 0
        with open(f"../bin/animations/anim_{index}.txt", "w") as fh:
            for x in cmd_list:
                if x[0] == "}":
                    tabbing -= 1
                txt = x
                for y in range(tabbing):
                    txt = f"\t{txt}"
                fh.write(f"{txt}\n")
                if x[-1] == "{":
                    tabbing += 1



def getAnimationDefinitionFile():
    ptr_offset = 0x101C50
    write_path = "../bin/animations/"
    anim_pointers = []
    with open("../dk64.z64","rb") as fh:
        fh.seek(ptr_offset + (0xD << 2))
        def_table = int.from_bytes(fh.read(4), "big") + ptr_offset
        fh.seek(def_table)
        file_start = int.from_bytes(fh.read(4), "big") + ptr_offset
        file_end = int.from_bytes(fh.read(4), "big") + ptr_offset
        file_size = file_end - file_start
        fh.seek(file_start)
        data = fh.read(file_size)
        with open(f"../{DEF_FILE}","wb") as fg:
            fg.write(zlib.decompress(data, (15 + 32)))
    size = 0x1140 # TODO: Seems like there's more to this file
    count = size >> 2
    if not os.path.exists(write_path):
        os.mkdir(write_path)
    with open(f"../{DEF_FILE}","rb") as fg:
        fg.read()
        def_file_size = fg.tell()
        fg.seek(0)
        for x in range(count):
            anim_pointers.append(int.from_bytes(fg.read(4), "big"))
        for xi, x in enumerate(anim_pointers):
            fg.seek(x)
            end = def_file_size
            if xi < (len(anim_pointers) - 1):
                end = anim_pointers[xi + 1]
            code_size = end - x
            code = fg.read(code_size)
            with open(TEMP_CODE_FILE,"wb") as fi:
                fi.write(code)
            parseAnimationCode(code_size, xi)

getAnimationDefinitionFile()