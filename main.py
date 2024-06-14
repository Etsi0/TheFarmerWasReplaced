from builtins import list, max, range
from Util import FarmWhat, Loop, Move


clear()

oneXOne = []
fullSizeXFullSize = []

for row in range(get_world_size()):
	if row == 0:
		oneXOne.append([])

	fullSizeXFullSize.append([])

	for col in range(get_world_size()):
		if row == 0 and col == 0:
			oneXOne[row].append([False])

		fullSizeXFullSize[row].append([False])


crops = [
	[
		Items.Hay,
		Entities.Grass,
		None,
		Grounds.Turf,
		oneXOne,
		None,
		[],
		None
	],
	[
		Items.Carrot,
		Entities.Carrots,
		Items.Carrot_Seed,
		Grounds.Soil,
		oneXOne,
		None,
		[],
		None
	],
	[
		Items.Wood,
		Entities.Tree,
		None,
		Grounds.Soil,
		oneXOne,
		None,
		[],
		None
	],
	[
		Items.Pumpkin,
		Entities.Pumpkin,
		Items.Pumpkin_Seed,
		Grounds.Soil,
		fullSizeXFullSize,
		None,
		[],
		None
	],
	[
		Items.Power,
		Entities.Sunflower,
		Items.Sunflower_Seed,
		Grounds.Soil,
		fullSizeXFullSize,
		[
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[],
			[]
		],
		[],
		[],
	]
]

isRunning = False


def Main():
	while isRunning == False:
			trade(Items.Empty_Tank, max(get_world_size() ** 2 / 0.25 - num_items(Items.Empty_Tank) - num_items(Items.Water_Tank), 0))

			ResetCropArrays()
			crop = FarmWhat()

			Orchestra(crop)


def ResetCropArrays():
	for crop in crops:
		for i in range(2):
			crop.pop(6)

		plantArea = []
		for row in crop[4]:
			plantArea.append(list(row))
		crop.append(plantArea)

		if not crop[5] == None:
			powerArea = []
			for row in crop[5]:
				powerArea.append(list(row))
			crop.append(powerArea)
		else:
			crop.append(None)


def Orchestra(crop):
	isRunning = True
	
	while isRunning == True:	
		Plant(crop)

		if Check(crop):
			if crop[7] == None:
				harvest()
			else:
				for i in range(15):
					for j in range(len(crop[7][i])):
						moves = Move([get_pos_x(), get_pos_y()], [crop[7][i][j][0], crop[7][i][j][1]])
						for k in range(2):
							for l in range(moves[0][k]):
								move(moves[1][k])
						if get_entity_type() == None:
							break
						harvest()

			isRunning = False


def Check(crop):
	def Action():
		crop[6][get_pos_y()][get_pos_x()] = can_harvest()

		if (not crop[7] == None) and (not measure() == None):
			crop[7][15 - measure()].append([get_pos_x(), get_pos_y()])
		
		if not can_harvest():
			return False


	if (Loop(crop[6], Action) == False):
		return False

	return True


def Plant(crop):
	def Move():
		Action(crop)

	def Action(crop):
		if (crop[3] == Grounds.Soil and get_ground_type() == Grounds.Turf) or (crop[3] == Grounds.Turf and get_ground_type() == Grounds.Soil):
			till()

		if crop[2] != None and num_items(crop[2]) <= 0:
			trade(crop[2])

		if not get_entity_type():
			plant(crop[1])

		if crop[4] == fullSizeXFullSize:
			while get_water() <= 0.75 and (not can_harvest()):
				use_item(Items.Water_Tank)
		else:
			while can_harvest() == False and get_entity_type() != None:
				if num_items(Items.Fertilizer) <= 0:
					trade(Items.Fertilizer)
					
				use_item(Items.Fertilizer)
	
	Loop(crop[6], Move)


Main()