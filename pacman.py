import numpy as np
"""
This module a single function which solves the FDS technical test involving a 'pacman' moving around a board, collection coins
as descriped here: https://gist.github.com/c3-pritak/592bb74b539b65812d5d1eb56202d488

Written for python 3.6
It runs in O(n) time

The function must be called from another file.
"""

__author__ = "Elijah Moreau-Arnott"

def err():
    return -1, -1, 0

# Expects a filepath, or name of a local file, which can be read from.
# It will return the final resting x and y position of the pacman, and the amount of coins collected OR -1, -1, 0 if there is an error
def pacman(input_file):
    """ Use this function to format your input/output arguments. Be sure not change the order of the output arguments. 
    Remember that code organization is very important to us, so we encourage the use of helper functions and classes as you see fit.
    
    Input:
        1. input_file (String) = contains the name of a text file you need to read that is in the same directory, includes the ".txt" extension
           (ie. "input.txt")
    Outputs:
        1. final_pos_x (int) = final x location of Pacman
        2. final_pos_y (int) = final y location of Pacman
        3. coins_collected (int) = the number of coins that have been collected by Pacman across all movements
    """

    # return final_pos_x, final_pos_y, coins_collected 

    # holds the state of all the primitive variables so that they are easier work with
    board = None

    # Helper function for catching errors in input
    def good_position(x, y):
        if (x < 0 or x >= board.shape[0] or y < 0 or y >= board.shape[1] or board[x,y] > 1):
            return 0
        return 1

    # Open file
    try:
        f = open(input_file)
    except IOError:
        print("Error opening file")
        return err()

    # File must include board size and starting position at least
    lines = f.readlines()
    if(len(lines) < 2):
        print("Not enought lines in input")
        return err()

    # Close file
    try:
        f.close()
    except IOError:
        print("Error closing file")
        return err()

    # Get board size
    try:
        w, h = (int(s) for s in lines[0].split())
    except ValueError:
        print("Non-int in input")
        return err()
    board = np.ones((w, h))

    # Get wall positions
    for line in lines[3:]:
        try:
            x, y = (int(s) for s in line.split()) 
        except ValueError:
            print("Non-int in input")
            return err()
        if(good_position(x, y)):
            board[x,y] = 3
        else:
            print("Wall outside of board or on top of another wall")
            return err()

    # Get starting position
    try:
        start_x, start_y = (int(s) for s in lines[1].split())
    except ValueError:
        print("Non-int in input")
        return err()
    if(good_position(start_x, start_y)):
        board[start_x,start_y] = 0
    else:
        print("Starting position outside of board or on top of wall")
        return err()

    path = ""
    # Follow the directions
    if(len(lines) > 2):
        path = lines[2].upper()

    # finalXposition, finalYposition, totalCoins
    # Now that we have collected the board, start postions, and path, we can compute the desired final positions
    return compute(board,start_x,start_y,path)




# Board, start positions, and path are passed
# returns the finalXposition, finalYposition, and totalCoins
def compute(board, start_x, start_y, path):
    class state:
        coins = 0
        pac_x = start_x
        pac_y = start_y

        # used in debugging
        def print_state(self):
            print(self.pac_x,self.pac_y,self.coins)

        def return_state(self):
            return self.pac_x,self.pac_y,self.coins
    s = state()

    def good_position(x, y):
        if (x < 0 or x >= board.shape[0] or y < 0 or y >= board.shape[1] or board[x,y] > 1):
            return 0
        return 1

    # Directional functions
    def move_west():
        if(s.pac_x != 0 and board[s.pac_x - 1, s.pac_y] != 3):
            s.pac_x -= 1
    def move_north():
        if(s.pac_y != board.shape[1]-1 and board[s.pac_x, s.pac_y + 1] != 3):
            s.pac_y += 1
    def move_east():
        if(s.pac_x != board.shape[0]-1 and board[s.pac_x + 1, s.pac_y] != 3):
            s.pac_x += 1
    def move_south():
        if(s.pac_y != 0 and board[s.pac_x, s.pac_y - 1] != 3):
            s.pac_y -= 1

    # Enables an easy switch-like statement
    dir_function = {
    "N": move_north,
    "E": move_east,
    "S": move_south,
    "W": move_west
    }
            
    # Takes a capital cardinal (NSEW) character as input
    # Changes the state by evaluation input
    def move(direction):
        move_function = dir_function.get(direction, None)
        if(move_function == None):
            # I will allow spaces and newline's in directions
            if(not(direction == " " or direction == chr(10))):
                print("Non-cardinal character encountered")
                raise ValueError
            return
        move_function()

        # collect coin
        if(board[s.pac_x,s.pac_y] == 1):
            s.coins += 1
            board[s.pac_x,s.pac_y] = 0

    # Follow the path
    # I will allow lowercase characters.  move expects uppercase
    for c in path:
        try:
            move(c)
        except ValueError:
            return err()

    # finalXposition, finalYposition, totalCoins
    return s.return_state()





