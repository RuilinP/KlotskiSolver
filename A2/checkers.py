import argparse
import copy
import sys
import time

cache = {} # you can use this to implement state caching!

# class Game:
#     def __init__(self):
#         pass
####################################################



class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):

        self.board = board

        self.width = 8
        self.height = 8
        self.blue_left = self.red_left = 0
        self.blue_king_left = self.red_king_left = 0
        self.jumping = False
        # count # of blue and red in the initial board
        for row in board:
            for col in row:
                if col == 'b':
                    self.blue_left += 1
                elif col == 'r':
                    self.red_left += 1


    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")

    def eval(self):
        return self.blue_left - self.red_left + self.blue_king_left * 0.5 - self.red_king_left * 0.5

    def get_all_pieces(self, color):
        pieces = []
        if color == "b":
            color1 = ['B', 'b']
        else:
            color1 = ['R', 'r']
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] in color1:
                    pieces.append([row, col])
        return pieces
    
    def get_board(self):
        return self.board
    
    def move(self, old_row, old_col, new_row, new_col):
        piece = self.board[old_row][old_col]
        self.board[old_row][old_col] = '.'
        self.board[new_row][new_col] = piece
        
        if new_row == self.height - 1 or new_row == 0:
            if piece == 'r':
                self.board[new_row][new_col] = 'R'
                self.red_king_left += 1
            else:
                self.board[new_row][new_col] = 'B'
                self.blue_king_left += 1
        self.display()

    def valid_move(self, player, old_row, old_col, new_row, new_col):
        #player = self.board[old_row][old_col]
        if self.board[new_row][new_col] != '.':
            return False, None
        
        if player.isupper() and abs(old_row - new_row) == 1 and abs(old_col - new_col) == 1 and not self.jumping:
            # King moving up/downward is valid
            return True, None
        elif player == 'b' and new_row - old_row == 1 and abs(old_col - new_col) == 1 and not self.jumping:
            # Normal red moving upward
            return True, None
        elif player == 'r' and old_row - new_row == 1 and abs(old_col - new_col) == 1 and not self.jumping:
            # Normal blue moving downward
            return True, None
        
        if player.isupper() and abs(old_row - new_row) == 2 and abs(old_col - new_col) == 2:
            # King piece make a jump, record the eaten piece
            eaten_row = int((new_row - old_row) / 2 + old_row)
            eaten_col = int((new_col - old_col) / 2 + old_col)
            if self.board[eaten_row][eaten_col].lower() not in [player, '.']:
                return True, [eaten_row, eaten_col]
        elif player == 'b' and new_row - old_row == 2 and abs(old_col - new_col) == 2:
            # blue piece make a jump, record the eaten piece
            eaten_row = int((new_row - old_row) / 2 + old_row)
            eaten_col = int((new_col - old_col) / 2 + old_col)
            if self.board[eaten_row][eaten_col].lower() not in [player, '.']:
                return True, [eaten_row, eaten_col]
        elif player == 'r' and old_row - new_row == 2 and abs(old_col - new_col) == 2:
            # red piece make a jump, record the eaten piece
            eaten_row = int((new_row - old_row) / 2 + old_row)
            eaten_col = int((new_col - old_col) / 2 + old_col)
            if self.board[eaten_row][eaten_col].lower() not in [player, '.']:
                return True, [eaten_row, eaten_col]
        return False, None


    def get_valid_moves(self, player):
        moves = []
        for i in self.get_all_pieces(player):
            for x in [-1, 1]:
                for y in [-1, 1]:
                    new_loc = [i[0] + x, i[1] + y]
                    if (new_loc[0] < self.width) & (new_loc[0] >= 0) & (new_loc[1] < self.height) & (new_loc[1] >= 0):
                        
                        is_valid_move, jump = self.valid_move(self.board[i[0]][i[1]], i[0], i[1], new_loc[0], new_loc[1])
                        if is_valid_move:
                            moves.append([i, [i[0] + x, i[1] + y], None])
            can_jump = True
            
            old_loc = i
            jumped_list = [] # multiple jumps until no more jump can be made
            ban_direction = []
            while can_jump:
                can_jump = False
                jump_found = False
                for x in [-2, 2]:
                    for y in [-2, 2]:
                        if not jump_found and ban_direction != [x,y]:
                            new_loc = [old_loc[0] + x, old_loc[1] + y]
                            if (new_loc[0] < self.width) & (new_loc[0] >= 0) & (new_loc[1] < self.height) & (new_loc[1] >= 0):
                                is_valid_move, jump = self.valid_move(self.board[i[0]][i[1]], old_loc[0], old_loc[1], new_loc[0], new_loc[1])

                                if is_valid_move:
                                    can_jump = True
                                    jump_found = True
                                    jumped_list.append(jump)
                                    moves.append([i, new_loc, jumped_list])
                                    old_loc = new_loc
                                    ban_direction = [-x, -y]
            return moves


    def winner(self):
        if self.red_left <= 0:
            return "b"
        elif self.blue_left <= 0:
            return "r"
        return None

##########################################################
def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board
######################################################


def alpha_beta_search(state, depth, player, alpha=float('-inf'), beta=float('+inf')):
    if state.winner() != None or depth == 0:
        if state.winner() == 'r':
            return float('-inf'), None
        elif state.winner() == 'b':
            return float('inf'), None
        return state.eval(), None
    if player == 'r':
        pass
    

if __name__ == '__main__':

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "--inputfile",
    #     type=str,
    #     required=True,
    #     help="The input file that contains the puzzles."
    # )
    # parser.add_argument(
    #     "--outputfile",
    #     type=str,
    #     required=True,
    #     help="The output file that contains the solution."
    # )
    # args = parser.parse_args()

    # initial_board = read_from_file(args.inputfile)
    # state = State(initial_board)
    # turn = 'r'
    # ctr = 0

    # sys.stdout = open(args.outputfile, 'w')

    # sys.stdout = sys.__stdout__

    initial_board = read_from_file("won.txt")
    state = State(initial_board)
    # print(state.eval())
    # print(state.get_all_pieces("Blue"))
    #sys.stdout = open("sol.txt", 'w')
    print("solving puzzle")
    state.display()
    print()
    turn = 'r'
    ctr = 0
    # while state.winner() is None:
    #     evaluation, next_moves = alpha_beta_search(initial_board, 3, turn)
    #print(state.valid_move(6, 3, 4, 1))
    print(state.get_valid_moves('b'))


    #sys.stdout = sys.__stdout__
    
    







