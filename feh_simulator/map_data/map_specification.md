A valid map data file should contains:

num_rows
num_cols
terrain

An example:
8
6
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0


Terrain type specification:
0: plain
1: forest (which prevents calvary movement-type from passing or standing on)
2: water/mountain (only flying movement-type can pass or stand on)
3: half-barrier (if attacked once, its value becomes 0)
4: full-barrier (if attacked once, its value becomes 4)
5: unbreakable-barrier (no unit can pass or stand on)

Other terrain types are not implemented yet
