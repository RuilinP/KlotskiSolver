from copy import deepcopy
from heapq import heappush, heappop
import time
import argparse
import sys

#====================================================================================

char_goal = '1'
char_single = '2'

class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal, is_single, coord_x, coord_y, orientation):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v') 
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_goal = is_goal
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single, \
            self.coord_x, self.coord_y, self.orientation)

    def move(self, direction):
        if direction == "up":
            if check_coord(self.coord_x, self.coord_y-1):
                self.coord_y -= 1
            else:
                print("Invalid move")
        elif direction == "down":
            if check_coord(self.coord_x, self.coord_y+1):
                self.coord_y += 1
            else:
                print("Invalid move")
        elif direction == "left":
            if check_coord(self.coord_x-1, self.coord_y):
                self.coord_x -= 1
            else:
                print("Invalid move")
        elif direction == "right":
            if check_coord(self.coord_x+1, self.coord_y):
                self.coord_x += 1
            else:
                print("Invalid move")

def check_coord(coord_x, coord_y):
    return coord_x > -1 and coord_x < 4 and coord_y > -1 and coord_y < 5


    


if __name__ == "__main__":
    Cao = Piece(True, False, 0, 0, None)
    Cao.move("right")
    Cao.move("down")
    print(Cao)
