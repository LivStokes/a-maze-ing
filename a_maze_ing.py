#!/usr/bin/env python3

import sys
from config import parse_config, ConfigError
from pathlib import Path

if len(sys.argv) != 2:
	print("!Error!\n Usage: python3 a_maze_ing.py config.txt")
	sys.exit(1)

try:
	config = parse_config(Path(sys.argv[1]))
	output_file = Path(config.pop("output_file"))
except ConfigError as e:
    print(f"Config error: {e}")
    sys.exit(1)
	


# What am I parsing??
'''
Parsing configuration describing how to create/uptput the maze
Extracting structured meaning from text
'''
# config.txt file

# hexidecimal grid text

# Good layout structure
'''
config.txt
parse_config()
python dictionary / config object
maze generation algorithm
maze representation
ascii renderer
output file
'''
