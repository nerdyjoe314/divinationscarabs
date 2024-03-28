import json
import subprocess
import os
import time
from cleanUpPrices import prepare_card_data

DEFAULT_WEIGHT = 4987
PRICE_FLOOR = 6
CLICK_THRESHOLD = 10

prepare_card_data(DEFAULT_WEIGHT, PRICE_FLOOR)

start_time = time.time()
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

with open("prices.json", 'r') as f:
	data = json.load(f)
# print(len(data))

t_name_array = []
t_price_array = []
t_weight_array = []
t_stack_array = []
t_map_label =[[0 for _ in range(len(data))] for _ in range(len(maps))]

# print(data[0])

for i in range(len(data)):
	t_name_array.append(data[i]['name'])
	t_price_array.append(data[i]['price'])
	t_stack_array.append(data[i]['stack'])
	try:
		t_weight_array.append(data[i]['weight'])
	except KeyError:
		t_weight_array.append(0)
	try:
		areas = data[i]['drop']['areas']
		for map_id in range(len(maps)):
			if "MapWorlds"+maps[map_id] in areas:
				t_map_label[map_id][i] = 1
	except KeyError:
		pass


# print(len(t_name_array))
# print(len(t_price_array))
# print(len(t_weight_array))
# print(len(t_stack_array))

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
	ev = 0
	if t_price_array[card_id] >= CLICK_THRESHOLD:
		ev += t_price_array[card_id] * t_weight_array[card_id] * 0.8 
	if t_stack_array[card_id] * t_price_array[card_id] >= CLICK_THRESHOLD:
		ev += t_stack_array[card_id] * t_price_array[card_id] * t_weight_array[card_id] * 0.2 
	objective_string += str(ev) + " c"+str(card_id)+" + "
out.write(objective_string+'0\n')
out.write("Subject To\n")

# constraint, only 12 maps allowed
map_count_string = "map_count: "
for map_index in range(len(maps)):
	map_count_string += "m"+str(map_index)+" + "
out.write(map_count_string[:-3]+" <= 12\n")

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

# remove old DivCard.out if it exists
if os.path.exists("DivCard.out"):
    os.remove("DivCard.out")

# run the integer program
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
subprocess.run(["scip","-f","DivCard.lp","-q","-l","DivCard.out"])

# open and read the outfile into memory
logfile=open("DivCard.out","r")
lines = logfile.readlines()

# parse the output
findtext = "primal solution (original space):"
for i in range(len(lines)):
	if findtext in lines[i]:
		break

startline=i

findtext = "Statistics"
for i in range(len(lines)):
	if findtext in lines[i]:
		break

endline = i

for i in range(startline+1,endline):
	if 'm' in lines[i]:
		print(maps[int(lines[i][1:4])])

print(time.time()-start_time)
