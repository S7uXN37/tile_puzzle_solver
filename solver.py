from time import sleep
import sys

# possibilities:
# woman w/ can:  front bottom, front top		-	fb, ft
# woman from behind:  behind bottom, behind top	-	bb, bt
# cake: cake left, cake right
# 	(both clockWise and Counterclockwise up)	-	clw, clc, crw, crc
# watering can: can handle, can tip
# 	(both clockWise and Counterclockwise up)	-	whw, whc, wtw, wtc

def doImagesFit(i1, i2):
	if len(i1) == len(i2) == 2:
		return i1[0] == i2[0] and not i1[1] == i2[1]
	elif len(i1) == len(i2) == 3:
		return i1[0] == i2[0] and not i1[1] == i2[1] and not i1[2] == i2[2]
	else:
		return False

ORDER = "NESW"
tiles = {
	1: {'N':'fb',	'E':'wtc',	'S':'bt',	'W':'crw'},
	2: {'N':'fb',	'E':'whc',	'S':'bt',	'W':'crw'},
	3: {'N':'bb',	'E':'clc',	'S':'ft',	'W':'whw'},
	4: {'N':'clc',	'E':'bt',	'S':'ft',	'W':'whw'},
	5: {'N':'crw',	'E':'fb',	'S':'bt',	'W':'whw'},
	6: {'N':'clc',	'E':'bt',	'S':'whw',	'W':'fb'},
	7: {'N':'ft',	'E':'bt',	'S':'crw',	'W':'wtc'},
	8: {'N':'wtc',	'E':'ft',	'S':'crw',	'W':'bb'},
	9: {'N':'bb',	'E':'wtc',	'S':'crw',	'W':'ft'}
}

def getImage(tile, rot, side, allow_error=True):
	if not allow_error and tile == -1:
		return "???"
	orig_side = ORDER[(ORDER.index(side) + rot) % 4]
	return tiles[tile][orig_side]

def check(map):
	wrong_tiles = [] # indexed as in map
	# rows
	for row in range(3):
		for gap in range(2):
			left, l_rot = map[row*3 + gap]
			right, r_rot = map[row*3 + gap + 1]
			if left == -1 or right == -1:
				# not yet set, ignore gap
				continue
			if not doImagesFit(
				getImage(left, l_rot, 'E'),
				getImage(right, r_rot, 'W')
				):
				wrong_tiles.append(row*3 + gap)
				wrong_tiles.append(row*3 + gap + 1)
	# cols
	for col in range(3):
		for gap in range(2):
			up, u_rot = map[col + gap*3]
			down, d_rot = map[col + (gap+1)*3]
			if up == -1 or down == -1:
				# not yet set, ignore gap
				continue
			if not doImagesFit(
				getImage(up, u_rot, 'S'),
				getImage(down, d_rot, 'N')
				):
				wrong_tiles.append(col + gap*3)
				wrong_tiles.append(col + (gap+1)*3)
	return wrong_tiles

def pad(s):
	return s if len(s) >= 3 else " "*(3-len(s)) + s

def pretty(map):
	out = ""

	for row in range(3):
		left, l_rot = map[row*3 + 0]
		middle, m_rot = map[row*3 + 1]
		right, r_rot = map[row*3 + 2]

		out += "*--%s--*--%s--*--%s--*\n" % (
			pad(getImage(left,		l_rot, 'N', allow_error=False)),
			pad(getImage(middle,	m_rot, 'N', allow_error=False)),
			pad(getImage(right,		r_rot, 'N', allow_error=False))
			)
		out += "|T%s   R%d|T%s   R%d|T%s   R%d|\n" % (
			"?" if left == -1 else str(left), l_rot,
			"?" if middle == -1 else str(middle), m_rot,
			"?" if right == -1 else str(right), r_rot
			)
		out += "|%s %s|%s %s|%s %s|\n" % (
			pad(getImage(left,		l_rot, 'W', allow_error=False)),
			pad(getImage(left,		l_rot, 'E', allow_error=False)),
			pad(getImage(middle,	m_rot, 'W', allow_error=False)),
			pad(getImage(middle,	m_rot, 'E', allow_error=False)),
			pad(getImage(right,		r_rot, 'W', allow_error=False)),
			pad(getImage(right,		r_rot, 'E', allow_error=False))
			)
		out += "|       "*3+"|\n"
		out += "*--%s--*--%s--*--%s--*\n" % (
			pad(getImage(left,		l_rot, 'S', allow_error=False)),
			pad(getImage(middle,	m_rot, 'S', allow_error=False)),
			pad(getImage(right, 	r_rot, 'S', allow_error=False))
			)
	return out[:-1]

#	tile_id, rotation
map = [(-1, 0) for i in range(9)]

def recurse(tile=0, tiles_used=[]):
	if VERBOSE:
		print "\n\n-------- Spot %d -------" % tile
		print ""
		print pretty(map)
		sleep(DELAY * 0.5)
	# for each tile not used
	for t in tiles:
		if t in tiles_used:
			continue
		
		# for each rotation
		for i in range(4):
			# update map
			map[tile] = (t, i)

			if VERBOSE:
				print pretty(map)

			# check that this tile fits
			wrong_tiles = check(map)
			if tile in wrong_tiles:
				if VERBOSE:
					#print "Tile #%d, rot=%d doesn't fit" % (t, i)
					sleep(DELAY * 0.1)
				continue
			else:
				if len(wrong_tiles) == 0 and tile==8:
					print "\n\nGot it\n"
					print pretty(map)
					quit()

			# looks good so far,
			# try out the rest of the tiles
			new_used = [tiles_used[x] if x < len(tiles_used) else t
							for x in range(len(tiles_used)+1)]
			recurse(tile=tile+1, tiles_used=new_used)

			if VERBOSE:
				print "\nBack to Spot %d" % tile
				print "tiles_used=" + str(tiles_used)
				print ""
				print pretty(map)
				sleep(DELAY * 1)
	# No tiles fit anymore
	# Backtrack a layer, free tiles, clear map
	map[tile] = (-1, 0)


if __name__ == '__main__':
	if "--verbose" in sys.argv:
		VERBOSE = True
		DELAY = 1.0 / float(raw_input("Specify the animation speed: ") or "1.0")
	else:
		VERBOSE = False
		SPEED = 1.0
		print "use --verbose if you want more output"

	recurse()
	print "Nope :/"