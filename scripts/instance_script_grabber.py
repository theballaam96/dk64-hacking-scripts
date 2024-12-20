import os
import zlib
import shutil
import gzip
from typing import BinaryIO
import math

from lib import getFilePath, getROMData, maps, object_modeltwo_types, Version

hud_items = [
	"Coloured banana",
	"Banana coin",
	"Ammo",
	"Homing ammo",
	"Orange",
	"Crystal",
	"Film",
	"Instrument",
	"GB Count?(Left)",
	"GB Count (Bottom)",
	"Banana Medal",
	"Minecart/Minigame Coin",
	"Blueprint",
	"Coloured Bananas (???)",
	"Banana coins (???)",
]

songs = [
	"Silence",
	"Jungle Japes (Starting Area)",
	"Cranky's Lab",
	"Jungle Japes (Minecart)",
	"Jungle Japes (Army Dillo)",
	"Jungle Japes (Caves/Underground)",
	"Funky's Hut",
	"Unused Coin Pickup",
	"Bonus Minigames",
	"Triangle Trample",
	"Guitar Gazump",
	"Bongo Blast",
	"Trombone Tremor",
	"Saxaphone Slam",
	"Angry Aztec",
	"Transformation",
	"Mini Monkey",
	"Hunky Chunky",
	"GB/Key Get",
	"Angry Aztec (Beetle Slide)",
	"Oh Banana",
	"Angry Aztec (Temple)",
	"Company Coin Get",
	"Banana Coin Get",
	"Going through Vulture Ring",
	"Angry Aztec (Dogadon)",
	"Angry Aztec (5DT)",
	"Frantic Factory (Car Race)",
	"Frantic Factory",
	"Snide's HQ",
	"Jungle Japes (Tunnels)",
	"Candy's Music Shop",
	"Minecart Coin Get",
	"Melon Slice Get",
	"Pause Menu",
	"Crystal Coconut Get",
	"Rambi",
	"Angry Aztec (Tunnels)",
	"Water Droplets",
	"Frantic Factory (Mad Jack)",
	"Success",
	"Start (To pause game)",
	"Failure",
	"DK Transition (Opening)",
	"DK Transition (Closing)",
	"Unused High-Pitched Japes",
	"Fairy Tick",
	"Melon Slice Drop",
	"Angry Aztec (Chunky Klaptraps)",
	"Frantic Factory (Crusher Room)",
	"Jungle Japes (Baboon Blast)",
	"Frantic Factory (R&D)",
	"Frantic Factory (Production Room)",
	"Troff 'n' Scoff",
	"Boss Defeat",
	"Angry Aztec (Baboon Blast)",
	"Gloomy Galleon (Outside)",
	"Boss Unlock",
	"Awaiting Entering the Boss",
	"Generic Twinkly Sounds",
	"Gloomy Galleon (Pufftoss)",
	"Gloomy Galleon (Seal Race)",
	"Gloomy Galleon (Tunnels)",
	"Gloomy Galleon (Lighthouse)",
	"Battle Arena",
	"Drop Coins (Minecart)",
	"Fairy Nearby",
	"Checkpoint",
	"Fungi Forest (Day)",
	"Blueprint Get",
	"Fungi Forest (Night)",
	"Strong Kong",
	"Rocketbarrel Boost",
	"Orangstand Sprint",
	"Fungi Forest (Minecart)",
	"DK Rap",
	"Blueprint Drop",
	"Gloomy Galleon (2DS)",
	"Gloomy Galleon (5DS/Submarine)",
	"Gloomy Galleon (Pearls Chest)",
	"Gloomy Galleon (Mermaid Palace)",
	"Fungi Forest (Dogadon)",
	"Mad Maze Maul",
	"Crystal Caves",
	"Crystal Caves (Giant Kosha Tantrum)",
	"Nintendo Logo (Old?)",
	"Success (Races)",
	"Failure (Races & Try Again)",
	"Bonus Barrel Introduction",
	"Stealthy Snoop",
	"Minecart Mayhem",
	"Gloomy Galleon (Mechanical Fish)",
	"Gloomy Galleon (Baboon Blast)",
	"Fungi Forest (Anthill)",
	"Fungi Forest (Barn)",
	"Fungi Forest (Mill)",
	"Generic Seaside Sounds",
	"Fungi Forest (Spider)",
	"Fungi Forest (Mushroom Top Rooms)",
	"Fungi Forest (Giant Mushroom)",
	"Boss Introduction",
	"Tag Barrel (All of them)",
	"Crystal Caves (Beetle Race)",
	"Crystal Caves (Igloos)",
	"Mini Boss",
	"Creepy Castle",
	"Creepy Castle (Minecart)",
	"Baboon Balloon",
	"Gorilla Gone",
	"DK Isles",
	"DK Isles (K Rool's Ship)",
	"DK Isles (Banana Fairy Island)",
	"DK Isles (K-Lumsy's Prison)",
	"Hideout Helm (Blast-O-Matic On)",
	"Move Get",
	"Gun Get",
	"Hideout Helm (Blast-O-Matic Off)",
	"Hideout Helm (Bonus Barrels)",
	"Crystal Caves (Cabins)",
	"Crystal Caves (Rotating Room)",
	"Crystal Caves (Tile Flipping)",
	"Creepy Castle (Tunnels)",
	"Intro Story Medley",
	"Training Grounds",
	"Enguarde",
	"K-Lumsy Celebration",
	"Creepy Castle (Crypt)",
	"Headphones Get",
	"Pearl Get",
	"Creepy Castle (Dungeon w/ Chains)",
	"Angry Aztec (Lobby)",
	"Jungle Japes (Lobby)",
	"Frantic Factory (Lobby)",
	"Gloomy Galleon (Lobby)",
	"Main Menu",
	"Creepy Castle (Inner Crypts)",
	"Creepy Castle (Ballroom)",
	"Creepy Castle (Greenhouse)",
	"K Rool's Theme",
	"Fungi Forest (Winch)",
	"Creepy Castle (Wind Tower)",
	"Creepy Castle (Tree)",
	"Creepy Castle (Museum)",
	"BBlast Final Star",
	"Drop Rainbow Coin",
	"Rainbow Coin Get",
	"Normal Star",
	"Bean Get",
	"Crystal Caves (Army Dillo)",
	"Creepy Castle (Kut Out)",
	"Creepy Castle (Dungeon w/out Chains)",
	"Banana Medal Get",
	"K Rool's Battle",
	"Fungi Forest (Lobby)",
	"Crystal Caves (Lobby)",
	"Creepy Castle (Lobby)",
	"Hideout Helm (Lobby)",
	"Creepy Castle (Trash Can)",
	"End Sequence",
	"K-Lumsy Ending",
	"Jungle Japes",
	"Jungle Japes (Cranky's Area)",
	"K Rool Takeoff",
	"Crystal Caves (Baboon Blast)",
	"Fungi Forest (Baboon Blast)",
	"Creepy Castle (Baboon Blast)",
	"DK Isles (Snide's Room)",
	"K Rool's Entrance",
	"Monkey Smash",
	"Fungi Forest (Rabbit Race)",
	"Game Over",
	"Wrinkly Kong",
	"100th CB Get",
	"K Rool's Defeat",
	"Nintendo Logo"
]

trigger_types = [
	"Unknown 0x00",
	"Unknown 0x01",
	"Unknown 0x02",
	"Boss Door Trigger", # Also sets boss fadeout type as fade instead of spin. In toolshed too??
	"Unknown 0x04",
	"Cutscene Trigger",
	"Unknown 0x06",
	"Unknown 0x07",
	"Unknown 0x08",
	"Loading Zone (0x9)",
	"Cutscene Trigger (0xA)",
	"Unknown 0x0B",
	"Loading Zone + Objects", # Allows objects through
	"Loading Zone (0xD)",
	"Unknown 0x0E",
	"Warp Trigger", # Factory Poles
	"Loading Zone (0x10)",
	"Loading Zone (0x11)", # Snide's, Return to Parent Map?
	"Coin Shower Trigger",
	"Detransform Trigger (0x13)",
	"Boss Loading Zone", # Takes you to the boss of that level
	"Autowalk Trigger",
	"Sound Trigger",
	"Cutscene Trigger (0x17)",
	"Unknown 0x18",
	"Unknown 0x19",
	"Gravity Trigger",
	"Slide Trigger", # Beetle Slides
	"Unslide Trigger",
	"Loading Zone (Zipper)",
	"Song Trigger",
	"Unknown 0x1F",
	"Cutscene Trigger (0x20)",
	"Unknown 0x21",
	"Unknown 0x22",
	"Unknown 0x23",
	"Detransform Trigger (0x24)",
	"Chunk Texture Load Trigger",
	"K. Lumsy Code Activator", # In BFI too, but seems like functionality in BFI has been stripped from final
]

relevant_pointer_tables = [
	{
		"index": 1,
		"name": "Map Geometry",
		"output_filename": "geometry.bin",
	},
	{
		"index": 2,
		"name": "Map Walls",
		"output_filename": "walls.bin",
	},
	{
		"index": 3,
		"name": "Map Floors",
		"output_filename": "floors.bin",
	},
	{
		"index": 8,
		"name": "Map Cutscenes",
		"output_filename": "cutscenes.bin",
	},
	{
		"index": 9,
		"name": "Map Setups",
		"output_filename": "setup.bin",
	},
	{
		"index": 10,
		"name": "Map Data 0xA",
		"output_filename": "map_0x0a.bin",
	},
	{
		"index": 15,
		"name": "Map Paths",
		"output_filename": "paths.bin",
	},
	{
		"index": 16,
		"name": "Map Paths",
		"output_filename": "character_spawners.bin",
	},
	{
		"index": 18,
		"name": "Map Loading Zones",
		"output_filename": "loading_zones.bin",
	},
	{
		"index": 21,
		"name": "Map Data 0x15",
		"output_filename": "map_0x15.bin",
	},
	{
		"index": 23,
		"name": "Map Exits",
		"output_filename": "exits.bin",
	},
]

num_tables = 32
pointer_tables = []
main_pointer_table_offset = 0
setup_table_index = 9
script_table_index = 10
files = {}
tab_indentation = 0
folder_removal = []
version = Version.us

def getTriggerTypeName(index):
	if (index < (len(trigger_types) - 1)):
		return trigger_types[index]
	return "Type %s" % (hex(index))

def getSongName(index):
	if (index < (len(songs) - 1)):
		return songs[index]
	return "Song %s" % (hex(index))

def getTOrF(value):
	if value == 0:
		return "False"
	return "True"

def getSetOrNot(value):
	if value == 0:
		return "Don't Set"
	return "Set"

def display(file, string):
	global tab_indentation;

	if (string[-1:] != "{"):
		if (string[-1:] != "}"):
			string += ";"
	for x in range(tab_indentation):
		string = "\t" + string;
	if string[-1:] == "{":
		tab_indentation += 1;
	elif string[-1:] == "}":
		tab_indentation -= 1;
	file.write(string + "\n")

def grabConditional(param_1, ScriptCommand,params,behaviour,param_3,file):
	functionType = ScriptCommand & 0x7FFF
	inverseFlag = ScriptCommand & 0x8000
	inverseFlagChar = ""
	inverseFlagInvertedChar = "!"
	if inverseFlag != 0:
		inverseFlag = 1;
		inverseFlagChar = "!"
		inverseFlagInvertedChar = ""
	else:
		inverseFlagChar = ""
		inverseFlagInvertedChar = "!"
	if functionType == 0:
		display(file, "if (%strue) {" % (inverseFlagChar))
	elif functionType == 1:
		display(file, "if (*(byte *)(behaviour + %s) %s== %s) {" % (hex(params[1] + 0x48), inverseFlagChar, str(params[0])))
	elif functionType == 2:
		display(file, "x2_successful = 0")
		display(file, "x2_focusedPlayerNumber = 0")
		display(file, "if (player_count != 0) {")
		display(file, "do {")
		display(file, "x2_focusedPlayerNumber_ = x2_focusedPlayerNumber")
		display(file, "x2_focusedPlayerNumber = (x2_focusedPlayerNumber_ + 1) & 0xFF")
		display(file, "if (*(byte *)(character_change_pointer[x2_focusedPlayerNumber_]->does_player_exist) != 0) {")
		display(file, "x2_focusedPlayerPointer = *(int *)(character_change_pointer[x2_focusedPlayerNumber_)]->character_pointer)")
		display(file, "if (*(byte *)(x2_focusedPlayerPointer->locked_to_pad) == 1) {")
		display(file, "if (this->id == *(short *)(x2_focusedPlayerPointer->standingOnObjectM2Index)) {")
		display(file, "x2_successful = 1")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "} while (x2_focusedPlayerNumber < player_count)")
		display(file, "}")
		display(file, "if (x2_successful %s== 1) {" % (inverseFlagChar))
	elif functionType == 3:
		display(file, "if (1 == 0) {")
	elif functionType == 4:
		display(file, "if (*(ushort *)(behaviour + %s) %s== %s) {" %(hex((params[1] * 2) + 0x44), inverseFlagChar, str(params[0])))
	elif functionType == 5:
		display(file, "if (FUN_806425FC(%s,%s) %s== 0) {" % (str(params[0]), str(params[1]), inverseFlagInvertedChar))
	elif functionType == 6:
		display(file, 
			"if (*(code *)(%s)(behaviour,this->id,%s,%s) %s== 0) {" % (hex(0x80748048 + (params[0] * 4)), str(params[1]), str(params[2]), inverseFlagInvertedChar))
	elif functionType == 7:
		display(file, "if (FUN_80642500(behaviour + 0x14,%s,%s) %s== 0) {" % (str(params[0]), str(params[1]), inverseFlagInvertedChar))
	elif functionType == 8:
		display(file, "if (*(byte *)(behaviour + 0x51) %s== 0) {" % (inverseFlagInvertedChar))
	elif functionType == 9:
		display(file, "if (*(byte *)(behaviour + 0x52) %s== 0) {" % (inverseFlagInvertedChar))
	elif functionType == 10:
		display(file, "xA_successful = 0")
		display(file, "xA_focusedPlayerNumber = 0")
		display(file, "if (player_count != 0) {")
		display(file, "do {")
		display(file, "xA_focusedPlayerNumber_ = xA_focusedPlayerNumber")
		display(file, "xA_focusedPlayerNumber = (xA_focusedPlayerNumber_ + 1) & 0xFF")
		display(file, "if (*(byte *)(character_change_pointer[xA_focusedPlayerNumber_]->does_player_exist) != 0) {")
		display(file, "xA_focusedPlayerPointer = *(int *)(character_change_pointer[xA_focusedPlayerNumber_]->character_pointer)")
		display(file, "xA_successful = 0")
		display(file, "if (*(byte *)(xA_focusedPlayerPointer->locked_to_pad) == 2) {")
		display(file, "if (this->id == *(short *)(xA_focusedPlayerPointer->standingOnObjectM2Index)) {")
		display(file, "xA_successful = 1")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "} while (xA_focusedPlayerNumber < player_count)")
		display(file, "}")
		display(file, "if (xA_successful %s== 1) {" % (inverseFlagChar))
	elif functionType == 11:
		display(file, "xB_successful = 0")
		display(file, "xB_focusedPlayerNumber = 0")
		display(file, "if (player_count != 0) {")
		display(file, "do {")
		display(file, "xB_focusedPlayerNumber_ = xB_focusedPlayerNumber")
		display(file, "xB_focusedPlayerNumber = (xB_focusedPlayerNumber_ + 1) & 0xFF")
		display(file, "if (*(byte *)(character_change_pointer[xB_focusedPlayerNumber_]->does_player_exist) != 0) {")
		display(file, "xB_focusedPlayerPointer = *(int *)(character_change_pointer[xB_focusedPlayerNumber_]->character_pointer)")
		display(file, "if (*(byte *)(xB_focusedPlayerPointer->locked_to_pad) == 3) {")
		display(file, "if (*(byte *)(xB_focusedPlayerPointer->unk0x12F == %s)) {" % (str(params[0])))
		display(file, "if (this->id == *(short *)(xB_focusedPlayerPointer->standingOnObjectM2Index)) {")
		display(file, "xB_successful = 1")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "} while (xB_focusedPlayerNumber < player_count)")
		display(file, "}")
		display(file, "if (xB_successful %s== 1) {" % (inverseFlagChar))
	elif functionType == 12:
		display(file, "if (%s(((((FLOAT_807F621C == FLOAT_807F61FC) && (FLOAT_807F6220 == 1729.11706543)) && ((FLOAT_807F6224 == 3433.54956055 && ((FLOAT_807F6228 == 330 && (FLOAT_807F622C == 170)))))) && (FLOAT_807F6230 == 0)) && (FLOAT_807F6234 == 1))) {" % (inverseFlagInvertedChar))
	elif functionType == 13:
		display(file, "xC_successful = 0")
		display(file, "xC_focusedPlayerNumber = 0")
		display(file, "if (player_count != 0) {")
		display(file, "do {")
		display(file, "xC_focusedPlayerNumber_ = xC_focusedPlayerNumber")
		display(file, "xC_focusedPlayerNumber = (xC_focusedPlayerNumber_ + 1) & 0xFF")
		display(file, "if (*(byte *)(character_change_pointer[xC_focusedPlayerNumber_]->does_player_exist) != 0) {")
		display(file, "xC_focusedPlayerPointer = *(int *)(character_change_pointer[xC_focusedPlayerNumber_]->character_pointer)")
		display(file, "if (*(byte *)(xC_focusedPlayerPointer->locked_to_pad) == 1) {")
		display(file, "if (this->id == *(short *)(xC_focusedPlayerPointer->standingOnObjectM2Index)) {")
		display(file, "if (this->id == *(byte *)(xC_focusedPlayerPointer->unk0x10E == %s)) {" % (str(params[0])))
		display(file, "xC_successful = 1")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "} while (xC_focusedPlayerNumber < player_count)")
		display(file, "}")
		display(file, "if (xC_successful %s== 1) {" % (inverseFlagChar))
	elif functionType == 14:
		display(file, "if (FUN_80641F70(param_1,%s) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
	elif functionType == 15:
		display(file, "if (FUN_80723C98(*(word *) (behaviour + 0x38)) %s== 0) {" % (inverseFlagInvertedChar))
	elif functionType == 16:
		x10_conditional = "";
		x10_conditional_2 = "";
		if params[1] != -1:
			x10_conditional = "(*(byte *)(behaviour + 0x5C) != %s) || " % (str(params[1]))
		if params[0] != 0:
			x10_conditional_2 = "(FUN_8067ACC0(*(ushort *)(behaviour + 0x5E)) & %s)" % (str(params[0]))
			display(file, "if ((((*(byte *)(behaviour + 0x5C) == 0) || %s%s)) || (canHitSwitch() == 0)) {" % (x10_conditional, x10_conditional_2))
			display(file, "x10_uvar9 = 0")
			display(file, "} else {")
			display(file, "FUN_80641724(ObjectModel2ArrayPointer[id2index(this->id)].object_type)")
			display(file, "x10_uvar9 = 1")
			display(file, "}")
			display(file, "if (x10_uvar9 %s== 1) {" % (inverseFlagChar))
		else:
			if inverseFlag == 1:
				display(file, "if (true) {")
			else:
				display(file, "if (1 == 0) {")
	elif functionType == 17:
		display(file, "x11_successful = false")
		display(file, "if (loadedActorCount != 0) {")
		display(file, "x11_focusedArraySlot = &loadedActorArray")
		display(file, "x11_focusedActor = loadedActorArray")
		display(file, "while (true) {")
		display(file, "x11_focusedArraySlot = x11_focusedArraySlot + 8")
		display(file, "if ((*(uint *)(x11_focusedActor->object_properties_bitfield) & 0x2000) == 0) {")
		display(file, "if (*(int *)(x11_focusedActor->actor_type) == %s) {" % (str(params[0])))
		display(file, "if (x11_focusedActor->locked_to_pad == 1) {")
		display(file, "if (this->id == *(short *)(x11_focusedActor->standingOnObjectM2Index)) {")
		display(file, "x11_successful = true")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "if ((&loadedActorArray + (loadedActorCount * 8) <= x11_focusedArraySlot) || (x11_successful)) break;")
		display(file, "}")
		display(file, "}")
		display(file, "if (%sx11_successful) {" % (inverseFlagChar))
	elif functionType == 18:
		display(file, "x12_successful = false")
		display(file, "if (loadedActorCount != 0) {")
		display(file, "x12_focusedArraySlot = &loadedActorArray")
		display(file, "x12_focusedActor = loadedActorArray")
		display(file, "while (true) {")
		display(file, "x12_focusedArraySlot = x12_focusedArraySlot + 8")
		display(file, "if ((*(uint *)(x12_focusedActor->object_properties_bitfield) & 0x2000) == 0) {")
		display(file, "if (*(int *)(x12_focusedActor->actor_type) == %s) {" % (str(params[0])))
		display(file, "if (x12_focusedActor->locked_to_pad == 1) {")
		display(file, "if (this->id == *(short *)(x12_focusedActor->standingOnObjectM2Index)) {")
		display(file, "if (*(short *)(x12_focusedActor->unk10E) == %s) {" % (str(params[1])))
		display(file, "x12_successful = true")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "if ((&loadedActorArray + (loadedActorCount * 8) <= x12_focusedArraySlot) || (x12_successful)) break;")
		display(file, "x12_focusedActor = *x12_focusedArraySlot")
		display(file, "}")
		display(file, "}")
		display(file, "if (%sx12_successful) {" % (inverseFlagChar))
	elif functionType == 19:
		display(file, "if (isPlayerWithinDistanceOfObject(%s) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
	elif functionType == 20:
		display(file, "x14_successful_count = 0")
		display(file, "x14_focusedArraySlot = &loadedActorArray")
		display(file, "if (loadedActorCount != 0) {")
		display(file, "x14_focusedActor = loadedActorArray")
		display(file, "while (true) {")
		display(file, "x14_focusedArraySlot = x14_focusedArraySlot + 8")
		display(file, "if ((*(uint *)(x14_focusedActor->object_properties_bitfield) & 0x2000) == 0) {")
		display(file, "if (*(int *)(x14_focusedActor->actor_type) == %s) {" % (str(params[0])))
		display(file, "if (x14_focusedActor->locked_to_pad == 1) {")
		display(file, "if (this->id == *(short *)(x14_focusedActor->standingOnObjectM2Index)) {")
		display(file, "if (*(short *)(x14_focusedActor->unk10E) == %s) {" % (str(params[1])))
		display(file, "x14_successful_count = true")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "if ((&loadedActorArray + (loadedActorCount * 8) <= x14_focusedArraySlot)) break;")
		display(file, "x14_focusedActor = *x14_focusedArraySlot")
		display(file, "}")
		display(file, "}")
		display(file, "if (x14_successful_count %s== %s) {" % (inverseFlagChar, str(params[2])))
	elif functionType == 21:
		display(file, "if (FUN_80650D04(this->id,%s) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
	elif functionType == 22:
		display(file, "if ((LevelStateBitfield & %s) != 0) {" % (hex((params[0] * 0x10000) + params[1])))
	elif functionType == 23:
		display(file, "x17_successful = 0")
		display(file, "x17_focusedPlayerNumber = 0")
		display(file, "if (player_count != 0) {")
		display(file, "do {")
		display(file, "x17_focusedPlayerNumber_ = x17_focusedPlayerNumber")
		display(file, "x17_focusedPlayerNumber = (x17_focusedPlayerNumber_ + 1) & 0xFF")
		display(file, "if (*(byte *)(character_change_pointer[x17_focusedPlayerNumber_]->does_player_exist) != 0) {")
		display(file, "x17_focusedPlayerPointer = *(int *)(character_change_pointer[x17_focusedPlayerNumber_]->character_pointer)")
		display(file, "if (*(byte *)(x17_focusedPlayerPointer->control_state) == %s) {" % (str(params[0])))
		if params[1] == 0:
			display(file, "x17_successful = 1")
		else:
			display(file, "if (x17_focusedPlayerPointer->control_state_progress == %s) {" % (str(params[1])))
			display(file, "x17_successful = 1")
			display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "} while (x17_focusedPlayerNumber < player_count)")
		display(file, "}")
		display(file, "if (x17_successful %s== 1) {" % (inverseFlagChar))
	elif functionType == 24:
		display(file, "x18_successful = 0")
		display(file, "if (*(byte *)(behaviour + 0x5C) != 0) {")
		if params[1] != -1:
			display(file, "if (*(byte *)(behaviour + 0x5C) == %s){" % (str(params[1])))
		display(file, "if ((*(ushort *)(behaviour + 0x5E) == %s) && canHitSwitch() != 0) {" % (str(params[0])))
		display(file, "FUN_80641724(ObjectModel2Array[id2index(this->id)].object_type)")
		display(file, "x18_successful = 1")
		display(file, "}")
		if params[1] != -1:
			display(file, "}")
		display(file, "}")
		display(file, "if (x18_successful %s== 1) {" % (inverseFlagChar))
	elif functionType == 25:
		display(file, "if (*(int *)(PlayerPointer->ActorType) %s== %s) {" % (inverseFlagChar, str(params[0])))
	elif functionType == 26:
		display(file, "if (*(byte *)(character_change_pointer->unk0x2C0) %s== %s) {" % (inverseFlagChar, str(params[0])))
	elif functionType == 27:
		display(file, "if (*(byte *)(character_change_pointer->unk0x2C1) %s== 0){" % (inverseFlagInvertedChar))
	elif functionType == 28:
		display(file, "x1C_svar6 = 80650a70()")
		if params[1] == 0:
			if inverseFlag == 0:
				display(file, "if (x1C_svar6 < %s) {" % (str(params[2])))
			else:
				display(file, "if (x1C_svar6 >= %s) {" % (str(params[2])))
		elif params[1] == 1:
			if inverseFlag == 0:
				display(file, "if (x1C_svar6 >= %s) {" % (str(params[2])))
			else:
				display(file, "if (x1C_svar6 < %s) {" % (str(params[2])))
		else:
			display(file, "if (1 == 0) {")
	elif functionType == 29:
		if params[0] == 0:
			if inverseFlag == 0:
				display(file, "if (*(byte *)(behaviour + %s) < %s) {" % (hex(0x48 + params[2]), str(params[1])))
			else:
				display(file, "if (*(byte *)(behaviour + %s) >= %s) {" % (hex(0x48 + params[2]), str(params[1])))
		elif params[0] == 1:
			if inverseFlag == 0:
				display(file, "if (*(byte *)(behaviour + %s) >= %s) {" % (hex(0x48 + params[2]), str(params[1])))
			else:
				display(file, "if (*(byte *)(behaviour + %s) < %s) {" % (hex(0x48 + params[2]), str(params[1])))
		else:
			display(file, "if (1 == 0) {")
	elif functionType == 30:
		display(file, "if ((FUN_80726D7C() & 0xFF) %s== 0){" % (inverseFlagInvertedChar))
	elif functionType == 31:
		if inverseFlag == 0:
			display(file, "if (1 == 0) {")
		else:
			display(file, "if (true) {")
	elif functionType == 32:
		display(file, "if ((FUN_806422D8() & 0xFF) %s== 0){" % (inverseFlagInvertedChar))
	elif functionType == 33:
		display(file, "x21_successful = 0")
		display(file, "x21_focusedPlayerNumber = 0")
		display(file, "if (player_count != 0) {")
		display(file, "do {")
		display(file, "x21_focusedPlayerNumber_ = x21_focusedPlayerNumber")
		display(file, "x21_focusedPlayerNumber = (x21_focusedPlayerNumber_ + 1) & 0xFF")
		display(file, "if (*(byte *)(character_change_pointer[x21_focusedPlayerNumber_]->does_player_exist) != 0) {")
		display(file, "x21_focusedPlayerPointer = *(int *)(character_change_pointer[x21_focusedPlayerNumber_]->character_pointer)")
		display(file, "if (*(byte *)(x21_focusedPlayerPointer->control_state_progress) == %s) {" % (str(params[0])))
		display(file, "x21_successful = 1")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "if (x21_successful %s== 1) {" % (inverseFlagChar))
	elif functionType == 34:
		display(file, "if (touchingModelTwoById(%s) %s== 0) {" % (hex(params[0]), inverseFlagInvertedChar))
	elif functionType == 35:
		display(file, "if (CutsceneActive %s== 1) {" % (inverseFlagChar))
	elif functionType == 36:
		display(file, "x24_focusedActor = getSpawnerTiedActor(%s,0)" % (str(params[0])))
		display(file, "if (*(byte *)(x24_focusedActor->control_state) %s== %s) {" % (inverseFlagChar, str(params[1])))
	elif functionType == 37:
		display(file, "if (%s(*(byte *)CurrentCollectableBase->SlamLvl => %s)) {" % (inverseFlagChar, str(params[0])))
	elif functionType == 38:
		display(file, "if ((*(uint *)(PlayerPointer->unk0x368) & %s) %s== 0) {" % (hex((params[0] * 0x10000) + params[1]), inverseFlagInvertedChar))
	elif functionType == 39:
		display(file, "if ((*(uint *)(PlayerPointer->effectBitfield) & %s) %s== 0) {" % (hex((params[0] * 0x10000) + params[1]), inverseFlagInvertedChar))
	elif functionType == 40:
		display(file, "if ((*(byte *)(behaviour + 0x9A) & 1) %s== 0) {" % (inverseFlagChar))
	elif functionType == 41:
		display(file, "if (notTouchingActorSpawnerWithinRan(%s,%s,%s) %s== 0) {" % (str(params[0]), str(params[1]), str(params[2]), inverseFlagInvertedChar))
	elif functionType == 42:
		if inverseFlag == 0:
			display(file, "if (BYTE_807F61F8 != 0 || *(byte *)(PTR_0x807F61F0->control_state) == 5) {")
		else:
			display(file, "if (BYTE_807F61F8 == 0 && *(byte *)(PTR_0x807F61F0->control_state) != 5) {")
	elif functionType == 43:
		display(file, "if (BYTE_807F61F8 %s== 0) {" % (inverseFlagInvertedChar))
	elif functionType == 44:
		display(file, "if (FUN_80689BAC(%s) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
	elif functionType == 45:
		display(file, "if (checkFlag(%s>%s,'Permanent') %s== 0) {" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), inverseFlagInvertedChar))
	elif functionType == 46:
		display(file, "if (getAndSetActorSpawnerControlStateFromActorSpawnerID(%s,0,'%s') %s== %s) {" % (str(params[0]), getSetOrNot(0), inverseFlagChar, str(params[1])))
	elif functionType == 47:
		display(file, "if ((isCharacterSpawnerInState7(%s) & 0xFF) %s== 0) {" % (str(params[0] & 0xFF), inverseFlagInvertedChar))
	elif functionType == 48:
		display(file, "if (*(byte *)(PlayerPointer->unk0xD1) %s== %s) {" % (inverseFlagChar, str(params[0])))
	elif functionType == 49:
		display(file, "x31_ivar10_4 = id2index(&WORD_807F6240[%s])" % (str(params[0])))
		display(file, "if (ObjectModel2ArrayPointer[x31_ivar10_4]->behaviour_pointer[%s] %s== %s) {" % (hex(0x48 + params[2]), inverseFlagChar, str(params[1])))
	elif functionType == 50:
		display(file, "if (*(ushort *)PreviousMap %s== %s) {" % (inverseFlagChar, str(params[0])))
	elif functionType == 51:
		if params[0] == 0:
			if inverseFlag == 0:
				display(file, "if (%s < FUN_80614A54(PlayerPointer)) {" % (str(params[1])))
			else:
				display(file, "if (%s >= FUN_80614A54(PlayerPointer)) {" % (str(params[1])))
		elif params[0] == 1:
			if inverseFlag == 0:
				display(file, "if (%s >= FUN_80614A54(PlayerPointer)) {" % (str(params[1])))
			else:
				display(file, "if (%s < FUN_80614A54(PlayerPointer)) {" % (str(params[1])))
		else:
			display(file, "if (1 == 0) {")
	elif functionType == 52:
		display(file, "x34_uvar4 == FUN_806C8D2C(%s)" % (str(params[0])))
		if inverseFlag == 0:
			display(file, "if (%s <= &character_collectable_base[(BYTE_807FC929 * 0x5E) + (0x306 * x34_uvar4)] {" % (str(params[1])))
		else:
			display(file, "if (%s > &character_collectable_base[(BYTE_807FC929 * 0x5E) + (0x306 * x34_uvar4)] {" % (str(params[1])))
	elif functionType == 53:
		display(file, "if (*(byte *)PlayerPointer->0xD0 %s== %s) {" % (inverseFlagChar, str(params[0])))
	elif functionType == 54:
		display(file, "if (checkFlag(%s>%s,'Temporary') %s== 0) {" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), inverseFlagInvertedChar))
	elif functionType == 55:
		display(file, "FUN_80650D8C(this->id,%s,austack30,austack36)" % (str(params[0])))
		display(file, "if (austack30[0] %s== %s) {" % (inverseFlagChar, str(params[1])))
	elif functionType == 56:
		display(file, "if (%s(*(byte *)Character < 5)) {" % (inverseFlagChar))
	elif functionType == 57:
		display(file, "if ((%s& *(ushort *)PlayerPointer->CollisionQueue->TypeBitfield) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
	elif functionType == 58:
		display(file, "if (((1 << %s) & BYTE_807F693E) %s== 0) {" % (str(params[0]), inverseFlagInvertedChar))
	elif functionType == 59:
		display(file, "if (checkFlag(%s>%s,'Global') %s== 0) {" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), inverseFlagInvertedChar))
	elif functionType == 60:
		display(file, "if (PlayerPointer->chunk %s== %s) {" % (inverseFlagChar, str(params[0])))
	elif functionType == 61:
		display(file, "if (BYTE_807F6903 %s== 0) {" % (inverseFlagInvertedChar))
	else:
		display(file, "if ([%s,%s,%s,%s]) {" % (str(functionType), str(params[0]), str(params[1]), str(params[2])))

def grabExecution(param_1, ScriptCommand,params,behaviour,param_3,file):
	functionType = ScriptCommand
	if functionType == 0:
		display(file, "FUN_80642748(%s,%s,%s)" % (str(params[0]),str(params[1]),str(behaviour)))
	elif functionType == 1:
		display(file, "*(byte *)(behaviour + %s) = %s" % (hex(params[1] + 0x4B), str(params[0])))
	elif functionType == 2:
		display(file, "FUN_80723284(*(int*)(behaviour + 0x38),%s)" % (str(params[0])))
	elif functionType == 3:
		if params[0] == 0:
			display(file, "*(short *)(behaviour + %s) = %s" % (hex((params[2] * 2) + 0x44), str(params[1])))
		else:
			display(file, "*(short *)(behaviour + %s) = *(short *)(behaviour + %s)" % (hex((params[2] * 2) + 0x44), hex((params[1] * 4) + 0x14)))
	elif functionType == 4:
		display(file, "FUN_80723484(*(int *)(behaviour + 0x38))")
		display(file, "FUN_807238D4(*(int *)(behaviour + 0x38),0x807F621C,0x807F6220,0x807F6224)")
	elif functionType == 5:
		display(file, "FUN_806418E8(%s,%s,behaviour)" % (str(params[0]), str(params[1])))
	elif functionType == 6:
		display(file, "*(float *)(behaviour + %s) = %s" % (hex((params[0] * 4) + 0x14), str(params[1] / 10)))
	elif functionType == 7:
		display(file, "*(code *)(%s)(behaviour,this->id,%s,%s)" % (hex(0x80747E70 + (params[0] * 4)), str(params[1]), str(params[2])))
	elif functionType == 8:
		display(file, "FUN_80642844(%s,%s,behaviour)" % (str(params[0]), str(params[1])))
	elif functionType == 9:
		display(file, "if ((FLOAT_807F621C != FLOAT_807F61FC) || (FLOAT_807F6224 != 3433.54956055)) {")
		display(file, "FUN_80642480(%s)" % (str(params[0])))
		display(file, "}")
	elif functionType == 0xA:
		display(file, "*(byte *)(behaviour + 0x50) = %s" % (str(params[0])))
		display(file, "*(float *)(behaviour + 0x78) = %s" % (str(params[1] / 100)))
		display(file, "*(float *)(behaviour + 0x7C) = %s" % (str(params[2] / 100)))
	elif functionType == 0xB:
		display(file, "*(short *)(behaviour + 0x80) = %s" % (str(params[0])))
		display(file, "*(short *)(behaviour + 0x82) = %s" % (str(params[1])))
	elif functionType == 0xC:
		display(file, "*(short *)(behaviour + 0x84) = %s" % (str(params[0])))
		display(file, "*(short *)(behaviour + 0x86) = %s" % (str(params[1])))
	elif functionType == 0xD:
		display(file, "*(short *)(behaviour + 0x88) = %s" % (str(params[0])))
		display(file, "*(short *)(behaviour + 0x8A) = %s" % (str(params[1])))
	elif functionType == 0xE:
		display(file, "if (*(short *)(behaviour + %s) < 0) {" % (hex(((params[0] & 1) * 2) + 0x10)))
		display(file, "*(short *)(behaviour + %s) = FUN_80605044(this->id,%s,%s,%s)" % (hex(((params[0] & 1) * 2) + 0x10), str(params[0]), str(params[2] & 0x7F), str(params[1] & 2)))
		display(file, "}")
	elif functionType == 0xF:
		xF_ivar5 = params[1]
		if params[1] < 0:
			xF_ivar5 = xF_ivar5 + 0x7F
		xF_uvar9 = (xF_ivar5 >> 7) & 0xFF
		xF_bvar15 = xF_uvar9
		xF_ivar5 = params[2]
		if params[2] < 0:
			xF_ivar5 = xF_ivar5 + 0x7F
		xF_uvar14 = (xF_ivar5 >> 7) & 0xFF
		if xF_uvar9 == 0:
			xF_bvar15 = 0x7F
		if xF_uvar14 == 0:
			xF_uvar14 = 0xFF
		display(file, "FUN_806085DC(this->id,%s,%s,%s)" % (str(params[0]), str(xF_uvar14), str(xF_bvar15)))
	elif functionType == 0x10:
		display(file, "x10_temp = *(short *)(behaviour + %s)" % (hex((params[1] * 2) + 0x10)))
		display(file, "if (-1 < x10_temp) {")
		display(file, "FUN_80605380(x10_temp)")
		display(file, "*(short *)(behaviour + %s) = 0xFFFF" % (hex((params[1] * 2) + 0x10)))
		display(file, "}")
	elif functionType == 0x11:
		display(file, "FUN_806508B4(this->id,%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x12:
		display(file, "FUN_8065092C(this->id,%s)" % (str(params[0])))
	elif functionType == 0x13:
		display(file, "FUN_80650998(this->id,%s)" % (str(params[0])))
	elif functionType == 0x14:
		display(file, "FUN_80650A04(this->id,%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x15:
		display(file, "FUN_80650b50(this->id,%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x16:
		display(file, "FUN_80650BBC(this->id,%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x17:
		display(file, "FUN_80650C28(this->id,%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x18:
		display(file, "FUN_80650C98(this->id,%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x19:
		display(file, "setCharacterChangeParameters(%s,0,0)" % (str(params[0])))
	elif functionType == 0x1A:
		display(file, "FUN_80650AD8(this->id,%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2] / 100)))
	elif functionType == 0x1B:
		display(file, "if ((&WORD_807F6240)[%s] != -1) {" % (str(params[0])))
		display(file, "FUN_806335B0((&WORD_807F6240)[%s],1,%s)" % (str(params[0]), str(params[1])))
		display(file, "}")
	elif functionType == 0x1C:
		display(file, "if ((&WORD_807F6240)[id2index(%s)] != -1) {" % (str(params[0])))
		display(file, "x1C_ivar7 = (&WORD_807F6240)[%s]" % (str(params[0])))
		display(file, "if ((x1C_ivar7 != -1) && (ObjectModel2ArrayPointer[x1C_ivar7].behaviour != 0)) {")
		display(file, "x1C_puvar10 = ObjectModel2ArrayPointer[x1C_ivar7].behaviour + %s" % (str(params[1])))
		display(file, "x1C_puvar10[0x48] = x1C_puvar10[0x48] + %s" % str(params[2]))
		display(file, "}")
		display(file, "}")
	elif functionType == 0x1D:
		display(file, "FUN_80642844(%s,%s,behaviour)" % (str(params[0]), str(params[1])))
	elif functionType == 0x1E:
		display(file, "FUN_80642748(%s,%s,behaviour)" % (str(params[0]), str(params[1])))
	elif functionType == 0x1F:
		display(file, "FUN_807232EC(*(int *)(behaviour + 0x38),%s)" % (str(params[0])))
	elif functionType == 0x20:
		display(file, "FUN_80723380(*(int *)(behaviour + 0x38),%s)" % (str(params[0])))
	elif functionType == 0x21:
		display(file, "FUN_80723320(*(int *)(behaviour + 0x38),%s)" % (str(params[0])))
	elif functionType == 0x22:
		display(file, "*(int *)(behaviour + 0x38) = FUN_80723020(FLOAT_807F6220,FLOAT_807F6224,%s)" % (str(params[2])))
	elif functionType == 0x23:
		display(file, "FUN_80723428(*(int *)(behaviour + 0x38))")
		display(file, "*(int *)(behaviour + 0x38) = 0xFFFFFFFF")
	elif functionType == 0x24:
		display(file, "FUN_8072334C(*(int *)(behaviour + 0x38),%s)" % (str(params[0])))
	elif functionType == 0x25:
		display(file, "playCutsceneFromModelTwoScript(behaviour,%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
	elif functionType == 0x26:
		display(file, "FUN_8064199C(behaviour,%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x27:
		display(file, "FUN_80634EA4(this->id,%s,%s)" % (str(params[0]), str(params[1] & 0xFF)))
	elif functionType == 0x28:
		display(file, "FUN_80635018(this->id,%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
	elif functionType == 0x29:
		display(file, "FUN_8061EF4C(0x29,PlayerPointer->unk0x27C,%s,%s,FLOAT_807F621C)" % (str(params[0] & 0xFF), str(params[1])))
	elif functionType == 0x2A:
		display(file, "ObjectModel2ArrayPointer[id2Index(this->id)]->unk0x3C = %s" % (str(params[0])))
	elif functionType == 0x2B:
		display(file, "FUN_80636014(this->id,1)")
	elif functionType == 0x2C:
		display(file, "FUN_806335B0(this->id,1,%s") % (str(params[0]))
		display(file, "FUN_8067A9F0(0,PlayerPointer)")
	elif functionType == 0x2D:
		display(file, "x2d_counter = 0")
		display(file, "x2d_PTR_focusedLoadedActor = &PTR_DAT_807FB930")
		display(file, "if (loadedActorCount != 0) {")
		display(file, "do {")
		display(file, "x2d_ADDR_focusedLoadedActor = *x2d_PTR_focusedLoadedActor")
		display(file, "x2d_counter = x2d_counter + 1")
		display(file, "if ((*(uint *)(x2d_ADDR_focusedLoadedActor->object_properties_bitfield_1) & 0x2000) == 0) {")
		display(file, "if (x2d_ADDR_focusedLoadedActor->locked_to_pad == 0x1) {")
		display(file, "if (this->id == *(word *)(x2d_ADDR_focusedLoadedActor->unk0x10C)) {")
		if params[0] == 0:
			display(file, "*(ushort *)(x2d_ADDR_focusedLoadedActor->unk0x68) = *(ushort *)(x2d_ADDR_focusedLoadedActor->unk0x68) & 0xFFFB")
		else:
			display(file, "*(ushort *)(x2d_ADDR_focusedLoadedActor->unk0x68) = *(ushort *)(x2d_ADDR_focusedLoadedActor->unk0x68) | 4")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "x2d_PTR_focusedLoadedActor = x2d_PTR_focusedLoadedActor + 8")
		display(file, "x2d_finishedArray = x2d_counter < loadedActorCount")
		display(file, "} while(x2d_finishedArray)")
		display(file, "}")
	elif functionType == 0x2E:
		display(file, "FUN_80651BC0(%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x2F:
		display(file, "FUN_8060B49C(PlayerPointer,%s)" % (str(params[0])))
	elif functionType == 0x30:
		display(file, "InitMapChange(%s,0)" % (str(params[0])))
	elif functionType == 0x31:
		if (params[2] & 0x100) != 0:
			display(file, "SetIntroStoryPlaying(2)")
			display(file, "setNextTransitionType('Fade (Wrong Cutscene)')")
		if (params[2] & 0xFF) == 0:
			display(file, "InitMapChange_TransferredActor(%s,%s,0,0)" % (str(params[0]), str(params[1])))
		else:
			if (params[2] & 0xFF) == 1:
				display(file, "InitMapChange_TransferredActor(%s,%s,0,1)" % (str(params[0]), str(params[1])))
			elif (params[2] & 0xFF) == 2:
				display(file, "InitMapChange_TransferredActor(%s,%s,0,3)" % (str(params[0]), str(params[1])))
			else:
				display(file, "InitMapChange_TransferredActor(%s,%s,0,0)" % (str(params[0]), str(params[1])))
	elif functionType == 0x32:
		display(file, "InitMapChange_ParentMap(%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x33:
		display(file, "FUN_8062B86C(%s,(float)%s,(float)%s)" % (str(params[0]), str(params[1]), str(params[2] / 100)))
	elif functionType == 0x34:
		display(file, "FUN_8062B8A4(%s,(float)%s,(float)%s)" % (str(params[0]), str(params[1]), str(params[2] / 100)))
	elif functionType == 0x35:
		display(file, "FUN_80641C98(%s,%s,this->id)" % (str(params[0]), str(params[1])))
	elif functionType == 0x36:
		display(file, "FUN_80641BCC(%s,%s,this->id)" % (str(params[0]), str(params[1])))
	elif functionType == 0x37:
		display(file, "FUN_80679200(PlayerPointer,0,0x400000,%s)" % (str(params[0] & 0xFF)))
	elif functionType == 0x38:
		display(file, "FUN_80651be0(%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
	elif functionType == 0x39:
		display(file, "*(byte *)(behaviour + 0x4F) = %s" % (str(params[0])))
	elif functionType == 0x3A:
		display(file, "// Execution Type 0x3A stripped from final. Parameters: %s, %s, %s" % (str(params[0]), str(params[1]), str(params[2])))
	elif functionType == 0x3B:
		display(file, "*(uint *)(PlayerPointer->unk0x368) = *(uint *)(PlayerPointer->unk0x368) & ~%s" % (hex((params[0] * 0x10000) + params[1])))
	elif functionType == 0x3C:
		display(file, "if (*(int *)(behaviour + 0x94) != 0) {")
		display(file, "FUN_806782C0(*(int *)(behaviour + 0x94))")
		display(file, "*(int *)(behaviour + 0x94) = 0")
		display(file, "}")
	elif functionType == 0x3D:
		display(file, "*(byte *)(behaviour + 0x67) = %s" % (str(params[0])))
	elif functionType == 0x3E:
		display(file, "*(byte *)(behaviour + 0x6F) = %s" % (str(params[0])))
	elif functionType == 0x3F:
		display(file, "*(byte *)(behaviour + 0x6E) = %s" % (str(params[0])))
	elif functionType == 0x40:
		display(file, "*(int *)LevelStateBitfield = *(int *)LevelStateBitfield | %s" % (hex((params[0] * 0x10000) + params[1])))
	elif functionType == 0x41:
		display(file, "WORD_807F6904 = 1")
	elif functionType == 0x42:
		display(file, "FUN_80634CC8(this->id,%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
	elif functionType == 0x43:
		display(file, "if (%s == 1) {" % (str(params[0])))
		display(file, "*(int *)(behaviour + 0x8) = *(int *)(behaviour + %s)" % (hex((params[1] * 4) + 0x14)))
		display(file, "*(int *)(behaviour + 0xC) = *(int *)(behaviour + %s)" % (hex((params[2] * 4) + 0x14)))
		display(file, "}")
		display(file, "else {")
		display(file, "*(float *)(behaviour + 0x8) = %s" % (str(params[1] / 10)))
		display(file, "*(float *)(behaviour + 0xC) = %s" % (str(params[2] / 10)))
		display(file, "}")
	elif functionType == 0x44:
		display(file, "WORD_807F6906 = %s" % (str(params[0])))
		display(file, "WORD_807F6908 = %s" % (str(params[1])))
	elif functionType == 0x45:
		display(file, "*(byte *)(behaviour + 0x60) = %s" % (str(params[0])))
		display(file, "*(ushort *)(behaviour + 0x62) = %s" % (str(params[1])))
		display(file, "*(byte *)(behaviour + 0x66) = %s" % (str(params[2])))
	elif functionType == 0x46:
		display(file, "*(byte *)(behaviour + 0x70) = %s" % (str(params[0])))
	elif functionType == 0x47:
		display(file, "*(byte *)(behaviour + 0x71) = %s" % (str(params[0])))
	elif functionType == 0x48:
		display(file, "FUN_80604BE8(*(byte *)(behaviour + %s,%s,%s)" % (hex((params[0] * 2) + 0x11), str(params[1] / 100), str(params[2])))
	elif functionType == 0x49:
		display(file, "FUN_8067ABC0(%s,FLOAT_807F621C,FLOAT_807F6220,FLOAT_807F6224)" % (str(params[2])))
	elif functionType == 0x4A:
		display(file, "FUN_8063393C(this->id,1,%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x4B:
		display(file, "FUN_8072ED9C(this->id,%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x4C:
		display(file, "x4C_temp = FUN_80650A70()")
		display(file, "x4C_temp = (x4C_temp + %s)" % (hex(params[1])))
		display(file, "if (x4C_temp < 0) {")
		display(file, "x4C_temp = 0")
		display(file, "}")
		display(file, "FUN_80650A04(this->id,%s,x4C_temp)" % (str(params[0])))
	elif functionType == 0x4D:
		display(file, "x4D_svar12 = SpawnModelTwoObject(0,%s,FLOAT_807F690C,FLOAT_807F6910,FLOAT_807F6914)" % (str(params[0])))
		if params[1] == 0:
			display(file, "FUN_80641B00(x4D_svar12,this->id,%s)" % (str(params[2])))
		end
	elif functionType == 0x4E:
		display(file, "FUN_807146A4(%s)" % (str(params[0])))
		display(file, "FUN_807149B8(1)")
		display(file, "FUN_80714B84(0)")
	elif functionType == 0x4F:
		display(file, "if (BYTE_807F6938 != 0x10) {")
		if params[0] == -2:
			display(file, "(&WORD_807F6918)[BYTE_807F6938] = ObjectModel2ArrayPointer[id2index(this->id)]->id")
		else:
			display(file, "(&WORD_807F6918)[BYTE_807F6938] = %s" % (str(params[0])))
		display(file, "BYTE_807F6938 = BYTE_807F6938 + 1")
	elif functionType == 0x50:
		display(file, "if ((&WORD_807F6240)[%s] != -1) {" % (str(params[0])))
		display(file, "FUN_806335B0((&WORD_807F6240)[%s],1,%s)" % (str(params[0]), str(params[1])))
		display(file, "}")
	elif functionType == 0x51:
		display(file, "FUN_806F4F50(this->id,FLOAT_807F621C,FLOAT_807F6220,FLOAT_807F6224)")
	elif functionType == 0x52:
		display(file, "// Execution Type 0x52 stripped from final. Parameters: %s,%s,%s" % (str(params[0]), str(params[1]), str(params[2])))
	elif functionType == 0x53:
		display(file, "// Execution Type 0x53 stripped from final. Parameters: %s,%s,%s" % (str(params[0]), str(params[1]), str(params[2])))
	elif functionType == 0x54:
		display(file, "x54_ivar7 = id2index((&WORD_807F6240)[%s])" % (str(params[0])))
		display(file, "if (x54_ivar7 != -1) {")
		display(file, "FUN_8064199C(ObjectModel2ArrayPointer[x54_ivar7].behaviour,%s,%s)" % (str(params[1]), str(params[2])))
		display(file, "}")
	elif functionType == 0x55:
		display(file, "FUN_8062B630(%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x56:
		display(file, "FUN_80724994(1,%s,0,0)" % (str(params[0])))
	elif functionType == 0x57:
		display(file, "FUN_80659620(&uStack52,&uStack56,&uStack60,WORD_807F693A)")
		display(file, "FUN_80659670(%s + fStack32, %s + fStack56,extraout_a0,extraout_a1, %s + fStack60, WORD_807F693A)" % (str(params[0] / 1000), str(params[1] / 1000), str(params[0] / 1000)))
	elif functionType == 0x58:
		display(file, "x58_temp = FUN_805FFE50(%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
		display(file, "if (x58_temp == 0) {")
		display(file, "FUN_8063DB3C(%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
		display(file, "}")
	elif functionType == 0x59:
		display(file, "FUN_80724994(3,%s,%s,0)" % (str(params[0]), str(params[1])))
	elif functionType == 0x5A:
		display(file, "*(ushort *)(behaviour + 0x68) = %s" % (str(params[0])))
		display(file, "*(ushort *)(behaviour + 0x6A) = %s" % (str(params[1])))
		display(file, "*(ushort *)(behaviour + 0x6C) = %s" % (str(params[2])))
	elif functionType == 0x5B:
		display(file, "FUN_806C92C4(%s)" % (str(params[0])))
	elif functionType == 0x5C:
		display(file, "FUN_80724A9C(%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
	elif functionType == 0x5D:
		display(file, "setNextTransitionType(%s)" % (str(params[0])))
	elif functionType == 0x5E:
		display(file, "FUN_80641874()")
	elif functionType == 0x5F:
		display(file, "*(uint *)(PlayerPointer->ExtraInfo->unk0x1F0) = *(uint *)(PlayerPointer->ExtraInfo->unk0x1F0 | %s" % (hex((params[0] * 0x10000) + params[1])))
	elif functionType == 0x60:
		display(file, "FUN_8065F134()")
	elif functionType == 0x61:
		if params[2] == 0:
			display(file, "playSong('%s', 1)" % (getSongName(params[0])))
		else:
			display(file, "playSong('%s', %s)" % (getSongName(params[0]), str(params[2] / 255)))
	elif functionType == 0x62:
		display(file, "WORD_807F693A = %s" % (str(params[0])))
	elif functionType == 0x63:
		display(file, "FUN_8068B830()")
	elif functionType == 0x64:
		display(file, "FUN_8068B8FC()")
	elif functionType == 0x65:
		display(file, "*(byte *)(behaviour + %s) = (byte *)(behaviour + %s) + %s" % (hex(params[1] + 0x4B), hex(params[1] + 0x4B), str(params[0])))
	elif functionType == 0x66:
		display(file, "if (BYTE_807F61F8 == 0) {")
		display(file, "spawnActor(TimerController)")
		display(file, "temp = CurrentActorPointer")
		display(file, "WORD_807F61F4 = PTR_PTR_807FBB44")
		display(file, "CurrentActorPointer = mainmemory.read_u32_be(0x7FBB44)")
		display(file, "spawnTimer(0xDC,0x2A,%s)" % (str(params[0])))
		display(file, "BYTE_807F61F8 = 1")
		display(file, "WORD_807F61F0 = PTR_PTR_807FBB44")
		display(file, "CurrentActorPointer = temp")
		display(file, "}")
	elif functionType == 0x67:
		display(file, "if (BYTE_807F61F8 != 0) {")
		display(file, "FUN_806A2B08()")
		display(file, "}")
	elif functionType == 0x68:
		display(file, "if (BYTE_807F61F8 != 0) {")
		display(file, "FUN_806782C0(DWORD_807F61F0)")
		display(file, "FUN_806782C0(DWORD_807F61F4)")
		display(file, "}")
	elif functionType == 0x69:
		display(file, "FUN_80661398()")
	elif functionType == 0x6A:
		display(file, "FUN_806613E8(%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2] / 100)))
	elif functionType == 0x6B:
		display(file, "setFlag(%s>%s,%s,'Permanent')" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), getTOrF(params[1])))
	elif functionType == 0x6C:
		display(file, "FUN_80631B8C(%s)" % (str(params[0])))
	elif functionType == 0x6D:
		display(file, "FUN_8063A8C4(this->id,1,%s)" % (str(params[0] / 100)))
	elif functionType == 0x6E:
		display(file, "BYTE_807F693F = %s" % (str(params[0])))
	elif functionType == 0x6F:
		display(file, "?playMusic(%s,%s)" % (str(params[0]), str(params[1] & 0xFF)))
	elif functionType == 0x70:
		display(file, "FUN_80602C6C(%s,%s)" % (str(params[0]), str(params[1] / 255)))
	elif functionType == 0x71:
		display(file, "FUN_80602DC4()")
	elif functionType == 0x72:
		display(file, "getAndSetActorSpawnerControlStateFromActorSpawnerID(%s,%s,'%s')" % (str(params[0]), str(params[1] & 0xFF), getSetOrNot(1)))
	elif functionType == 0x73:
		display(file, "FUN_806EB178(0,%s,%s,%s)" % (str(params[0]), str(params[1]), str(params[2])))
	elif functionType == 0x74:
		display(file, "*(byte *)(behaviour + 0x9B) = *(byte *)(behaviour + 0x9B) | %s" % (hex(params[0])))
	elif functionType == 0x75:
		display(file, "changeTriggerActiveStateOfFirstInstanceOfType('%s',%s)" % (getTriggerTypeName(params[0]), str(params[1])))
	elif functionType == 0x76:
		display(file, "x76_counter = 0")
		display(file, "x76_focusedLoadedActorSlot = &loadedActorArray")
		display(file, "if (loadedActorCount != 0) {")
		display(file, "do {")
		display(file, "x76_focusedLoadedActor = *x76_focusedLoadedActorSlot")
		display(file, "if ((*(uint *)(x76_focusedLoadedActor->object_properties_bitfield) & 0x2000) == 0) {")
		display(file, "if (x76_focusedLoadedActor->locked_to_pad == 1) {")
		display(file, "if (this->id == *(short *)(x76_focusedLoadedActor->unk0x10c)) {")
		display(file, "FUN_80679200(x76_focusedLoadedActor,0,8,0)")
		display(file, "}")
		display(file, "}")
		display(file, "}")
		display(file, "x76_counter = x76_counter + 1")
		display(file, "x76_focusedLoadedActorSlot = x76_focusedLoadedActorSlot + 8")
		display(file, "} while (x76_counter < loadedActorCount)")
		display(file, "}")
	elif functionType == 0x77:
		display(file, "FUN_80650794(this->id,%s,%s,%s)" % (str(params[0]), str(params[1] & 0xFF), str(params[2] / 1000)))
	elif functionType == 0x78:
		display(file, "FUN_806335B0(this->id,1,%s)" % (str(params[0])))
		display(file, "PlayerPointer->unk0x3A4 = uStack40")
		display(file, "PlayerPointer->unk0x3A8 = uStack44")
		display(file, "PlayerPointer->unk0x3AC = uStack48")
	elif functionType == 0x79:
		display(file, "setFlag(%s>%s,%s,'Temporary')" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), getTOrF(params[1])))
	elif functionType == 0x7A:
		display(file, "FUN_80661264(%s,%s)" % (str(params[0] & 0xFF), str(params[0] & 0xFF)))
	elif functionType == 0x7B:
		display(file, "FUN_806335B0(this->id,%s)" % (str(params[1])))
		display(file, "FUN_8072ECFC(%s)" % (str(params[0])))
	elif functionType == 0x7C:
		display(file, "BYTE_80748094 = %s" % (str(params[0])))
	elif functionType == 0x7D:
		display(file, "if (*(short *)(behaviour + %s) < 0) {" % (hex((2 * params[1]) + 0x10)))
		display(file, "*(short *)(behaviour + %s) = FUN_80605044(this->id,%s,%s,%s)" % (hex((2 * params[1]) + 0x10), str(params[0]), str(params[2] & 0x7F), str(params[1] & 2)))
		display(file, "}")
	elif functionType == 0x7E:
		x7e_ivar5 = params[1]
		if params[1] < 0:
			x7e_ivar5 = x7e_ivar5 + 0x7F
		x7e_uvar9 = (x7e_ivar5 >> 7) & 0xFF
		x7e_ivar5 = params[2]
		if params[2] < 0:
			x7e_ivar5 = x7e_ivar5 + 0x7F
		x7e_uvar14 = (x7e_ivar5 >> 7) & 0xFF
		x7e_bvar15 = x7e_uvar14
		if x7e_uvar9 == 0:
			x7e_uvar9 = 0x7F
		if x7e_uvar14 == 0:
			x7e_bvar15 = 0xFF
		display(file, "if (BYTE_80748094 < 1) {")
		display(file, "playSFX(%s,0x7FFF,0x427C0000,%s)" % (str(params[0]), str(x7e_uvar9/127)))
		display(file, "}")
		display(file, "else {")
		display(file, "FUN_806335B0(this->id,1,BYTE_80748094)")
		display(file, "FUN_806086CC(%s,%s,%s,%s,0.3,0)" % (str(x7e_bvar15), str(x7e_uvar9), str(params[1] & 0x7F), str(params[2] & 0x7F)))
		display(file, "}")
	elif functionType == 0x7F:
		if params[1] == 0:
			x7f_temp = 0
		elif params[1] == 1:
			x7f_temp = 1
		elif params[1] == 2:
			x7f_temp = 2
		elif params[1] == 3:
			x7f_temp = 3
		else:
			x7f_temp = 0
		display(file, "FUN_8072EE0C(this->id,%s,%s)" % (str(params[0]),str(x7f_temp)))
	elif functionType == 0x80:
		display(file, "save()")
	elif functionType == 0x81:
		display(file, "BYTE_807F693E = BYTE_807F693E | (1 << %s)" % (str(params[0])))
	elif functionType == 0x82:
		display(file, "BYTE_807F693E = BYTE_807F693E & ~(1 << %s)" % (str(params[0])))
	elif functionType == 0x83:
		_item = "Unknown %s" % (hex(params[0]))
		if params[0] in hud_items:
			_item = hud_items[params[0]]
		display(file, "setHUDItemAsInfinite(%s,%s,%s)" % (_item, str(params[1]), getTOrF(params[2])))
	elif functionType == 0x84:
		display(file, "setFlag(%s>%s,%s,'Global')" % (hex(math.floor(params[0] / 8)), str(params[0] % 8), getTOrF(params[1])))
	elif functionType == 0x85:
		display(file, "FUN_8062D1A8()")
	elif functionType == 0x86:
		display(file, "FUN_806CF398(PlayerPointer)")
		display(file, "InitMapChange_TransferredActor(0x2A,0,%s,2)" % (str(params[0])))
	elif functionType == 0x87:
		display(file, "warpOutOfBonusGame()")
	elif functionType == 0x88:
		display(file, "DWORD_807FBB68 = DWORD_807FBB68 | %s" % (hex((params[0] * 0x10000) + params[1])))
	elif functionType == 0x89:
		display(file, "DWORD_807FBB68 = DWORD_807FBB68 & ~%s" % (hex((params[0] * 0x10000) + params[1])))
	elif functionType == 0x8A:
		display(file, "FUN_806417BC(%s,%s)" % (str(params[0]), str(params[1])))
	elif functionType == 0x8B:
		display(file, "*(uint *)(PlayerPointer->unk0x36C) = *(uint *)(PlayerPointer->unk0x36C) & ~%s" % (hex((params[0] * 0x10000) + params[1])))
	elif functionType == 0x8C:
		display(file, "*(uint *)(PlayerPointer->unk0x36C) = *(uint *)(PlayerPointer->unk0x36C) | %s" % (hex((params[0] * 0x10000) + params[1])))
	elif functionType == 0x8D:
		display(file, "next_transition_type = 'Fade'")
		display(file, "FUN_806CF398(PlayerPointer)")
		display(file, "x8d_uvar5 = getWorld(CurrentMap,0)")
		display(file, "x8d_ivar6 = isLobby(CurrentMap)")
		display(file, "x8d_ivar7 = x8d_uvar5")
		display(file, "if (x8d_ivar6 == 0) {")
		display(file, "warpOutOfLevel(x8d_ivar7)")
		display(file, "}")
		display(file, "else {")
		display(file, "x8d_svar12 = *(short *)(&DAT_8074809C + (x8d_ivar7 * 2))")
		display(file, "x8d_dstack88 = (short)(&WORD_807480AC)[x8d_ivar7]")
		display(file, "x8d_uvar9 = isFlagSet(*(short *)(&DAT_807480BC + (x8d_ivar7 * 2)),'Permanent')")
		display(file, "if ((x8d_uvar9 == 0) && (x8d_svar12 == 0x57)) {")
		display(file, "x8d_dstack88 = 0x15")
		display(file, "}")
		display(file, "x8d_ivar6 = DetermineLevel_NewLevel()")
		display(file, "if (x8d_ivar6 == 0) {")
		display(file, "InitMapChange(x8d_svar12,x8d_dstack88)")
		display(file, "}")
	elif functionType == 0x8E:
		display(file, "FUN_8066C904(&ObjectModel2ArrayPointer[id2index(this->id)]->unk0x28)")
	elif functionType == 0x8F:
		display(file, "FUN_806348B4(&ObjectModel2ArrayPointer[id2index(this->id)]->unk0x48)")
	elif functionType == 0x90:
		display(file, "BYTE_807F6902 = %s" % (str(params[0])))
	elif functionType == 0x91:
		display(file, "*(float *)(PlayerPointer->velocity) = %s" % (str(params[0])))
	elif functionType == 0x92:
		display(file, "*(uint *)(PlayerPointer->unk0x368) = *(uint *)(PlayerPointer->unk0x368) | 0x40000800")
	elif functionType == 0x93:
		display(file, "FUN_8061F510(%s,%s)" % (str(params[0] & 0xFF),str(params[1] & 0xFF)))
	elif functionType == 0x94:
		display(file, "FUN_80724994(2,%s,0,0)" % (str(params[0])))
	elif functionType == 0x95:
		display(file, "WORD_807F693C = 0x80")
	elif functionType == 0x96:
		display(file, "BYTE_807F6903 = %s" % (str(params[0])))
	else:
		display(file, "[%s,%s,%s,%s]" % (str(functionType),str(params[0]), str(params[1]), str(params[2])))


def readData(data,size,read_location):
	return bytereadToInt(data[read_location:read_location+size])

def grabScripts(data,file_path):
	global tab_indentation;
	global folder_removal;

	read_location = 0;
	script_count = readData(data,2,read_location);
	if script_count == 0:
		folder_removal.append(file_path)
	elif script_count > 0:
		complete_setup = [];
		with open (f"{file_path}/scripts.raw","wb") as fh:
			fh.write(data)
		with open (file_path + "/setup.bin","rb") as setupFile:
			with open(file_path + "/setup.json","w") as setupJson:
				setupFile.seek(0)
				modeltwo_count = bytereadToInt(setupFile.read(4))
				setup_read = 4;
				for item in range(modeltwo_count):
					setupFile.seek(setup_read + 0x2A)
					_id = bytereadToInt(setupFile.read(2))
					setupFile.seek(setup_read + 0x28)
					_type = bytereadToInt(setupFile.read(2))
					setupFile.seek(setup_read)
					_x = bytereadToInt(setupFile.read(4))
					setupFile.seek(setup_read + 4)
					_y = bytereadToInt(setupFile.read(4))
					setupFile.seek(setup_read + 8)
					_z = bytereadToInt(setupFile.read(4))
					complete_setup.append({
						"_id": _id,
						"_type": _type,
						"_x": _x,
						"_y": _y,
						"_z": _z
					})
					setup_read += 0x30
					setupJson.write(str(complete_setup))
		print(file_path + ": " + str(script_count))
		read_location += 2;
		if not os.path.exists(file_path):
			os.mkdir(file_path)
		for x in range(script_count):
			tab_indentation = 0;
			object_id = readData(data,2,read_location);
			object_type = 0;
			object_x = 0;
			object_y = 0;
			object_z = 0;
			for y in complete_setup:
				if y["_id"] == object_id:
					object_type = y["_type"]
					object_x = y["_x"]
					object_y = y["_y"]
					object_z = y["_z"]
			object_name = "Unknown " + hex(object_type)
			if object_type < (len(object_modeltwo_types) - 1):
				object_name = object_modeltwo_types[object_type];
			object_name = make_safe_filename(object_name).replace("?","")
			with open(file_path + "/" + object_name + "_" + str(hex(object_id)) + ".json","w") as jsonFile:
				jsonFile.write("{\n")
				jsonFile.write("\t\"_id\": " + hex(object_id) + ",\n")
				jsonFile.write("\t\"_type\": " + hex(object_type) + ",\n")
				jsonFile.write("\t\"coordinates\": {\n")
				jsonFile.write("\t\t\"x\": " + hex(object_x) + ",\n")
				jsonFile.write("\t\t\"x\": " + hex(object_y) + ",\n")
				jsonFile.write("\t\t\"x\": " + hex(object_z))
				jsonFile.write("\t}\n")
				jsonFile.write("\t}\n")


			with open(file_path + "/" + object_name + "_" + str(hex(object_id)) + ".txt","w") as scriptFile:
				block_count = readData(data,2,read_location + 2);
				behav_9C = readData(data,2,read_location + 4);
				read_location += 6;
				for y in range(block_count):
					tab_indentation = 0;
					conditional_count = readData(data,2,read_location);
					read_location += 2;
					x = {};
					if conditional_count > 0:
						for z in range(conditional_count):
							func = readData(data,2,read_location)
							read_location += 2;
							p = []
							for a in range(3):
								p.append(readData(data,2,read_location))
								read_location += 2;
							grabConditional(0, func,p,0,0,scriptFile)
					execution_count = readData(data,2,read_location);
					read_location += 2;
					if execution_count > 0:
						for z in range(execution_count):
							func = readData(data,2,read_location)
							read_location += 2;
							p = []
							for a in range(3):
								p.append(readData(data,2,read_location))
								read_location += 2;
							grabExecution(0, func,p,0,0,scriptFile)
					for z in range(tab_indentation):
						term_string = "}"
						for a in range(tab_indentation - z - 1):
							term_string = "\t" + term_string;
						scriptFile.write(term_string + "\n")
					#blocks.append(x)

# Cheeky Stuff stolen from Iso
def getFileInfo(absolute_address: int):
	if hex(absolute_address) in files:
		return files[hex(absolute_address)]

def getOriginalUncompressedSize(fh : BinaryIO, pointer_table_index : int, file_index : int):
	global pointer_tables

	ROMAddress = pointer_tables[26]["entries"][pointer_table_index]["absolute_address"] + file_index * 4

	# print("Reading size for file " + str(pointer_table_index) + "->" + str(file_index) + " from ROM address " + hex(ROMAddress))

	fh.seek(ROMAddress)
	return int.from_bytes(fh.read(4), "big")

def addFileToDatabase(absolute_address : int, data: bytes, uncompressed_size : int):
	global files
	global pointer_tables

	has_been_written_to_rom = False
	for x in pointer_tables:
		if x["absolute_address"] == absolute_address:
			has_been_written_to_rom = True
			#print("WARNING: POINTER TABLE " + str(x["index"]) + " BEING USED AS FILE!")
			break

	files[hex(absolute_address)] = {
		"new_absolute_address": absolute_address,
		"has_been_modified": False,
		"is_bigger_than_original": False,
		"has_been_written_to_rom": has_been_written_to_rom,
		"data": data,
		"uncompressed_size": uncompressed_size,
	}


def parsePointerTables(fh : BinaryIO):
	global pointer_tables
	global main_pointer_table_offset
	global maps
	global num_tables

	# Read pointer table addresses
	fh.seek(main_pointer_table_offset)
	i = 0
	while i < num_tables:
		absolute_address = int.from_bytes(fh.read(4), "big") + main_pointer_table_offset
		pointer_tables.append({
			"index": i,
			"absolute_address": absolute_address,
			"new_absolute_address": absolute_address,
			"num_entries": 0,
			"entries": [],
		})
		i += 1

	# Read pointer table lengths
	fh.seek(main_pointer_table_offset + num_tables * 4)
	for x in pointer_tables:
		x["num_entries"] = int.from_bytes(fh.read(4), "big")

	# Read pointer table entries
	for x in pointer_tables:
		if x["num_entries"] > 0:
			i = 0
			while i < x["num_entries"]:
				# Compute address and size information about the pointer
				fh.seek(x["absolute_address"] + i * 4)
				raw_int = int.from_bytes(fh.read(4), "big")
				absolute_address = (raw_int & 0x7FFFFFFF) + main_pointer_table_offset
				next_absolute_address = (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF) + main_pointer_table_offset
				x["entries"].append({
					"index": i,
					"absolute_address": absolute_address,
					"next_absolute_address": next_absolute_address,
					"bit_set": (raw_int & 0x80000000) > 0,
				})
				i += 1

	# Read data and original uncompressed size
	for x in pointer_tables:
		if x["index"] == script_table_index - (version == Version.kiosk) or x["index"] == setup_table_index - (version == Version.kiosk):
			for y in x["entries"]:
				absolute_size = y["next_absolute_address"] - y["absolute_address"]

				if absolute_size > 0:
					fh.seek(y["absolute_address"])
					data = fh.read(absolute_size)
					addFileToDatabase(y["absolute_address"], data, getOriginalUncompressedSize(fh, x["index"], y["index"]))

def make_safe_filename(s):
	def safe_char(c):
		if c.isalnum():
			return c
		else:
			return "_"
	return "".join(safe_char(c) for c in s).rstrip("_")

def extractMaps(src_file: str, dump_path: str):
	global maps

	for mapIndex, mapName in enumerate(maps):
		mapPath = f"{dump_path}/{mapIndex} - {make_safe_filename(mapName)}"
		os.mkdir(mapPath)
		extractMap(src_file, mapIndex, mapPath)

def extractMap(src_file: str, mapIndex : int, mapPath : str):
	global pointer_tables
	global files
	global num_tables
	global relevant_pointer_tables
	global folder_removal

	setup_tbl = setup_table_index - (version == Version.kiosk)
	script_tbl = script_table_index - (version == Version.kiosk)

	tbls = [setup_tbl,script_tbl]
	sizes = [0,0]
	
	idx = 0
	with open(src_file,"rb") as fl:
		for tbl in tbls:
			fl.seek(main_pointer_table_offset + (num_tables * 4) + (4 * tbl))
			tbl_size = int.from_bytes(fl.read(4),"big")
			if tbl_size > mapIndex:
				fl.seek(main_pointer_table_offset + (4 * tbl))
				tbl_ptr = main_pointer_table_offset + int.from_bytes(fl.read(4),"big")
				fl.seek(tbl_ptr + (4 * mapIndex))
				entry_start = main_pointer_table_offset + (int.from_bytes(fl.read(4),"big") & 0x7FFFFFFF)
				entry_finish = main_pointer_table_offset + (int.from_bytes(fl.read(4),"big") & 0x7FFFFFFF)
				entry_size = entry_finish - entry_start
				sizes[idx] = entry_size
				if entry_size > 0:
					fl.seek(entry_start)
					compress = fl.read(entry_size)
					temp_bin = "temp.bin"
					with open(temp_bin,"wb") as fh:
						fh.write(compress)
					if int.from_bytes(compress[0:1],"big") == 0x1F and int.from_bytes(compress[1:2],"big") == 0x8B:
						data = zlib.decompress(compress, 15+32)
					else:
						data = compress
					if idx == 0:
						# Setup
						built_setup = mapPath + "/setup.bin"
						with open(built_setup, "wb") as fh:
							fh.write(data)
					elif idx == 1:
						# Scripts
						built_script = mapPath + "/scripts.bin"
						with open(built_script, "wb") as fh:
							fh.write(data)
						grabScripts(data,mapPath)
					if os.path.exists(temp_bin):
						os.remove(temp_bin)
			idx += 1
	if sizes[0] + sizes[1] == 0:
		folder_removal.append(mapPath)

def bytereadToInt(read):
	total = 0
	for x in list(read):
		total = (total * 256) + x
	return total

def extractScripts():
	global folder_removal
	global main_pointer_table_offset
	global version

	file_path = getFilePath()
	main_pointer_table_offset, version, dump_path, valid = getROMData(file_path, "instance scripts")
	if valid:
		extractMaps(file_path, dump_path)
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

extractScripts()