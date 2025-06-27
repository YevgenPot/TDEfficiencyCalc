import os
import re

'''
inputModule v1

input portion of the program
    reads data from file

    code is almost all ai here
    if it works it works
    
    (might not work in scale
    i am planning on working with nodes as data structs
    and not dictionaries
    in the future)

input is the filename string correlating to a file in the dataDir

output is a structured dictionary of dictionaries
    structure:
        { tower_name: { block_name: { key: value } } }

'''

def mainInput():
    filename = "entry.txt"
    towers_data = parse_custom_format(filename)
    
    #import pprint
    #pprint.pprint(towers_data)
    return towers_data

def parse_custom_format(filename):
    towers = {}
    current_tower = None
    current_block = None
    inside_block = False
    block_content = []

    # Matches towername line: - towername -
    towername_pattern = re.compile(r"^\s*-\s*(.+?)\s*-\s*$")

    # Matches block start: e.g. placement{ or up1-1{
    block_start_pattern = re.compile(r"^(\w[\w\-]*)\s*\{$")

    # Matches key=value lines: stat0=123,
    key_value_pattern = re.compile(r"^\s*(\w+)\s*=\s*(.+?),?\s*$")

    filePath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(filePath, "dataDir" , filename)

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Check if line is tower name
            tower_match = towername_pattern.match(line)
            if tower_match:
                current_tower = tower_match.group(1)
                #if current_tower not in towers:
                towers[current_tower] = {}
                current_block = None
                inside_block = False
                continue

            # Check if block start
            block_start_match = block_start_pattern.match(line)
            if block_start_match:
                current_block = block_start_match.group(1)
                inside_block = True
                block_content = []
                continue

            # Check if block end
            if line == "}" and inside_block:
                # Parse collected block_content lines
                block_dict = {}
                optional_tags = []
                for item in block_content:
                    kv_match = key_value_pattern.match(item)
                    if kv_match:
                        key = kv_match.group(1)
                        val = kv_match.group(2).rstrip(",")
                        # Try to convert numbers
                        if val.isdigit():
                            val = int(val)
                        else:
                            try:
                                val = float(val)
                            except ValueError:
                                val = val.strip()
                        block_dict[key] = val
                    else:
                        # If line doesn't match key=value, treat as optional tag
                        optional_tags.append(item.strip(","))
                if optional_tags:
                    block_dict["tags"] = optional_tags

                towers[current_tower][current_block] = block_dict
                inside_block = False
                current_block = None
                block_content = []
                continue

            # If inside block, accumulate content lines
            if inside_block:
                block_content.append(line)

    return towers

if __name__ == "__main__":
    mainInput()


''' sample output (outdated, pls fix)
'Missile Trooper': {'placement': {'Cost': 1250,
                                   'DMG': 40,
                                   'Range': 16.0,
                                   'Reload': 7.5,
                                   'tags': ['[Splash]']},
                     'up1-1': {'DMG': 75,
                               'Range': 16,
                               'Reload': 7.5,
                               'deltaCost': 1000},
                     'up1-2': {'DMG': 75,
                               'Range': 19,
                               'Reload': 7.5,
                               'deltaCost': 350},
                     'up1-3': {'DMG': 100,
                               'Range': 23,
                               'Reload': 6.5,
                               'deltaCost': 2000},
                     'up1-4': {'DMG': 160,
                               'Range': 27,
                               'Reload': 6.5,
                               'deltaCost': 3250},
                     'up1-5': {'DMG': 220,
                               'Range': 39,
                               'Reload': 4.5,
                               'deltaCost': 12500,
                               'tags': ['[Primary Target]']},
                     'up2-1': {'DMG': 40,
                               'Range': 16,
                               'Reload': 6.5,
                               'deltaCost': 275},
                     'up2-2': {'DMG': 40,
                               'Range': 16,
                               'Reload': 5.5,
                               'deltaCost': 300},
                     'up2-3': {'DMG': 80,
                               'Range': 16,
                               'Reload': 7,
                               'deltaCost': 2800},
                     'up2-4': {'DMG': 165,
                               'Range': 19,
                               'Reload': 7,
                               'deltaCost': 3850},
                     'up2-5': {'DMG': 65,
                               'Range': 19,
                               'Reload': 0.6,
                               'deltaCost': 23000}},
'''