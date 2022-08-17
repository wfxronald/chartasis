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

def get_notes_count(notes):
	# count non-zero entry, no regards to fake notes
	count = 0
	for measure in notes:
		for char in measure:
			if char != "0":
				count += 1
	return count

def get_jumps_and_brackets_count(notes):
	jumps_count = 0
	brackets_count = 0
	for measure in notes:
		rows = measure.split("\n")
		for row in rows:
			non_zero = 0
			for char in row:
				if char != "0":
					non_zero += 1

			if non_zero == 2:
				jumps_count += 1
			elif non_zero > 2:
				brackets_count += 1 
	return jumps_count, brackets_count


# process json file
with open('result.json') as json_file:
    data = json.load(json_file)

output = []
header = ['title', 'artist', 'bpm', 'length', 'category', 'mode', 'level']
features_engineered = [
	'measure_count', 'notes_count', 'jumps_count', 'brackets_count'
]
header.extend(features_engineered)
output.append(header)

for song in data:
	title = song['song_meta']['TITLE']
	artist = song['song_meta']['ARTIST']
	length = song['song_meta']['SONGTYPE']
	category = song['song_meta']['SONGCATEGORY']

	for chart in song['charts']:
		mode = chart['step_meta']['DESCRIPTION'][0].upper() # S or D
		if mode not in ['S', 'D']: # skip dirty data
			continue
		level = chart['step_meta']['METER']

		bpm = get_bpm(song['song_meta'], chart['step_meta'])
		basic_info = [title, artist, bpm, length, category, mode, level]

		measure_count = len(chart['notes'])
		notes_count = get_notes_count(chart['notes'])
		jumps_count, brackets_count = get_jumps_and_brackets_count(chart['notes'])

		basic_info.extend([measure_count, notes_count, jumps_count, brackets_count])
		output.append(basic_info)

with open('cleaned.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(output)
