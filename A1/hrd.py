from copy import deepcopy  
from heapq import heappush, heappop  
import time  
import argparse  
import sys  
import heapq  
import time
  
  
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
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single, self.coord_x, self.coord_y, self.orientation)  
  
    def move(self, direction):  
        if direction == "up":  
            self.coord_y -= 1  
        elif direction == "down":  
            self.coord_y += 1  
        elif direction == "left":  
            self.coord_x -= 1  
        elif direction == "right":  
            self.coord_x += 1  
      
  
  
  
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
  
    def find_empty(self):  
        """ 
        find the two empty spaces 
        """  
        x_0 = -1  
        y_0 = -1   
        x_1 = -1  
        y_1 = -1   
        for y in range(0,5):  
            for x in range(0,4):  
                if self.grid[y][x] == '.':  
                    if x_0 == -1:  
                        x_0 = x  
                        y_0 = y  
                    else:  
                        x_1 = x  
                        y_1 = y  
          
  
        for y in range(0,5):  
            for x in range(0,4):  
                if self.grid[y][x] == '.':  
                    if x_0 == x and y_0 == y:  
                        pass  
                    else:  
                        x_1 = x  
                        y_1 = y  
        return x_0, y_0, x_1, y_1  
  
  
  
  
  
  
class State:  
    """ 
    State class wrapping a Board with some extra current state information. 
    Note that State and Board are different. Board has the locations of the pieces.  
    State has a Board and some extra information that is relevant to the search:  
    heuristic function, f value, current depth and parent. 
    """  
  
    def __init__(self, board, f, depth, parent=None):  
        """ 
        :param board: The board of the state. 
        :type board: Board 
        :param f: The f value of current state. 
        :type f: int 
        :param depth: The depth of current state in the search tree. 
        :type depth: int 
        :param parent: The parent of current state. 
        :type parent: Optional[State] 
        """  
        self.board = board  
        self.f = f  
        self.depth = depth  
        self.parent = parent  
        self.id = hash(board)  # The id for breaking ties.  
  
    def __lt__(self, other):  
        return self.f < other.f  
  
  
  
  
  
  
  
  
def read_from_file(filename):  
    """ 
    Load initial board from a given file. 
 
    :param filename: The name of the given file. 
    :type filename: str 
    :return: A loaded board 
    :rtype: Board 
    """  
  
    puzzle_file = open(filename, "r")  
  
    line_index = 0  
    pieces = []  
    g_found = False  
  
    for line in puzzle_file:  
  
        for x, ch in enumerate(line):  
  
            if ch == '^': # found vertical piece  
                pieces.append(Piece(False, False, x, line_index, 'v'))  
            elif ch == '<': # found horizontal piece  
                pieces.append(Piece(False, False, x, line_index, 'h'))  
            elif ch == char_single:  
                pieces.append(Piece(False, True, x, line_index, None))  
            elif ch == char_goal:  
                if g_found == False:  
                    pieces.append(Piece(True, False, x, line_index, None))  
                    g_found = True  
        line_index += 1  
  
    puzzle_file.close()  
  
    board = Board(pieces)  
      
    return board  
  
def write_file(filename, state9):  
    """ 
    Write boards to a given file. 
 
    :param filename: The name of the given file. 
    :type filename: str 
    :return: A loaded board 
    :rtype: Board 
    """ 
    count = 0 
    sol = []  
    sol_file = open(filename, "w")  
    while state9 != None:  
        sol.append(state9)  
        state9 = state9.parent  
    sol.reverse()  
    for state in sol:  
        for i, line in enumerate(state.board.grid):  
            for ch in line:  
                sol_file.write(ch)  
            sol_file.write("\n")  
        sol_file.write("\n")
        count+=1  
    sol_file.close()
    print(str(count-1) + " moves using " + str(time.time() - start_time)+ "s \n" )  
  
  
def legal_move_check(i, board, direction):  
    x0, y0, x1, y1 = board.find_empty()  
    if board.pieces[i].is_goal: #piece is caocao  
        if board.pieces[i].coord_y == 0 and direction == "up":    
            return False    
        elif board.pieces[i].coord_y == 3 and direction == "down":    
            return False    
        elif board.pieces[i].coord_x == 0 and direction == "left":    
            return False    
        elif board.pieces[i].coord_x == 2 and direction == "right":    
            return False  
        # above is check for border of the board  
        if direction == "up":  
            e = [(board.pieces[i].coord_x, board.pieces[i].coord_y-1), (board.pieces[i].coord_x+1, board.pieces[i].coord_y-1)]  
            return (x0, y0) in e and (x1, y1) in e  
        elif direction == "down":  
            e = [(board.pieces[i].coord_x, board.pieces[i].coord_y+2), (board.pieces[i].coord_x+1, board.pieces[i].coord_y+2)]  
            return (x0, y0) in e and (x1, y1) in e  
        elif direction == "left":  
            e = [(board.pieces[i].coord_x-1, board.pieces[i].coord_y), (board.pieces[i].coord_x-1, board.pieces[i].coord_y+1)]  
            return (x0, y0) in e and (x1, y1) in e  
        elif direction == "right":  
            e = [(board.pieces[i].coord_x+2, board.pieces[i].coord_y), (board.pieces[i].coord_x+2, board.pieces[i].coord_y+1)]  
            return (x0, y0) in e and (x1, y1) in e  
    elif board.pieces[i].orientation == 'v': #piece is vertical  
        if board.pieces[i].coord_y == 0 and direction == "up":    
            return False    
        elif board.pieces[i].coord_y == 3 and direction == "down":    
            return False    
        elif board.pieces[i].coord_x == 0 and direction == "left":    
            return False    
        elif board.pieces[i].coord_x == 3 and direction == "right":    
            return False  
        # above is check for border of the board  
        if direction == "up":  
            e = [(board.pieces[i].coord_x, board.pieces[i].coord_y-1)]  
            return (x0, y0) in e or (x1, y1) in e  
        elif direction == "down":  
            e = [(board.pieces[i].coord_x, board.pieces[i].coord_y+2)]  
            return (x0, y0) in e or (x1, y1) in e  
        elif direction == "left":  
            e = [(board.pieces[i].coord_x-1, board.pieces[i].coord_y), (board.pieces[i].coord_x-1, board.pieces[i].coord_y+1)]  
            return (x0, y0) in e and (x1, y1) in e  
        elif direction == "right":  
            e = [(board.pieces[i].coord_x+1, board.pieces[i].coord_y), (board.pieces[i].coord_x+1, board.pieces[i].coord_y+1)]  
            return (x0, y0) in e and (x1, y1) in e  
    elif board.pieces[i].orientation == 'h': #piece is horizontal  
        if board.pieces[i].coord_y == 0 and direction == "up":    
            return False    
        elif board.pieces[i].coord_y == 4 and direction == "down":    
            return False    
        elif board.pieces[i].coord_x == 0 and direction == "left":    
            return False    
        elif board.pieces[i].coord_x == 2 and direction == "right":    
            return False  
        # above is check for border of the board  
        if direction == "up":  
            e = [(board.pieces[i].coord_x, board.pieces[i].coord_y-1), (board.pieces[i].coord_x+1, board.pieces[i].coord_y-1)]  
            return (x0, y0) in e and (x1, y1) in e  
        elif direction == "down":  
            e = [(board.pieces[i].coord_x, board.pieces[i].coord_y+1), (board.pieces[i].coord_x+1, board.pieces[i].coord_y+1)]  
            return (x0, y0) in e and (x1, y1) in e  
        elif direction == "left":  
            e = [(board.pieces[i].coord_x-1, board.pieces[i].coord_y)]  
            return (x0, y0) in e or (x1, y1) in e  
        elif direction == "right":  
            e = [(board.pieces[i].coord_x+2, board.pieces[i].coord_y)]  
            return (x0, y0) in e or (x1, y1) in e  
    elif board.pieces[i].is_single: # piece is a soldier  
        if board.pieces[i].coord_y == 0 and direction == "up":    
            return False    
        elif board.pieces[i].coord_y == 4 and direction == "down":    
            return False    
        elif board.pieces[i].coord_x == 0 and direction == "left":    
            return False    
        elif board.pieces[i].coord_x == 3 and direction == "right":    
            return False  
        # above is check for border of the board  
        if direction == "up":  
            e = [ (board.pieces[i].coord_x, board.pieces[i].coord_y-1)]  
            return (x0, y0) in e or (x1, y1) in e  
        elif direction == "down":  
            e = [(board.pieces[i].coord_x, board.pieces[i].coord_y+1)]  
            return (x0, y0) in e or (x1, y1) in e  
        elif direction == "left":  
            e = [(board.pieces[i].coord_x-1, board.pieces[i].coord_y)]  
            return (x0, y0) in e or (x1, y1) in e  
        elif direction == "right":  
            e = [(board.pieces[i].coord_x+1, board.pieces[i].coord_y)]  
            return (x0, y0) in e or (x1, y1) in e  
  
  
  
def display_sol(state9):  
    print("\n \n \n")  
    while state9 != None:  
        state9.board.display()  
        print("\n")  
        state9 = state9.parent  
  
def dfs(state0, filename="sol.txt"):  
    frontier = [state0]  
    visited = set()
    visited.add(grid_hashing(state0.board.grid))  
    rslt = []  
    found = False  
    while frontier != []:  
        if found:  
            break  
        state0 = frontier.pop()  
        rslt = neighbouring(visited, copy(state0))  
        for state in rslt:  
            if is_goal(state):  
                found = True  
                print("found")  
                #display_sol(state)  
                write_file(filename, state)  
                break;  
            
            frontier.append(state)  
                  
  
    # if not found:  
    #     print("not found")  
    # else:  
    #     print("end of solution")  
          
  
def manhattan(board):  
    for piece in board.pieces:  
        if piece.is_goal:  
            return abs(1 - piece.coord_x) + abs(3 - piece.coord_y)  
          
  
def astar(state0, filename="sol.txt"):  
    frontier = []  
    heapq.heapify(frontier)  
    heapq.heappush(frontier, state0)  
    visited = set()
    visited.add(grid_hashing(state0.board.grid)) 
    rslt = []  
    found = False  
    temp = heapq.heappop(frontier)  
    while temp is not None:  
        if found:  
            break  
        rslt = neighbouring(visited, copy(temp))  
        for state in rslt:  
            #add heuristic value to f  
            state.f = state.depth + manhattan(state.board)  
            if is_goal(state):  
                found = True  
                print("found")  
                #display_sol(state)  
                write_file(filename, state)  
                break;  
            #new_hash = grid_hashing(state.board.grid)
              
            heapq.heappush(frontier, state)  
            #visited.add(new_hash) 
        if not found:  
            temp = heapq.heappop(frontier)  
  
  
def copy(state0):  
    """ 
    Perform a deep copy of a given state 
    """  
    copy_pieces = []  
    for piece in state0.board.pieces:  
        copy_pieces.append(Piece(piece.is_goal, piece.is_single, piece.coord_x, piece.coord_y, piece.orientation))  
    copy_board = Board(copy_pieces)  
    copy_state = State(copy_board, state0.f, state0.depth, state0.parent)  
    return copy_state  
  
def neighbouring(visited, state0):  
    init = copy(state0)  
    moves = []  
    for j in range(5):  
        for i in range(10):  
            if legal_move_check(i, state0.board, "left"):  
                state0.board.pieces[i].move("left")  
                new_board = Board(state0.board.pieces)  
                new_state = State(new_board, state0.f+1, state0.depth+1)  
                new_state.parent = state0  
                new_hash = grid_hashing(new_board.grid)  
                if new_hash not in visited:  
                    moves.append(new_state)  
                    visited.add(new_hash)  
                    state0 = copy(init)  
                    break  
                else:  
                    state0 = copy(init)  
                      
            if legal_move_check(i, state0.board, "up"):  
                state0.board.pieces[i].move("up")  
                new_board = Board(state0.board.pieces)  
                new_state = State(new_board, state0.f+1, state0.depth+1)  
                new_state.parent = state0
                new_hash = grid_hashing(new_board.grid)  
                if new_hash not in visited:  
                    moves.append(new_state)  
                    visited.add(new_hash)  
                    state0 = copy(init)  
                    break  
                else:  
                    state0 = copy(init)  
                      
            if legal_move_check(i, state0.board, "right"):  
                state0.board.pieces[i].move("right")  
                new_board = Board(state0.board.pieces)  
                new_state = State(new_board, state0.f+1, state0.depth+1)  
                new_state.parent = state0
                new_hash = grid_hashing(new_board.grid)  
                if new_hash not in visited:  
                    moves.append(new_state)  
                    visited.add(new_hash)  
                    state0 = copy(init)  
                    break  
                else:  
                    state0 = copy(init)  
                      
            if legal_move_check(i, state0.board, "down"):  
                state0.board.pieces[i].move("down")  
                new_board = Board(state0.board.pieces)  
                new_state = State(new_board, state0.f+1, state0.depth+1)  
                new_state.parent = state0  
                new_hash = grid_hashing(new_board.grid)  
                if new_hash not in visited:  
                    moves.append(new_state)  
                    visited.add(new_hash)  
                    state0 = copy(init)  
                    break  
                else:  
                    state0 = copy(init)  
    return moves  


def grid_hashing(grid):
    temp_list = []
    for lst in grid:
        temp_list+=lst
    str0 = ' '.join(temp_list)
    return hash(str0)
      
                      
                  
  
          
          
          
  
def pruning(visited, new_state):  
    """ 
    check if the same board has reached previously, True if not 
    """  
    for state in visited:  
        if state.board.pieces == new_state.board.pieces:  
            return False  
        elif state.id == new_state.id:  
            return False  
        elif state.board.grid == new_state.board.grid:  
            return False  
        elif hash(state.board) == hash(new_state.board):  
            return False  
    return True  
  
  
  
def is_goal(state):  
    """ 
    returns True if the state is a goal state, aka caocao is at specific coord 
    """  
    for piece in state.board.pieces:  
        if piece.is_goal:  
            return piece.coord_x == 1 and piece.coord_y == 3      
  
  
  
  
  
  
  
      
  
  
if __name__ == "__main__":  
      
  
    # c = Piece(True, False, 0, 3, None)  
    # s0 = Piece(False, True, 0, 0, None)  
    # s1 = Piece(False, True, 0, 1, None)  
    # s2 = Piece(False, True, 2, 0, None)  
    # s3 = Piece(False, True, 3, 0, None)  
    # v0 = Piece(False, False, 1, 0, 'v')   
    # v1 = Piece(False, False, 3, 3, 'v')  
    # h0 = Piece(False, False, 2, 1, 'h')  
    # h1 = Piece(False, False, 2, 2, 'h')  
    # h2 = Piece(False, False, 0, 2, 'h')  
    # board1 = Board([c, s0, s1, s2, s3, v0, v1, h0, h1, h2])  
    # board1.display()  
    # print("\n")  
      
    # print(board1.find_empty())  
    # #legalmove check  
    # print(legal_move_check(4, board1, "down"))  
  
    # board2 = read_from_file("testhrd_easy1.txt")  
    # board2.display()  
    # board2.find_empty()  
  
  
    parser = argparse.ArgumentParser()  
    parser.add_argument(  
        "--inputfile",  
        type=str,  
        required=True,  
        help="The input file that contains the puzzle."  
    )  
    parser.add_argument(  
        "--outputfile",  
        type=str,  
        required=True,  
        help="The output file that contains the solution."  
    )  
    parser.add_argument(  
        "--algo",  
        type=str,  
        required=True,  
        choices=['astar', 'dfs'],  
        help="The searching algorithm."  
    )  
    args = parser.parse_args()  
    print(args.inputfile)  
    print("\n")
    print(args.outputfile) 
    print("\n") 
    print(args.algo)
    print("\n")  
    board = read_from_file(args.inputfile)
    board.display()  
    state0 = State(board, manhattan(board), 0)
    print("\n")  
    start_time = time.time()
    if args.algo == "dfs":
        dfs(state0, args.outputfile)
    elif args.algo == "astar":
        astar(state0, args.outputfile)
      
      
      
  
    #read the board from the file  
    #board = read_from_file("testhrd_hard1.txt")  
    #board = read_from_file("toy1")  
    #board.display()  
    #state0 = State(board, manhattan(board), 0)  
    #print(is_goal(state0))  
    #print("\n")  
    #dfs(state0)  
    #astar(state0)
    #visited = set()  
    #neighbouring(visited, state0)  