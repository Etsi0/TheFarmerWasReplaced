from builtins import abs, len, range
from main import crops


def FarmWhat():
	def SetArray(array, obj):
		array[0] = obj
		array[1] = num_items(obj[0])
		
		return array
	
	smallestCrop = [[], -1]

	for crop in crops:
		if smallestCrop[1] > num_items(crop[0]):
			SetArray(smallestCrop, crop)
		elif smallestCrop[1] == -1:
			SetArray(smallestCrop, crop)

	return smallestCrop[0]


def Loop(emptyCropSpots, action):
	isAnyFalse = False
	for row in range(len(emptyCropSpots)):
		for col in range(len(emptyCropSpots[row])):
			if emptyCropSpots[row][col] == None or emptyCropSpots[row][col] == True:
				continue

			moves = Move([get_pos_x(), get_pos_y()], [col, row])
			for i in range(2):
				for j in range(moves[0][i]):
					move(moves[1][i])
			
			if action() == False:
				isAnyFalse = True
	
	if isAnyFalse == True:
			return False


def Move(startPos, endPos):
	delta_x = endPos[0] - startPos[0]
	wrap_around_x = get_world_size() - abs(delta_x)
	
	if abs(delta_x) <= wrap_around_x:
		shortest_x = delta_x
	elif delta_x > 0:
		shortest_x = -wrap_around_x
	else:
		shortest_x = wrap_around_x
    
	delta_y = endPos[1] - startPos[1]
	wrap_around_y = get_world_size() - abs(delta_y)
	
	if abs(delta_y) <= wrap_around_y:
		shortest_y = delta_y
	elif delta_y > 0:
		shortest_y = -wrap_around_y
	else:
		shortest_y = wrap_around_y

	directions = []
	if shortest_x >= 0:
		directions.append(East)
	elif shortest_x < 0:
		directions.append(West)

	if shortest_y >= 0:
		directions.append(North)
	elif shortest_y < 0:
		directions.append(South)

	return [abs(shortest_x), abs(shortest_y)], directions