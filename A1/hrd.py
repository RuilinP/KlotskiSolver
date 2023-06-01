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
            if self._check_coord(direction):
                self.coord_y -= 1
            else:
                print("Invalid move")
        elif direction == "down":
            if self._check_coord(direction):
                self.coord_y += 1
            else:
                print("Invalid move")
        elif direction == "left":
            if self._check_coord(direction):
                self.coord_x -= 1
            else:
                print("Invalid move")
        elif direction == "right":
            if self._check_coord(direction):
                self.coord_x += 1
            else:
                print("Invalid move")
    

    def _check_coord(self, direction):
        """
        Check the new coord of the piece, return True if valid, False otherwise
        """
        if self.is_goal: #caocao
            if self.coord_y == 0 and direction == "up":
                return False
            elif self.coord_y == 3 and direction == "down":
                return False
            elif self.coord_x == 0 and direction == "left":
                return False
            elif self.coord_x == 2 and direction == "right":
                return False
            return True
        elif self.orientation == 'h': #horizontal general
            if self.coord_y == 0 and direction == "up":
                return False
            elif self.coord_y == 4 and direction == "down":
                return False
            elif self.coord_x == 0 and direction == "left":
                return False
            elif self.coord_x == 2 and direction == "right":
                return False
            return True
        elif self.orientation == 'v': #vertical general
            if self.coord_y == 0 and direction == "up":
                return False
            elif self.coord_y == 3 and direction == "down":
                return False
            elif self.coord_x == 0 and direction == "left":
                return False
            elif self.coord_x == 3 and direction == "right":
                return False
            return True
        else: #soldier
            if self.coord_y == 0 and direction == "up":
                return False
            elif self.coord_y == 4 and direction == "down":
                return False
            elif self.coord_x == 0 and direction == "left":
                return False
            elif self.coord_x == 3 and direction == "right":
                return False
            return True


    





class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = 5

        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()


    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = char_goal
                self.grid[piece.coord_y][piece.coord_x + 1] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = char_goal
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()




# def check_coord(coord_x, coord_y):
#     return coord_x > -1 and coord_x < 4 and coord_y > -1 and coord_y < 5


    


if __name__ == "__main__":
    caocao = Piece(True, False, 0, 0, None)
    zhangfei = Piece(False, False, 0, 2, 'h')
    caocao.move("left")
    caocao.move("down")
    caocao.move("down")
    caocao.move("down")
    caocao.move("down")
    # caocao.move("down")
    print(caocao)
    #board1 = Board()
