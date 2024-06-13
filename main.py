from builtins import list, max, range
from Util import FarmWhat, Loop


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
			
		fullSizeXFullSize[row].append([])
			

crops = [
	[Items.Hay, Entities.Grass, None, Grounds.Turf, oneXOne, []],
	[Items.Carrot, Entities.Carrots, Items.Carrot_Seed, Grounds.Soil, oneXOne, []],
	[Items.Wood, Entities.Tree, None, Grounds.Soil, oneXOne, []],
	[Items.Pumpkin, Entities.Pumpkin, Items.Pumpkin_Seed, Grounds.Soil, fullSizeXFullSize, []]
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
		crop.pop(5)
		temp = []
		for row in crop[4]:
			temp.append(list(row))
		crop.append(temp)


def Orchestra(crop):
	isRunning = True
	
	while isRunning == True:	
		Plant(crop)

		if Check(crop):
			harvest()
			isRunning = False


def Check(crop):
	def Action():
		crop[5][get_pos_y()][get_pos_x()] = can_harvest()
		
		if not can_harvest():
			return False


	if (Loop(crop[5], Action) == False):
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
		
		if crop[1] == Entities.Pumpkin:
			while get_water() <= 0.75 and (not can_harvest()):
				use_item(Items.Water_Tank)
		else:
			while can_harvest() == False and get_entity_type() != None:
				if num_items(Items.Fertilizer) <= 0:
					trade(Items.Fertilizer)
					
				use_item(Items.Fertilizer)
	
	Loop(crop[5], Move)


Main()