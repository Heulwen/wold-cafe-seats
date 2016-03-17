from itertools import combinations
from random import shuffle

TABLE_SIZE = 3
NUMBER_OF_TABLES = 4

ALL_PEOPLE = list(range(1, 13))
rounds = range(1, 5)

exclusives = (
	[1, 2],
	[3, 4],
	[5, 6],
	[7, 8, 9]
)

potentially_exclusive = list(range(1, 10))

neighbors_list = {}

neighbors_list_count = {}

tables_not_visited = {}
for p in ALL_PEOPLE:
	tables_not_visited[p] = list(range(0, NUMBER_OF_TABLES)) 


def get_bad_people(p):
	for group in exclusives:
		if p in group:
			return [i for i in group if i != p]
	print "bad group"
	return []

def update_neighbors(table):
	for p in table:
		if p not in neighbors_list:
			neighbors_list[p] = set()
		neighbors_list[p].update([i for i in table if i != p])

		if p not in neighbors_list_count:
			neighbors_list_count[p] = {}

		for i in table:
			if i != p:
				if i not in neighbors_list_count[p]:
					neighbors_list_count[p][i] = 0

				neighbors_list_count[p][i] += 1


def get_weight(candidate, table):
	# print 'candidate', candidate
	# print 'neighbors', neighbors_list
	if candidate not in neighbors_list:
		return 0
	return len(neighbors_list[candidate].intersection(table))

def get_best_candidate(candidates, table):
	weighted_list = [(c, get_weight(c, table)) for c in candidates]
	def srt(tup):
		return tup[1]
	weighted_list.sort(key=srt)
	# weighted_list.reverse()
	# print weighted_list
	return weighted_list[0][0]


def generate_table(table, people):
	candidates = []
	for p in [i for i in people]:
		skip = False
		if p in potentially_exclusive:
			bad_neighbors = get_bad_people(p)
			for b in bad_neighbors:
				if b in table:
					skip = True
		if not skip:
			candidates.append(p)
			# people.pop(people.index(p)

	while len(table) < TABLE_SIZE:
		c = get_best_candidate(candidates, table)
		table.append(c)
		candidates.pop(candidates.index(c))
		people.pop(people.index(c))

	update_neighbors(table)
	return table

def bad_neighbor(me, neighbor):
	if me in potentially_exclusive:
		bad_neighbors = get_bad_people(me)
		return neighbor in bad_neighbors
	return False

def get_table_weight(p, t, tables):
	weight = 0
	for neighbor in tables[t]:
		if bad_neighbor(p, neighbor):
			weight += 999

		if p in neighbors_list_count and neighbor in neighbors_list_count[p]:
			weight += neighbors_list_count[p][neighbor]
	return weight

def get_best_table(p, tables, available_tables_names):
	weighted_list = [(t, get_table_weight(p, t, tables)) for t in available_tables_names if len(tables[t]) < TABLE_SIZE]
	def srt(tup):
		return tup[1]
	weighted_list.sort(key=srt)
	# weighted_list.reverse()
	# print weighted_list
	return weighted_list[0][0]

def update_table_neighbors(table, p):
	for n in table:
		if n != p:
			if n not in neighbors_list:
				neighbors_list[n] = set()
			neighbors_list[n].add(p)

			if n not in neighbors_list_count:
				neighbors_list_count[n] = {}

			if p not in neighbors_list_count[n]:
				neighbors_list_count[n][p] = 0

			neighbors_list_count[n][p] += 1

		if n == p:
			if n not in neighbors_list:
				neighbors_list[n] = set()
			neighbors_list[p].update([i for i in table if i != p])

			if p not in neighbors_list_count:
				neighbors_list_count[n] = {}

			for i in table:
				if i != p:
					if i not in neighbors_list_count[p]:
						neighbors_list_count[p][i] = 0
					neighbors_list_count[p][i] += 1


def assign_to_table(p, tables):
	best_table_name = get_best_table(p, tables, tables_not_visited[p])
	tables[best_table_name].append(p)
	tables_not_visited[p].pop(tables_not_visited[p].index(best_table_name))	
	update_table_neighbors(tables[best_table_name], p)

def generate_tables():
	tables = []
	people = [i for i in ALL_PEOPLE]
	shuffle(people)

	for _ in range(0, NUMBER_OF_TABLES):
		tables.append([])

	# for table in tables:
	# 	generate_table(table, people)

	for p in people:
		assign_to_table(p, tables)

	return tables

round_tables = []

list_of_neighbors = {}

for r in rounds:
	print '*'*80
	print 'ROUND', r
	print '*'*80
	tables = generate_tables()
	for table in tables:
		table.sort()
	print tables
	round_tables.append(tables)

# print round_tables
max_neighbors = 0

for p in neighbors_list_count:
	for n in neighbors_list_count[p]:
		if neighbors_list_count[p][n] > max_neighbors:
			max_neighbors = neighbors_list_count[p][n]

print "Max neighbors count: ", max_neighbors


