import sys
import pacman
"""
This module is used for running pacman.py

Expects a singlg input filename that it will pass into pacman.py

prints the return of the pacman function
"""

if(len(sys.argv) != 2):
	print("Requires 1 input file")
	exit()

print(pacman.pacman(sys.argv[1]))