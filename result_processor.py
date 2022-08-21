import csv, json

# helper function
def get_bpm(song_meta, step_meta):
	bpm = ""
	if 'DISPLAYBPM' in song_meta:
		bpm = song_meta['DISPLAYBPM']
	elif 'DISPLAYBPM' in step_meta:
		bpm = step_meta['DISPLAYBPM']
	elif 'BPMS' in step_meta:
		bpm = step_meta['BPMS'].split("=")[1]
	return bpm

def transform_into_array(notes):
	combined_string = ""
	for measure in notes:
		combined_string += measure

	row_by_row = combined_string.split("\n")
	cleaned = []
	for row in row_by_row:
		if len(row) in [5, 6, 10]:
			cleaned.append(row)
	return cleaned

def get_notes_count(array):
	# count non-zero entry, no regards to fake notes
	count = 0
	for row in array:
		for char in row:
			if char != "0":
				count += 1
	return count

def get_middle_four_notes_count(array):
	count = 0
	for row in array:
		if len(row) not in [6, 10]:
			continue

		if len(row) == 6:
			if row[1] != "0":
				count += 1
			if row[2] != "0":
				count += 1
			if row[3] != "0":
				count += 1
			if row[4] != "0":
				count += 1
		elif len(row) == 10:
			if row[3] != "0":
				count += 1
			if row[4] != "0":
				count += 1
			if row[5] != "0":
				count += 1
			if row[6] != "0":
				count += 1

	return count

def get_middle_six_notes_count(array):
	count = 0
	for row in array:
		if len(row) not in [6, 10]:
			continue

		if len(row) == 6:
			if row[0] != "0":
				count += 1
			if row[1] != "0":
				count += 1
			if row[2] != "0":
				count += 1
			if row[3] != "0":
				count += 1
			if row[4] != "0":
				count += 1
			if row[5] != "0":
				count += 1
		elif len(row) == 10:
			if row[2] != "0":
				count += 1
			if row[3] != "0":
				count += 1
			if row[4] != "0":
				count += 1
			if row[5] != "0":
				count += 1
			if row[6] != "0":
				count += 1
			if row[7] != "0":
				count += 1

	return count

def get_jumps_and_brackets_count(array):
	jumps_count = 0
	brackets_count = 0
	for row in array:
		non_zero = 0
		for char in row:
			if char != "0":
				non_zero += 1

		if non_zero == 2:
			jumps_count += 1
		elif non_zero > 2:
			brackets_count += 1 
	return jumps_count, brackets_count

def get_consecutive_red_blue_count(array):
	count = 0
	prev_row = ""
	for row in array:
		if len(row) not in [5, 6, 10]:
			continue

		if prev_row != "":
			if len(row) == 5:
				if prev_row[0] != '0' and row[1] != '0':
					count += 1
				if prev_row[1] != '0' and row[0] != '0':
					count += 1
				if prev_row[3] != '0' and row[4] != '0':
					count += 1
				if prev_row[4] != '0' and row[3] != '0':
					count += 1

			if len(row) == 6:
				if prev_row[1] != '0' and row[2] != '0':
					count += 1
				if prev_row[2] != '0' and row[1] != '0':
					count += 1
				if prev_row[3] != '0' and row[4] != '0':
					count += 1
				if prev_row[4] != '0' and row[3] != '0':
					count += 1

			elif len(row) == 10:
				if prev_row[0] != '0' and row[1] != '0':
					count += 1
				if prev_row[1] != '0' and row[0] != '0':
					count += 1
				if prev_row[3] != '0' and row[4] != '0':
					count += 1
				if prev_row[4] != '0' and row[3] != '0':
					count += 1
				if prev_row[5] != '0' and row[6] != '0':
					count += 1
				if prev_row[6] != '0' and row[5] != '0':
					count += 1
				if prev_row[8] != '0' and row[9] != '0':
					count += 1
				if prev_row[9] != '0' and row[8] != '0':
					count += 1

		prev_row = row

	return count

def get_straight_red_twist(array):
	count = 0
	prev_prev_row = ""
	prev_row = ""
	for row in array:
		if len(row) not in [5, 6, 10]:
			continue

		if prev_prev_row != "" and prev_row != "":
			if len(row) == 5:
				if prev_prev_row[1] != '0' and prev_row[2] != '0' and row[3] != '0':
					count += 1
				if prev_prev_row[3] != '0' and prev_row[2] != '0' and row[1] != '0':
					count += 1

			if len(row) == 6:
				if prev_prev_row[0] != '0' and prev_row[1] != '0' and row[4] != '0':
					count += 1
				if prev_prev_row[4] != '0' and prev_row[1] != '0' and row[0] != '0':
					count += 1
				if prev_prev_row[1] != '0' and prev_row[4] != '0' and row[5] != '0':
					count += 1
				if prev_prev_row[5] != '0' and prev_row[4] != '0' and row[1] != '0':
					count += 1

			elif len(row) == 10:
				if prev_prev_row[1] != '0' and prev_row[2] != '0' and row[3] != '0':
					count += 1
				if prev_prev_row[3] != '0' and prev_row[2] != '0' and row[1] != '0':
					count += 1
				if prev_prev_row[6] != '0' and prev_row[7] != '0' and row[8] != '0':
					count += 1
				if prev_prev_row[8] != '0' and prev_row[7] != '0' and row[6] != '0':
					count += 1

				if prev_prev_row[2] != '0' and prev_row[3] != '0' and row[6] != '0':
					count += 1
				if prev_prev_row[6] != '0' and prev_row[3] != '0' and row[2] != '0':
					count += 1
				if prev_prev_row[3] != '0' and prev_row[6] != '0' and row[7] != '0':
					count += 1
				if prev_prev_row[7] != '0' and prev_row[6] != '0' and row[3] != '0':
					count += 1

		prev_prev_row = prev_row
		prev_row = row

	return count

def get_straight_blue_twist(array):
	count = 0
	prev_prev_row = ""
	prev_row = ""
	for row in array:
		if len(row) not in [5, 6, 10]:
			continue

		if prev_prev_row != "" and prev_row != "":
			if len(row) == 5:
				if prev_prev_row[0] != '0' and prev_row[2] != '0' and row[4] != '0':
					count += 1
				if prev_prev_row[4] != '0' and prev_row[2] != '0' and row[0] != '0':
					count += 1

			if len(row) == 6:
				if prev_prev_row[0] != '0' and prev_row[2] != '0' and row[3] != '0':
					count += 1
				if prev_prev_row[3] != '0' and prev_row[2] != '0' and row[0] != '0':
					count += 1
				if prev_prev_row[2] != '0' and prev_row[3] != '0' and row[5] != '0':
					count += 1
				if prev_prev_row[5] != '0' and prev_row[3] != '0' and row[2] != '0':
					count += 1

			elif len(row) == 10:
				if prev_prev_row[0] != '0' and prev_row[2] != '0' and row[4] != '0':
					count += 1
				if prev_prev_row[4] != '0' and prev_row[2] != '0' and row[0] != '0':
					count += 1
				if prev_prev_row[5] != '0' and prev_row[7] != '0' and row[9] != '0':
					count += 1
				if prev_prev_row[9] != '0' and prev_row[7] != '0' and row[5] != '0':
					count += 1

				if prev_prev_row[2] != '0' and prev_row[4] != '0' and row[5] != '0':
					count += 1
				if prev_prev_row[5] != '0' and prev_row[4] != '0' and row[2] != '0':
					count += 1
				if prev_prev_row[4] != '0' and prev_row[5] != '0' and row[7] != '0':
					count += 1
				if prev_prev_row[7] != '0' and prev_row[5] != '0' and row[4] != '0':
					count += 1

		prev_prev_row = prev_row
		prev_row = row

	return count



# process json file
with open('result.json') as json_file:
    data = json.load(json_file)

output = []
header = ['title', 'artist', 'bpm', 'length', 'category', 'mode', 'level']
features_engineered = [
	'measure_count', 'notes_count', 'jumps_count', 'brackets_count',
	'red_blue_count', 'straight_red_count', 'straight_blue_count', 'middle_four_count', 'middle_six_count'
]
header.extend(features_engineered)
output.append(header)

for song in data:
	title = song['song_meta']['TITLE']
	artist = song['song_meta']['ARTIST']
	length = song['song_meta']['SONGTYPE']
	category = song['song_meta']['SONGCATEGORY']

	for chart in song['charts']:
		mode = chart['step_meta']['DESCRIPTION'] # S or D
		if mode == "" or mode[0].upper() not in ['S', 'D']: # skip dirty data
			continue
		mode = mode[0].upper()
		level = chart['step_meta']['METER']
		if level == "99": # skip more dirty data
			continue

		bpm = get_bpm(song['song_meta'], chart['step_meta'])
		basic_info = [title, artist, bpm, length, category, mode, level]

		measure_count = len(chart['notes'])
		array = transform_into_array(chart['notes'])
		notes_count = get_notes_count(array)
		jumps_count, brackets_count = get_jumps_and_brackets_count(array)
		red_blue_count = get_consecutive_red_blue_count(array)
		straight_red_count = get_straight_red_twist(array)
		straight_blue_count = get_straight_blue_twist(array)
		middle_four_count = get_middle_four_notes_count(array)
		middle_six_count = get_middle_six_notes_count(array)

		basic_info.extend([
			measure_count, notes_count, jumps_count, brackets_count,
			red_blue_count, straight_red_count, straight_blue_count, middle_four_count, middle_six_count
		])
		output.append(basic_info)

with open('cleaned.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(output)
