import os
import pacman
"""
This module is used for testing pacman.py in bulk

It simply passes all files that start with 'test' to the pacman function

TODO:
	add built in pass/fail check by comparing against expected output
"""

for file in os.listdir("."):
	if( file.startswith("test") ):
		print(file + ":")
		print(pacman.pacman(file))