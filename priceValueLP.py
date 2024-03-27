def offset(n: int, offsets):
	out = n
	for i in offsets:
		if n>i:
			out+=1
	return out

maps = [
  "ForbiddenWoods",
  "ColdRiver",
  "FrozenCabins",
  "Iceberg",
  "Scriptorium",
  "Museum",
  "Academy",
  "DrySea",
  "Dunes",
  "DesertSpring",
  "MineralPools",
  "CrystalOre",
  "TortureChamber",
  "Grotto",
  "Wharf",
  "FloodedMine",
  "Waterways",
  "Vault",
  "Peninsula",
  "Geode",
  "AshenWood",
  "SpiderForest",
  "Lair",
  "Thicket",
  "TropicalIsland",
  "Stagnation",
  "JungleValley",
  "BrambleValley",
  "SunkenCity",
  "VaalPyramid",
  "Alleyways",
  "Arcade",
  "Port",
  "MoonTemple",
  "Factory",
  "Excavation",
  "Orchard",
  "Plaza",
  "Conservatory",
  "Temple",
  "Cemetery",
  "GraveTrough",
  "Graveyard",
  "LavaChamber",
  "BoneCrypt",
  "Bog",
  "Marshes",
  "Basilica",
  "Residence",
  "Arsenal",
  "Promenade",
  "OvergrownShrine",
  "Courtyard",
  "Terrace",
  "Gardens",
  "Strand",
  "Shore",
  "LavaLake",
  "Estuary",
  "Volcano",
  "Foundry",
  "UndergroundSea",
  "CursedCrypt",
  "Necropolis",
  "AcidLakes",
  "ArachnidNest",
  "ArachnidTomb",
  "AridLake",
  "Armoury",
  "Atoll",
  "Barrows",
  "Beach",
  "Belfry",
  "BurialChambers",
  "Cage",
  "Canyon",
  "CastleRuins",
  "Cells",
  "Channel",
  "CitySquare",
  "CoralRuins",
  "Courthouse",
  "CrimsonTemple",
  "CrimsonTownship",
  "DefiledCathedral",
  "Dungeon",
  "Fields",
  "ForkingRiver",
  "Springs",
  "HauntedMansion",
  "Leyline",
  "Lighthouse",
  "Lookout",
  "Malformation",
  "Mausoleum",
  "Maze",
  "Palace",
  "Park",
  "Pen",
  "Phantasmagoria",
  "Pier",
  "Pit",
  "Plateau",
  "PrimordialPool",
  "Reef",
  "Shipyard",
  "Shrine",
  "Siege",
  "Silo",
  "SulphurVents",
  "Tower",
  "ToxicSewer",
  "UndergroundRiver",
  "VaalTemple",
  "Villa",
  "WastePool",
  "Wasteland",
]

removes =[
  "The Easy Stroll",
  "The Lunaris Priestess",
  "The Explorer",
  "The Mountain",
  "Boundless Realms",
  "Azure Rage",
  "Left to Fate",
  "Might is Right",
  "Scholar of the Seas",
  "Grave Knowledge",
  "The Wolverine",
  "Blind Venture",
  "Hunter's Resolve",
  "Alivia's Grace",
  "The Admirer",
  "The Surgeon",
  "The Wolf's Shadow",
  "Shard of Fate",
  "Jack in the Box",
  "Last Hope",
  "Mitts",
  "The Battle Born",
  "The Sun",
  "The Demoness",
  "The Sigil",
  "The Twins",
  "The Inoculated",
  "The Army of Blood",
  "The Visionary",
  "The Gladiator",
  "Gemcutter's Promise",
  "The Web",
  "The Sword King's Salute",
  "Boon of Justice",
  "The Penitent",
  "The Warden",
  "The Cache",
  "Lysah's Respite",
  "The Fathomless Depths",
  "The Harvester",
  "The Fox",
  "Volatile Power",
  "The Endurance",
  "The Wolf",
  "Time-Lost Relic",
  "The Rite of Elements",
  "Gift of the Gemling Queen",
  "The Standoff",
  "Prosperity",
  "Heterochromia",
  "The Insatiable",
  "The Incantation",
  "The Betrayal",
  "The Pack Leader",
  "The Oath",
  "Vile Power",
  "The Surveyor",
  "Thunderous Skies",
  "The Tower",
  "The Stormcaller",
  "The Opulent",
  "The Blazing Fire",
  "The Journalist",
  "The Jeweller's Boon",
  "The Survivalist",
  "Glimmer of Hope",
  "Destined to Crumble",
  "The Scholar",
  "Thirst for Knowledge",
  "Rain of Chaos",
  "Emperor's Luck",
  "Loyalty",
  "A Sea of Blue",
  "The Lover",
  "The King's Blade",
  "The Catalyst",
  "Lantador's Lost Love",
  "The Scarred Meadow",
  "Rats",
  "The Witch",
  "Three Voices",
]




f = open("prices.txt", 'r')
split= f.readlines()
f.close()
offsets = [30,31]
name_array = []
price_array = []
weight_array = []
stack_array = []
old_row_id = 0
map_label = [[0 for _ in range(428)] for _ in range(len(maps))]
for row_id in range(len(split)):
	for map_id in range(len(maps)):
		if "MapWorlds"+maps[map_id] in split[row_id]:
			map_label[map_id][old_row_id] = 1
	if "name: " in split[row_id]:
		name_array.append(split[row_id][11:-3])
		old_row_id+=1
	if "price:" in split[row_id]:
		price_array.append(float(split[row_id][10:-2]))
	if "weight: " in split[row_id]:
		weight_array.append(int(split[row_id][12:-2]))
	if "stack: " in split[row_id]:
		stack_array.append(int(split[row_id][10:-2]))

t_name_array = []
t_price_array = []
t_weight_array = []
t_stack_array = []
for card_id in range(len(name_array)):
	if name_array[card_id] not in removes:
		t_name_array.append(name_array[card_id])
		t_price_array.append(price_array[card_id])
		t_weight_array.append(weight_array[card_id])
		t_stack_array.append(stack_array[card_id])

t_map_label = [[0 for _ in range(428)] for _ in range(len(maps))]
for map_id in range(len(maps)):
	card_index=0
	for card_id in range(len(name_array)):
		if name_array[card_id] not in removes:
			t_map_label[map_id][card_index] = map_label[map_id][card_id]
			card_index+=1

print(len(t_name_array))
print(len(t_price_array))
print(len(t_weight_array))
print(len(t_stack_array))

#variables are cards and maps
# optimization is ev of cards dot cards
# constraints are:
# maps total <= 12
# for each card:
# card <= sum of maps
# rephrased:
# card - sum of maps <= 0

out = open("DivCard.lp", 'w')

# objective function, maximize value of included cards
out.write("Maximize\n")
objective_string=" obj: "
for card_id in range(len(t_name_array)):
	ev = t_price_array[card_id] * t_weight_array[card_id] * 0.8 + t_stack_array[card_id] * t_price_array[card_id] * t_weight_array[card_id] * 0.2 
	objective_string += str(ev) + " c"+str(card_id)+" + "
out.write(objective_string+'0\n')
out.write("Subject To\n")

# constraint, only 12 maps allowed
map_count_string = "map_count: "
for map_index in range(len(maps)):
	map_count_string += "m"+str(map_index)+" + "
out.write(map_count_string+"0 <= 12\n")

# constraint, for each card, it's inclusion has to be less than or equal to the sum of the maps it's in
for card_id in range(len(t_name_array)):
	card_inclusion_string = "inc"+str(card_id)+": - c"+str(card_id)
	for map_index in range(len(maps)):
		if t_map_label[map_index][card_id] == 1:
			card_inclusion_string += " + m"+str(map_index)
	out.write(card_inclusion_string+" >= 0\n")
		
# make all parameters binary and close
out.write("Binary\n")
for card_id in range(len(t_name_array)):
	out.write("c"+str(card_id)+"\n")
for map_id in range(len(maps)):
	out.write("m"+str(map_id)+"\n")
out.write("End\n")
out.close()

out = open("cardkey.txt", 'w')
for n in range(len(t_name_array)):
	out.write(str(n)+", ")
	out.write(t_name_array[n])
	out.write(", "+str(t_price_array[n]))
	out.write(", "+str(t_weight_array[n]))
	out.write(", "+str(t_stack_array[n]))
	out.write('\n')

out.write('\n')
for map_id in range(len(maps)):
	ev =0
	stack_ev =0 
	for card_id in range(len(t_name_array)):
		if t_map_label[map_id][card_id] == 1:
			ev += t_price_array[card_id] * t_weight_array[card_id]
			stack_ev += t_price_array[card_id] * t_weight_array[card_id] * 0.8 + t_stack_array[card_id] * t_price_array[card_id] * t_weight_array[card_id] * 0.2 
	out.write(str(map_id)+", "+maps[map_id]+", "+str(ev)+", "+str(stack_ev)+"\n")
out.close()
