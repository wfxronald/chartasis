import os, csv, sys

# Input by the user to obtain the relevant csv
try:
    mode = sys.argv[1]
    level = sys.argv[2]
except IndexError:
    print("Usage: python3 get_individual_level.py <mode> <level>")
    exit()

# Convert #xxx: yyy; format to {'xxx': 'yyy'}
def convert_to_dict(ssc_header):
    res = {}
    parsed = ssc_header.split("#")
    for item in parsed:
        if item and item != '\n':
            key = item.split(":")[0]
            value = item.split(":")[1].split(";")[0]
            res[key] = value
    return res

def count(equal_format):
    parsed = equal_format.split(",")
    count = 0
    for item in parsed:
        if item:
            count += 1
    return count

def convert_stepf2_note(stepf2_note):
    # print(stepf2_note)
    # As of now return as all fake notes
    return '0'

def convert_chart(string_format):
    split_on_line_break = string_format.split("\n")
    result = []
    for line in split_on_line_break:
        row = []
        if not line or ',' in line or '//' in line:
            continue

        encounter_open_bracket = False
        stepf2_note = ''
        for char in line:
            '''
            StepF2 Note syntax: {note type|attribute|fake flag|unknown flag}
            attribute: n-normal, v-vanish, s-sudden, h-hidden
            fake: 1-fake, 0-normal
            '''
            if char == '{':
                encounter_open_bracket = True
                stepf2_note += char
                continue
            if char == '}':
                stepf2_note += char
                row.append(convert_stepf2_note(stepf2_note))
                encounter_open_bracket = False
                stepf2_note = ''
                continue
            if encounter_open_bracket:
                stepf2_note += char
                continue

            row.append(char)

        # Ensure that the length is correct for either singles or doubles
        if len(row) != 5 and len(row) != 10:
            raise Exception("Error in parsing row")

        result.append(row)
    return result

def deduce_from_cut(cut_string):
    if cut_string == 'SHORTCUT':
        return 60
    elif cut_string == 'ARCADE':
        return 120
    elif cut_string == 'REMIX':
        return 180
    elif cut_string == 'FULLSONG':
        return 240

# To be implemented
def analyse_twist(chart_array):
    pass

def analyse_run(chart_array):
    pass

def analyse_brackets(chart_array):
    pass

def analyse_drill(chart_array):
    pass

def analyse_half(chart_array):
    pass

folder = 'steps/'
output = []
header = ['title', 'artist', 'bpm', 'length', 'bpm_change_count', 'stops_gimmick_count', 'scroll_speed_gimmick_count']
output.append(header)
with os.scandir(folder) as entries:
    for entry in entries:
        # Loop through all the stepcharts in the folder
        to_open = os.path.join(folder, entry.name)
        with open (to_open, "r") as file:
            data = file.read()

        # Split for different charts
        parsed = data.split("//---------------")
        song_info = parsed[0]
        info_dict = convert_to_dict(song_info)
        list_of_chart = parsed[1:]

        # Get chart of a particular level
        for chart in list_of_chart:
            level_info = chart.split("----------------")[0].lower()
            chart_info = chart.split("----------------")[1]
            if mode + level in level_info and 'ucs' not in level_info:
                print(info_dict['TITLE'] + " " + mode + level)
                chart_dict = convert_to_dict(chart_info)

                # Collect information to be put into csv
                title = info_dict['TITLE']
                artist = info_dict['ARTIST']
                if 'DISPLAYBPM' in info_dict:
                    bpm = info_dict['DISPLAYBPM']
                else:
                    bpm = info_dict['BPMS'].split("=")[1]
                if 'LASTSECONDHINT' in info_dict:
                    length = info_dict['LASTSECONDHINT']
                else:
                    length = deduce_from_cut(info_dict['SONGTYPE'])

                bpm_change_count = count(chart_dict['BPMS'])
                stops_gimmick_count = count(chart_dict['STOPS']) + count(chart_dict['DELAYS'])
                scroll_speed_gimmick_count = count(chart_dict['SPEEDS']) + count(chart_dict['SCROLLS'])
                converted_chart = convert_chart(chart_dict['NOTES'])

                output.append([title, artist, bpm, length, bpm_change_count, stops_gimmick_count, scroll_speed_gimmick_count])

with open(mode + level + '.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(output)
