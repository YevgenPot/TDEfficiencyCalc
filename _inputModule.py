import os
import re

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