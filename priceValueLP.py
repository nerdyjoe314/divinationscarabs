import json
import subprocess
import os
import time
from cleanUpPrices import prepare_card_data

DEFAULT_WEIGHT = 0
PRICE_FLOOR = 4
CLICK_THRESHOLD = 4
BENCHMARK_CARD = "The Union"
BENCHMARK_DROPPED = 144
FAVORITE_MAPS = 12
USE_FULL_STACK = True
#USE_FULL_STACK = False

prepare_card_data(DEFAULT_WEIGHT, PRICE_FLOOR)


start_time = time.time()
maps = [
 "BoneCrypt",
"CrimsonTownship",
"Shipyard",
"DesertSpring",
"Dunes",
"Iceberg",
"Pier",
"Arsenal",
"Belfry",
"Arcade",
"Wharf",
"Lair",
"OvergrownShrine",
"Strand",
"Volcano",
"CrystalOre",
"ToxicSewer",
"Mausoleum",
"Springs",  # "FungalHollow",
"Channel",
"Cemetery",
"MoonTemple",
"VaalPyramid",
"Canyon",
"Fields",
"Foundry",
"PrimordialPool",
"Cells",
"Atoll",
"Courtyard",
"Graveyard",
"Gardens",
"Siege",
"BurialChambers",
"Cage",
"Phantasmagoria",
"Shore",
"Promenade",
"DrySea",
"AridLake",
"Waterways",
"Tower",
"Basilica",
"CursedCrypt",
"WastePool",
"Silo",
"SpiderForest",
"Courthouse",
"Dungeon",
"BrambleValley",
"Orchard",
"JungleValley",
"LavaLake",
"SunkenCity",
"Reef",
"FrozenCabins",
"AshenWood",
"Park",
"Lookout",
"TropicalIsland",
"Stagnation",
"Academy",
"Gorge",  # "Glacier",
"UndergroundSea",
"Pit",
"Wasteland",
"Excavation",
"ArachnidNest",
"Grotto",
"AcidLakes",  # "AcidCaverns",
"Plaza",
"Residence",
"SulphurVents",
"ForkingRiver",
"Conservatory",
"Museum",
"Necropolis",
"Barrows",
"Bog",
"CrimsonTemple",
"Palace",
"FloodedMine",
"MineralPools",
"Terrace",
"GraveTrough",
"Shrine",
"Temple",
"Maze",
"ForbiddenWoods",
"Estuary",
"DefiledCathedral",
"UndergroundRiver",
"ColdRiver_",
"Arena",
"Port",
"Vault",
"Plateau",
"LavaChamber",
"CastleRuins",
"Thicket",
]

with open("prices.json", 'r') as f:
	data = json.load(f)
# print(len(data))

with open("realWeights.json",'r') as f:
	weights = json.load(f)

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
	#try:
	#	t_weight_array.append(data[i]['weight'])
	#except KeyError:
	#	t_weight_array.append(0)
	try:
		areas = data[i]['drop']['areas']
		for map_id in range(len(maps)):
			if "MapWorlds"+maps[map_id] in areas:
				t_map_label[map_id][i] = 1
	except KeyError:
		pass

for i in range(len(data)):
	t_weight_array.append(weights[0][t_name_array[i]])


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
	if USE_FULL_STACK:
		if t_price_array[card_id] >= CLICK_THRESHOLD:
			ev += t_price_array[card_id] * t_weight_array[card_id] * 0.8
		if t_stack_array[card_id] * t_price_array[card_id] >= CLICK_THRESHOLD:
			ev += t_stack_array[card_id] * t_price_array[card_id] * t_weight_array[card_id] * 0.2
	else:
		if t_price_array[card_id] >= CLICK_THRESHOLD:
			ev += t_price_array[card_id] * t_weight_array[card_id]
	objective_string += str(ev) + " c"+str(card_id)+" + "
out.write(objective_string+'0\n')
out.write("Subject To\n")

# constraint, only 12 maps allowed
map_count_string = "map_count: "
for map_index in range(len(maps)):
	map_count_string += "m"+str(map_index)+" + "
out.write(map_count_string[:-3]+" <= " + str(FAVORITE_MAPS) + "\n")

# constraint, for each card, it's inclusion has to be less than or equal to the sum of the maps it's in
for card_id in range(len(t_name_array)):
	card_inclusion_string = "inc"+str(card_id)+": - c"+str(card_id)
	for map_index in range(len(maps)):
		if t_map_label[map_index][card_id] == 1:
			card_inclusion_string += " + m"+str(map_index)
	out.write(card_inclusion_string+" >= 0\n")

# evaluate how much "droppage" is obtained by the benchmark
index_card_id = t_name_array.index(BENCHMARK_CARD)
card_count_constant = BENCHMARK_DROPPED/float(t_weight_array[index_card_id])

# constraint, total stacks of cards generated has to be carried out in 6 portals
# 6 portals of 60 slots is 360 stacks total
feel_the_weight_string = "six_portals: "
for card_id in range(len(t_name_array)):
	number_of_stacks = int(card_count_constant*t_weight_array[card_id]/t_stack_array[card_id])+1
	feel_the_weight_string += str(number_of_stacks) + " c"+str(card_id) + " + "
out.write(feel_the_weight_string[:-3] + " <= 390\n")
		
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

used_map_ids = []
used_card_ids = []

for i in range(startline+1,endline):
	if 'c' == lines[i][0]:
		used_card_ids.append(int(lines[i][1:4]))
	if 'm' in lines[i]:
		print(maps[int(lines[i][1:4])])
		used_map_ids.append(int(lines[i][1:4]))
	if 'objective value' in lines[i]:
		print("value = ",lines[i][-13:-1])

#print(used_card_ids)
#print(used_map_ids)
total_stacks = 0
for card_id in used_card_ids:
	total_stacks += int(card_count_constant*t_weight_array[card_id]/t_stack_array[card_id])+1
print("Used", str(total_stacks), "total stacks out of 360")

print("time: ",time.time()-start_time)
