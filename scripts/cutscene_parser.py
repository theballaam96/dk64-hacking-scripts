import os
import zlib
from lib import getFilePath, getROMData, getSafeFolderName, maps, Version

dump_unused = True

def readFile(file_data,start,end):
	return int.from_bytes(file_data[start:end],"big")

def readFileSigned(file_data,start):
	val = int.from_bytes(file_data[start:start+2],"big")
	if val > 0x7FFF:
		val = val - 0x10000
	return val

def parseSubCommand(sub_command, params_lst):
	code = []
	if sub_command == 0:
		code.append(f"Player->paad->field_6C = {params_lst[0]};")
		code.append("Player->paad->field_70 = Player->rotation.x;")
		code.append(f"Player->paad->field_74 = {params_lst[1]};")
		code.append(f"setCharacterChangeParameters(BBlast,0x0,0);")
	elif sub_command == 1:
		code.append(f"handleRap({params_lst[3]},0,200,{params_lst[0]};")
	elif sub_command == 2:
		code.append("Player->paad->field_1F0 |= 8;")
	elif sub_command == 3:
		code.append("Player->paad->field_1F0 &= 0xFFFFFFF7;")
	elif sub_command == 4:
		if params_lst[0] == 0:
			if params_lst[1] == 2:
				code.append("Player->rendering_params->field_10 = 0xFFFF;")
				code.append("displaySprite(Player,0x80747750);")
				if params_lst[2]:
					code.append(f"FUN_80614D00(Player,{params_lst[2]},0);")
		else:
			code.append(f"FUN_80724994(3,{params_lst[0]},{params_lst[1]},{params_lst[2]});")
	elif sub_command == 5:
		code.append(f"spawnCharacter({params_lst[0]},0,0,0,0,0,0);")
	elif sub_command == 6:
		code.append(f"void* uvar0 = getSpawnerTiedActor({params_lst[0]});")
		code.append(f"setCutsceneTarget(uvar0,{params_lst[1] & 0xFF});")
	elif sub_command == 7:
		code.append(f"changeCutsceneState({params_lst[0] & 0xFF},{params_lst[1] & 0xFF})")
	elif sub_command == 8:
		code.append(f"setCutsceneIndex({params_lst[0] & 0xFF});")
	elif sub_command == 9:
		code.append(f"FUN_8061DAAC({params_lst[0]},{params_lst[1]},{params_lst[2]});")
	elif sub_command == 10:
		if params_lst[0] == 0:
			code.append("void* uvar0 = getSpawnerTiedActor(1,0);")
			code.append("int uvar1 = 2;")
			code.append("while (uvar0 != 0) {")
			if params_lst[1] == 0:
				code.append("Player->obj_params_bitfield &= 0xFFFFFFFB;")
			else:
				code.append("Player->obj_params_bitfield |= 4;")
			code.append("uvar0 = getSpawnerTiedActor(uvar1,0);")
			code.append("uvar1 += 1;")
			code.append("}")
	elif sub_command == 11:
		code.append(f"FUN_807289E8({params_lst[0]},{params_lst[1]},{params_lst[2]},{params_lst[3]});")
	elif sub_command == 12:
		code.append(f"int uvar0 = {params_lst[0]};")
		code.append(f"FUN_8067AB20(CameraPointer,{params_lst[1]},0,1,&uvar0,0);")
	elif sub_command == 13:
		code.append(f"int uvar0 = {params_lst[0]};")
		code.append(f"FUN_8067AB20(CameraPointer,{params_lst[1]},0,0x10,&uvar0,0);")
		code.append(f"int sstack = 0xFFFF;")
		code.append(f"FUN_8067AB20(CameraPointer,{params_lst[1]},0,0xE,&uvar0,0);")
	elif sub_command == 14:
		code.append(f"FUN_80729AA4({params_lst[0] & 0xFF});")
	elif sub_command == 15:
		code.append(f"command_{sub_command}({params_lst[0]},{params_lst[1]},{params_lst[2]},{params_lst[3]})")
	elif sub_command == 0x10:
		code.append(f"FUN_8061F0B0(CameraPointer,{params_lst[1] & 0xFF},{params_lst[0]});")
	elif sub_command == 0x11:
		code.append(f"FUN_806291B4({params_lst[0] & 0xFF});")
	elif sub_command == 0x12:
		code.append(f"int uvar0 = {params_lst[0]};")
		code.append(f"FUN_8067AB20(CameraPointer,{params_lst[1]},0,0x14,&uvar0,0);")
	elif sub_command == 0x13:
		if params_lst[0] == 0:
			code.append("int* uvar0 = Player;")
			code.append("FUN_80672C30(Player);")
		else:
			code.append(f"int* uvar0 = getSpawnerTiedActor({params_lst[0]},0);")
		code.append(f"FUN_80724B5C({params_lst[1]&0xFF},{params_lst[2]&0xFF},uvar0->xPos,uvar0->yPos,uvar0->zPos);")
		code.append("int* uvar1 = uvar0;")
		code.append("FUN_8067A69C(0, uvar0, uvar0->xPos, uvar0->zPos, 2, 1);")
		code.append("float fvar0 = uvar0->yPos;")
		code.append(f"int uvar2 = {int((params_lst[1] << 0xC) / 0x168)};")
		code.append("uvar0->rotation.z = uvar2;")
		code.append("uvar0->rotation.x = uvar2;")
		code.append("uvar0->field_9C = fvar0;")
		code.append("renderActor(uvar0,0);")
		code.append("FUN_80614A64(uvar0);")
	elif sub_command == 0x14:
		if params_lst[0] > 0x7FF:
			if params_lst[1] < 0x800:
				code.append("double dvar0 = DOUBLE_807580C8;")
				if params_lst[0] != 0:
					code.append(f"dvar0 = ({params_lst[0]}/DOUBLE_807580B8) * DOUBLE_807580C0;")
				code.append("if (dvar0 < 0) {")
				code.append("dvar0 = -1;")
				code.append("}")
				code.append(f"playSFX_LowLevel(SFXLowerBank,{params_lst[1]},dvar0,0x3F);")
			else:
				code.append("double dvar0 = DOUBLE_807580E8;")
				if params_lst[0] != 0:
					code.append(f"dvar0 = ({params_lst[0]}/DOUBLE_807580D8) * DOUBLE_807580E0;")
				code.append("if (dvar0 < 0) {")
				code.append("dvar0 = -1;")
				code.append("}")
				code.append(f"playSFX_LowLevel(SFXUpperBank,{params_lst[1]-0x7FF},dvar0,0x3F);")
		else:
			code.append("int uvar0 = 0;")
			if params_lst[0] == 0:
				code.append("void* uvar1 = Player;")
				code.append("void* uvar2 = Player;")
			else:
				code.append(f"void* uvar2 = getSpawnerTiedActor({params_lst[0]},0);")
			code.append(f"*(short*)(0x807F5D7C) = FUN_806086CC(0,0,uvar2->zPos,{params_lst[1] & 0xFF});")
	elif sub_command == 0x15:
		code.append(f"modifyObjectState({params_lst[0]},{params_lst[1]&0xFF});")
	elif sub_command == 0x16:
		code.append(f"void* uvar0 = getSpawnerTiedActor({params_lst[0]},0);")
		code.append("if (uvar0 != 0) {")
		code.append("if ((*(int*)(0x807FBB68) & 2) == 0) {")
		code.append("attachActorToVehicle(Player,uvar0,0x3E19999A);")
		code.append("character_change_pointer->field_2C0 = 1")
		code.append("} else {")
		code.append("attachActorToVehicle(Player,uvar0,uvar0->rendering_params->field_38);")
		code.append("}")
		code.append("clearTagSlide(Player);")
		code.append("Player->obj_params_bitfield |= 4;")
		code.append("uvar0->control_state = 0x40;")
	elif sub_command == 0x17:
		if params_lst[1] == 0:
			code.append(f"playSong({params_lst[0]},f12);")
		else:
			code.append(f"playSong({params_lst[0]},{params_lst[1]}/DOUBLE_807580F8);")
	elif sub_command == 0x18:
		code.append("FUN_8070E8DC(1);")
	elif sub_command == 0x19:
		uvar0 = params_lst[0]
		if params_lst[0] < 1:
			uvar0 = -params_lst[0]
		if uvar0 < 1:
			code.append("FUN_80737924((&DAT_807F5D70)[0]);")
		else:
			uvar1 = -params_lst[0]
			if params_lst[0] > 0:
				uvar1 = params_lst[0]
			code.append(f"int uvar1 = {uvar1}")
			code.append("FUN_80737924((&DAT_807F5D70)[uvar]);")
	elif sub_command == 0x1A:
		code.append("FUN_80737924(SFXArray[*(short*)(0x807F5D7C)]);")
	elif sub_command == 0x1B:
		code.append(f"playMusic({params_lst[0]},0);")
	elif sub_command == 0x1C:
		code.append(f"int* uvar0 = getActorFromSpawnerTriggerOrPlayerIfZero({params_lst[0]});")
		code.append("uvar0->rotation.x = character_change_pointer->field_2C8 & 0xFFF;")
	elif sub_command == 0x1D:
		code.append("pauseCutscene();")
	elif sub_command == 0x1E:
		code.append("spawnActorWrapper(0x108,0x1D);")
		code.append(f"PTR_DAT_807FBB44->text_file = {params_lst[0]}")
		code.append(f"loadText(PTR_DAT_807FBB44,{params_lst[0]},{params_lst[1]&0xFF});")
	elif sub_command == 0x1F:
		code.append(f"command_{sub_command}({params_lst[0]},{params_lst[1]},{params_lst[2]},{params_lst[3]})")
	elif sub_command == 0x20:
		code.append(f"int* uvar0 = getSpawnerTiedActor({params_lst[0]},0);")
		code.append("if (uvar0 != 0) {")
		code.append("attachActorToVehicle(uvar0,Player,Player->rendering_params->field_38)")
		code.append("uvar0->control_state = 0x77;")
		code.append("uvar0->control_state_progress = 0;")
		code.append("}")
	elif sub_command == 0x21:
		code.append("FUN_8061C2C4(CameraPointer,0x8000);")
	elif sub_command == 0x22:
		if params_lst[0] == 0:
			code.append("deathwarp(Player);")
		else:
			code.append(f"initMapChange({params_lst[0]},{params_lst[1]});")
	elif sub_command == 0x23:
		code.append(f"TransitionSpeed = {params_lst[1]};")
		code.append(f"TransitionType = {params_lst[0]};")
	elif sub_command == 0x24:
		code.append(f"FUN_80724994(1,{params_lst[0]},{params_lst[1]},{params_lst[2]});")
	elif sub_command == 0x25:
		code.append("FUN_806F397C();")
	elif sub_command == 0x26:
		code.append(f"FUN_80641874({params_lst[0]},{params_lst[1]});")
	elif sub_command == 0x27:
		code.append("FUN_80656E58();")
		code.append("FUN_80656E58();")
		code.append("FUN_80656E58();")
		code.append("FUN_80656E58();")
	elif sub_command == 0x28:
		code.append(f"int* uvar0 = getSpawnerTiedActor({params_lst[0]},0);")
		code.append(f"int* uvar1 = getSpawnerTiedActor({params_lst[1]},0);")
		code.append("if ((uvar0 != 0) && (uvar1 != 0)) {")
		code.append("attachActorToVehicle(uvar0,uvar1,uvar1->rendering_params->field_38);")
		code.append("FUN_80613CA8(uvar0,uvar1->rendering_params->field_10,uvar1->rendering_params->field_4,0);")
		code.append("FUN_8061421C(uvar0);")
		code.append("uvar0->obj_params_bitfield |= 4;")
		code.append("uvar1->obj_params_bitfield &= 0xFFFFFFFB;")
		code.append("}")
	elif sub_command == 0x29:
		code.append("if (isISGActive() == 0) {")
		code.append(f"initTransitionWGamemode({params_lst[0]},{params_lst[1]});")
		code.append("}")
	elif sub_command == 0x2A:
		code.append(f"int* uvar0 = getSpawnerTiedActor({params_lst[0]},0);")
		code.append("if (uvar0 != 0) {")
		code.append("uvar0->control_state = 0x3C;")
		code.append("}")
	elif sub_command == 0x2B:
		code.append(f"setIntroStoryPlaying({params_lst[0]});")
	elif sub_command == 0x2C:
		code.append(f"int* uvar0 = getActorFromSpawnerTriggerOrPlayerIfZero({params_lst[0]});")
		code.append(f"FUN_80724B5C({params_lst[1]&0xFF},{params_lst[2]&0xFF},0xDC,0xD8,afStack44);")
		code.append(f"int uvar1 = FUN_80665DE0(afStack44[0],uvar0->xPos,uvar0->zPos);")
		code.append("uvar0->rotation.x = uvar1;")
	elif sub_command == 0x2D:
		code.append(f"FUN_8061CF80({params_lst[0]};)")
	elif sub_command == 0x2E:
		code.append(f"int* uvar0 = getActorFromSpawnerTriggerOrPlayerIfZero({params_lst[0]});")
		code.append(f"uvar0->field_15E = {params_lst[1] & 0xFF};")
	elif sub_command == 0x2F:
		code.append(f"modifyObjectState({params_lst[0]},{params_lst[3]}")
		if params_lst[1] != 0:
			code.append(f"modifyObjectState({params_lst[1]},{params_lst[3]}")
		if params_lst[2] != 0:
			code.append(f"modifyObjectState({params_lst[2]},{params_lst[3]}")
	elif sub_command == 0x30:
		code.append(f"int* uvar0 = getActorFromSpawnerTriggerOrPlayerIfZero({params_lst[0]});")
		if params_lst[1] > 0x7FF:
			code.append("uvar0->obj_params_bitfield &= 0xFF7FFFFF;")
		else:
			code.append(f"uvar0->red = {params_lst[1] & 0xFF}")
			code.append(f"uvar0->green = {params_lst[2] & 0xFF}")
			code.append(f"uvar0->blue = {params_lst[3] & 0xFF}")
			code.append("uvar0->obj_params_bitfield |= 0x800000;")
	elif sub_command == 0x31:
		if params_lst[0] == 0:
			code.append(f"FUN_80721560(0x20,0x82,0,{params_lst[0]},{params_lst[1] & 0xFF},{params_lst[2] & 0xFF});")
			code.append("FUN_807215D0(1,0);")
		else:
			code.append(f"FUN_80721560(0x20,0x82,0,100,100);")
			code.append("FUN_807215D0(1,0);")
	elif sub_command == 0x32:
		code.append(f"FUN_8065F49C({params_lst[0]},{params_lst[1]},{params_lst[2]},{params_lst[3]} * DOUBLE_807580A8);") # Water Something?
	elif sub_command == 0x33:
		code.append(f"int* uvar0 = getActorFromSpawnerTriggerOrPlayerIfZero({params_lst[0]});")
		code.append("int* uvar1 = uvar0->field_17C")
		code.append("uvar1->field_30 = 0xFE;")
		code.append(f"uvar1->field_33 = {params_lst[1]};")
		code.append(f"uvar1->field_22 = {params_lst[2]};")
		code.append(f"uvar1->field_32 = {params_lst[3]};")
		code.append("uvar1->field_31 = 1;")
	elif sub_command == 0x34:
		code.append(f"int* uvar0 = getActorFromSpawnerTriggerOrPlayerIfZero({params_lst[0]});")
		code.append("uvar0->field_17C->field_30 = 0xFF;")
	elif sub_command == 0x35:
		if params_lst[0] == 0:
			code.append("BananaMedalGet();")
	elif sub_command == 0x36:
		code.append(f"tagKong({params_lst[0]});")
		code.append("clearGun(Player);")
	elif sub_command == 0x37:
		if params_lst[0] == 0:
			code.append("int* uvar0 = Player;")
		else:
			code.append(f"int* uvar0 = getSpawnerTiedActor({params_lst[0]},0);")
		code.append("FUN_80605314(uvar0,0);")
	elif sub_command == 0x38:
		if params_lst[0] == 0:
			code.append("int* uvar0 = Player;")
		else:
			code.append(f"int* uvar0 = getSpawnerTiedActor({params_lst[0]},0);")
		code.append(f"FUN_80604CBC(uvar0,{params_lst[1]},0,1);")
	elif sub_command == 0x39:
		code.append(f"int* uvar0 = getActorFromSpawnerTriggerOrPlayerIfZero({params_lst[0]});")
		code.append(f"FUN_8070D8C0(uvar0,{params_lst[1]},{params_lst[2]})")
	elif sub_command == 0x3A:
		code.append("preventTransition();")
	elif sub_command == 0x3B:
		code.append(f"int* uvar0 = getActorFromSpawnerTriggerOrPlayerIfZero({params_lst[0]});")
		code.append(f"uvar0->field_146 = {params_lst[1]};")
	elif sub_command == 0x3C:
		code.append("int* uvar0 = getSpawnerTiedActor(1,0);")
		code.append(f"uvar0->field_17C->field_D |= {params_lst[0]};")
	elif sub_command == 0x3D:
		code.append("initMapChange(PreviousMap,0);")
	elif sub_command == 0x3E:
		code.append("initMapChange(0x22,0xC);")
	elif sub_command == 0x3F:
		code.append(f"handleEndSequence({params_lst[0]},{params_lst[1]},{params_lst[2]});")
	elif sub_command == 0x40:
		code.append(f"loadEndSequence(0);")
	elif sub_command == 0x41:
		code.append("exitMinigameOrBoss();")
	elif sub_command == 0x42:
		if params_lst[1] != 0:
			code.append(f"spawnKRoolText({params_lst[0] & 0xFF},{params_lst[1]},{params_lst[2]});")
		else:
			code.append(f"spawnKRoolText({params_lst[0] & 0xFF},0x5A,{params_lst[2]});")
	elif sub_command == 0x43:
		code.append("if (isISGActive() == 0) {")
		code.append(f"ExitWarp = {params_lst[2] & 0xFF};")
		code.append(f"initTransitionWGamemode({params_lst[0]},{params_lst[1]});")
		code.append("}")
	elif sub_command == 0x44:
		code.append(f"FUN_80602488({params_lst[0]});")
	elif sub_command == 0x45:
		code.append("setSpawnerTiedActorControlState(2,40);")
	else:
		code.append(f"command_{sub_command}({params_lst[0]},{params_lst[1]},{params_lst[2]},{params_lst[3]})")
	return code

pointer_table_offset = 0
cutscene_table_index = 8
version = Version.us

header_info = []
base_info = []
cutscene_info = []
point_info = []

def makeCodeFile(folder,cutscene_index,cutscene_db,point_db,unused_segments,is_last):
	cf = f"{folder}/cutscene_{cutscene_index}.txt"
	with open(cf,"w") as codefile:
		if cutscene_index < len(cutscene_db):
			focused_info = cutscene_db[cutscene_index]
			for point_index in range(focused_info["count"]):
				focused_point = focused_info["point_sequence"][point_index];
				focused_length = focused_info["point_durations"][point_index];
				codefile.write(f"Point {point_index}: Item {focused_point} for {focused_length} frames\n")
				indent_level = 0
				for pointdata in point_db:
					if pointdata["segment"] == focused_point:
						if focused_point in unused_segments:
							unused_segments.remove(focused_point)
						if "code" in pointdata:
							for codeitem in pointdata["code"]:
								if codeitem[:1] == "}":
									indent_level -= 1;
								if indent_level < 0:
									indent_level = 0
								extra_indent = ""
								for x_i in range(indent_level):
									extra_indent += "\t"
								codefile.write(f"{extra_indent}\t{codeitem}\n")
								if codeitem[-1:] == "{":
									indent_level += 1
						elif "points" in pointdata:
							point_idx = 0
							codefile.write("\tCamera Path:\n")
							for pt in pointdata["points"]:
								point_idx += 1
								codefile.write(f"\t\tPoint {point_idx}\n")
								codefile.write("\t\t\tPosition:\n")
								codefile.write(f"\t\t\t\tX: {pt['x']}\n")
								codefile.write(f"\t\t\t\tY: {pt['y']}\n")
								codefile.write(f"\t\t\t\tZ: {pt['z']}\n")
								codefile.write(f"\t\t\tZoom: {pt['zoom']}\n")
								codefile.write(f"\t\t\tRoll: {pt['roll']}\n")
								if pointdata["command"] == 4:
									codefile.write("\t\t\tRotation:\n")
									codefile.write(f"\t\t\t\tX1: {pt['rot']['x1']}\n")
									codefile.write(f"\t\t\t\tY: {pt['rot']['y1']}\n")
									codefile.write(f"\t\t\t\tX2: {pt['rot']['x2']}\n")
									codefile.write("\t\t\tUnknown:\n")
									for a_ in pt['unk']:
										codefile.write(f"\t\t\t\t{a_}\n")
						else:
							if "read" in pointdata:
								a_ = []
								for b_ in pointdata["read"]:
									b__ = []
									for c_ in b_:
										b__.append(hex(c_))
									a_.append(b__)
								codefile.write(f"\tCommand: {pointdata['command']}, Info: {a_}\n")
							else:
								codefile.write(f"\tCommand: {pointdata['command']}\n")
	empty = False
	with open(cf,"r") as codefile:
		if len(codefile.read()) == 0:
			empty = True
	if empty:
		if os.path.exists(cf):
			os.remove(cf)
	unused_file = f"{folder}/unused.txt"
	if len(unused_segments) > 0 and dump_unused and is_last:
		empty = False
		with open(unused_file,"w") as codefile:
			for seg in unused_segments:
				indent_level = 0
				for pointdata in point_db:
					if pointdata["segment"] == seg:
						codefile.write(f"Item {seg}:\n")
						if "code" in pointdata:
							for codeitem in pointdata["code"]:
								if codeitem[:1] == "}":
									indent_level -= 1;
								if indent_level < 0:
									indent_level = 0
								extra_indent = ""
								for x_i in range(indent_level):
									extra_indent += "\t"
								codefile.write(f"{extra_indent}\t{codeitem}\n")
								if codeitem[-1:] == "{":
									indent_level += 1
						elif "points" in pointdata:
							point_idx = 0
							codefile.write("\tCamera Path:\n")
							for pt in pointdata["points"]:
								point_idx += 1
								codefile.write(f"\t\tPoint {point_idx}\n")
								codefile.write("\t\t\tPosition:\n")
								codefile.write(f"\t\t\t\tX: {pt['x']}\n")
								codefile.write(f"\t\t\t\tY: {pt['y']}\n")
								codefile.write(f"\t\t\t\tZ: {pt['z']}\n")
								codefile.write(f"\t\t\tZoom: {pt['zoom']}\n")
								codefile.write(f"\t\t\tRoll: {pt['roll']}\n")
								if pointdata["command"] == 4:
									codefile.write("\t\t\tRotation:\n")
									codefile.write(f"\t\t\t\tX1: {pt['rot']['x1']}\n")
									codefile.write(f"\t\t\t\tY: {pt['rot']['y1']}\n")
									codefile.write(f"\t\t\t\tX2: {pt['rot']['x2']}\n")
									codefile.write("\t\t\tUnknown:\n")
									for a_ in pt['unk']:
										codefile.write(f"\t\t\t\t{a_}\n")
						else:
							if "read" in pointdata:
								codefile.write(f"\tCommand: {pointdata['command']}, Info: {pointdata['read']}\n")
							else:
								codefile.write(f"\tCommand: {pointdata['command']}\n")
	return not empty

def analyzeFile(data,folder_name,file_index):
	header_info = []
	base_info = []
	cutscene_info = []
	point_info = []
	info_l = 0x30
	read_l = 0
	for x in range(0x18):
		header_info_count = readFile(data,read_l,read_l+2)
		if (header_info_count > 0):
			for y in range(header_info_count):
				info = {
					"unk0": readFile(data,info_l,info_l+2),
				}
				header_info.append(info)
				info_l += 0x12
		read_l += 2
		#print(header_info_count)
	base_count = readFile(data,info_l,info_l+2)
	info_l += 2
	if base_count > 0:
		for x in range(base_count):
			info = {
				"x": readFile(data,info_l+0x10,info_l+0x12),
				"y": readFile(data,info_l+0x12,info_l+0x14),
				"z": readFile(data,info_l+0x14,info_l+0x16),
			}
			base_info.append(info)
			info_l += 0x1C
	cutscene_count = readFile(data,info_l,info_l+2)
	info_l += 2
	#print(f"Cutscene Count: {cutscene_count}")
	if cutscene_count > 0:
		for x in range(cutscene_count):
			subcount = readFile(data,info_l,info_l+0x2)
			info_l += 2
			master_a = []
			master_b = []
			if subcount > 0:
				for y in range(subcount):
					master_a.append(readFile(data,info_l,info_l+2))
					master_b.append(readFile(data,info_l+2,info_l+4))
					info_l += 4
			master = {
				"index": x,
				"count":subcount,
				"point_sequence": master_a,
				"point_durations": master_b,
			}
			cutscene_info.append(master)
	cutscene_point_count = readFile(data,info_l,info_l+2)
	#print(f"Point Count: {cutscene_point_count}")
	count_copy = cutscene_point_count
	info_l += 2
	repeat = 0
	unk0_list = []
	seg_idx = 0
	while count_copy != 0:
		command = readFile(data,info_l+1,info_l+2)
		unk0_item = readFile(data,info_l,info_l+1)
		if unk0_item not in unk0_list:
			unk0_list.append(unk0_item)
		info = {
			"unk0": unk0_item,
			"command": command,
			"segment": seg_idx
		}
		seg_idx += 1
		orig = count_copy
		count_copy -= 1
		if command == 1:
			info["read"] = data[info_l+4:info_l+10]
			info_l += 10
		elif command == 2:
			info["read"] = data[info_l+4:info_l+12]
			info_l += 12
		elif command == 3 or command == 13:
			info["read"] = data[info_l+4:info_l+16]
			info_l += 16
		elif command == 4:
			read_lst = []
			point_lst = []
			unk_count = readFile(data,info_l+4,info_l+6)
			info_l += 0x20
			for y in range(unk_count):
				read_lst.append(data[info_l:info_l+0xE])
				point_item = {
					"x": readFileSigned(data,info_l),
					"y": readFileSigned(data,info_l+2),
					"z": readFileSigned(data,info_l+4),
					"rot":{
						"x1":readFile(data,info_l+6,info_l+7),
						"y1":readFile(data,info_l+8,info_l+9),
						"x2":readFile(data,info_l+10,info_l+11),
					},
					"zoom":readFile(data,info_l+12,info_l+13),
					"roll":readFile(data,info_l+13,info_l+14),
					"unk":[
						hex(readFile(data,info_l+7,info_l+8)),
						hex(readFile(data,info_l+9,info_l+10)),
						hex(readFile(data,info_l+11,info_l+12)),
					]
				}
				point_lst.append(point_item)
				info_l += 0xE
			info["read"] = read_lst
			info["points"] = point_lst
		elif command == 5:
			read_lst = []
			point_lst = []
			unk_count = readFile(data,info_l+4,info_l+6)
			info_l += 0x14
			for y in range(unk_count):
				read_lst.append(data[info_l:info_l+0x8])
				point_item = {
					"x": readFileSigned(data,info_l),
					"y": readFileSigned(data,info_l+2),
					"z": readFileSigned(data,info_l+4),
					"zoom": readFile(data,info_l+6,info_l+7),
					"roll": readFile(data,info_l+7,info_l+8),
				}
				point_lst.append(point_item)
				info_l += 0x8
			info["read"] = read_lst
			info["points"] = point_lst
		elif command == 10 or command == 15 or command == 16:
			info["read"] = data[info_l+4:info_l+18]
			info_l += 18
		elif command == 12:
			info["read"] = data[info_l+4:info_l+6]
			info_l += 6
		else:
			count_copy += 1
			info_l += 4
		point_info.append(info)
	for point in point_info:
		command = point["command"]
		if command == 10 or command == 15 or command == 16 or command == 17:
			point["code"] = ["LevelStateBitfield = LevelStateBitfield | 0x2000"]
		elif command == 6:
			point["code"] = ["nextCutscenePart()"]
		elif command == 11:
			point["code"] = ["cancel cutscene something"]
		elif command == 12:
			point["code"] = [f"playSong({int.from_bytes(point['read'],'big')})"]
		elif command == 14:
			point["code"] = ["playCutsceneInMap()"]
		elif command == 13:
			command_info = {
				"sub_command": int.from_bytes(point["read"][0:4],"big")
			}
			params = []
			param_count = int((len(point["read"]) - 4) / 2)
			for a in range(param_count):
				params.append(int.from_bytes(point["read"][4+(2*a):6+(2*a)],"big"))
			command_info["params"] = params
			sub_command = command_info["sub_command"]
			code = parseSubCommand(sub_command,params)
			point["code"] = code
		#print(point)
	if not os.path.exists(folder_name):
		os.mkdir(folder_name)
	file_count = 0
	unused_segments = []
	for pt in point_info:
		unused_segments.append(pt["segment"])
	for cutscene in cutscene_info:
		last = False
		if cutscene_count - 1 == cutscene["index"]:
			last = True
		made = makeCodeFile(folder_name,cutscene["index"],cutscene_info,point_info,unused_segments,last)
		if made:
			file_count += 1
	with open(f"{folder_name}/cutscenes.bin", "wb") as cs:
		cs.write(data)

file_path = getFilePath()
pointer_table_offset, version, dump_path, valid = getROMData(file_path, "cutscenes")
if valid:
	if version == Version.kiosk:
		cutscene_table_index = 7
	with open(file_path,"rb") as romfile:
		romfile.seek(pointer_table_offset + (cutscene_table_index * 4))
		pointer_table = pointer_table_offset + int.from_bytes(romfile.read(4),"big")&0x7FFFFFFF
		romfile.seek(pointer_table_offset + (cutscene_table_index * 4) + (32*4))
		tbl_size = int.from_bytes(romfile.read(4),"big")
		for map_id in range(tbl_size-1):
			map_name = maps[map_id];
			romfile.seek(pointer_table + (4 * map_id))
			file_location = pointer_table_offset + int.from_bytes(romfile.read(4),"big")&0x7FFFFFFF
			romfile.seek(pointer_table + 4 + (4 * map_id))
			file_end = pointer_table_offset + int.from_bytes(romfile.read(4),"big")&0x7FFFFFFF
			file_size = file_end - file_location
			romfile.seek(file_location)
			compress = romfile.read(file_size)
			if int.from_bytes(compress[0:1],"big") == 0x1F and int.from_bytes(compress[1:2],"big") == 0x8B:
				data = zlib.decompress(compress, 15+32)
				print(f"[{map_id+1}/{tbl_size-1}] Analyzing: {map_name}")
				analyzeFile(data,f"{dump_path}/{getSafeFolderName(map_name)}",map_id)
			else:
				data = compress
				print(f"[{map_id+1}/{tbl_size-1}] Ignoring: {map_name}")
