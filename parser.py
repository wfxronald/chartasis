import json, os, re

# Helper function
def clean_key(key):
	return key[1:] if len(key) != 0 and key[0] == "#" else key

def clean_value(value):
	return value[:-1] if len(value) != 0 and value[-1] == ";" else value

def clean_preceding_line_break(str):
	return str[1:] if len(str) != 0 and str[0:1] == "\n" else str

def clean_notes(notes):
	measures = re.split(",.*\n", notes) # measure splitter
	measures[0] = clean_preceding_line_break(measures[0])
	return measures

def is_chart_ucs(chart):
	return "UCS" in chart['step_meta']['DESCRIPTION']

def is_chart_sp(chart):
	return "SP" in chart['step_meta']['DESCRIPTION']

def is_chart_dp(chart):
	return "DP" in chart['step_meta']['DESCRIPTION']

def clean_meta_information(metas, wanted_key):
	result = {}
	for meta in metas:
		split_key_value = meta.split(":")

		# ignore dirty data
		if len(split_key_value) < 2:
			continue

		key = clean_key(split_key_value[0])
		value = clean_value(split_key_value[1])
		if key in wanted_key:
			result[key] = value
	return result


# Main function
def parse_chart(data):
	cleaned = {}
	charts = []

	split_on_step = data.split("//---------------")
	for i in range(len(split_on_step)):
		step = split_on_step[i]

		# first element will be the song meta
		if i == 0:
			wanted_key = {"TITLE", "ARTIST", "SONGCATEGORY", "SONGTYPE", "DISPLAYBPM"}
			song_meta = step.split("\n")
			cleaned_song_meta = clean_meta_information(song_meta, wanted_key)
			cleaned['song_meta'] = cleaned_song_meta
			continue

		split_on_notes = step.split("#NOTES:")
		
		chart = {}
		chart['notes'] = clean_notes(split_on_notes[1])
		step_meta = split_on_notes[0].split("\n")

		wanted_key = {"DESCRIPTION", "METER", "BPMS", "DISPLAYBPM"}
		cleaned_step_meta = clean_meta_information(step_meta, wanted_key)
		chart['step_meta'] = cleaned_step_meta

		if 'DESCRIPTION' not in chart['step_meta']:
			continue
		if not is_chart_ucs(chart) and not is_chart_dp(chart) and not is_chart_sp(chart):
			charts.append(chart)

	cleaned['charts'] = charts
	return cleaned

result = []
folder = 'steps/'
with os.scandir(folder) as entries:
	for entry in entries:
		# Loop through all the stepcharts in the folder
		to_open = os.path.join(folder, entry.name)
		with open (to_open, "r") as file:
			data = file.read()

		# Main parser function
		cleaned = parse_chart(data)
		result.append(cleaned)

with open('result.json', 'w') as f:
	json.dump(result, f)
