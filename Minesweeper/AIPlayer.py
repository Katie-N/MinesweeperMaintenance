
from MinesweeperBoard import Minesweeper as MinesweeperBoard
import random

class AIPlayer:
    def __init__(self, board: MinesweeperBoard, difficulty: str):
        self.board = board
        self.difficulty = difficulty
    
    def make_move(self):
        if self.difficulty == "Easy":
            self.make_easy_move()
        elif self.difficulty == "Medium":
            self.make_medium_move()
        elif self.difficulty == "Hard":
            self.make_hard_move()
    
    # To uncover a cell just do self.board.reveal_square(x, y) 
    # To flag a cell just do self.toggle_flag(x,y)

    #only used by hard "ai"
    #different from getAdjacentValues, it returns the coordinates and its value, not only the values
    #decided to make it seperate, as to not have to change the medium ai patterns since the return values/structure is different
    def getAdjacentCells(self, row, col):
        neighbors = []
        currentBoardState = self.board.get_display_board()
        #loop over the adjacent rows (-1 to the left, +1 to the right)
        for rowOffset in (-1, 0, 1):
            #same thing for the cols
            for colOffset in (-1, 0, 1):
                #skip 0, 0 because thats just the center cell itself
                if rowOffset == 0 and colOffset == 0:
                    continue
                #get the neighbor row, col
                neigborRow, neighborCol = row + rowOffset, col + colOffset
                #make sure the neighbor is inside the board
                if 0 <= neigborRow < self.board.height and 0 <=neighborCol < self.board.width:
                    #add the neighbor's coordinates and what value it has ("?", "F", or a num)
                    neighbors.append(((neigborRow, neighborCol), currentBoardState[neigborRow][neighborCol]))
        return neighbors
    
    # TODO: Implement actual AI logic for easy mode
    def make_easy_move(self):
        # Make random move
        print("AI making easy move")
        self.board.reveal_square(0, 0)

    # TODO: Implement actual AI logic for easy mode
    def make_medium_move(self):
        # Implement medium difficulty logic
        print("AI making medium move")
        self.board.reveal_square(0, 0)

    def make_hard_move(self):
        print("AI making hard move")

        #the ""ai"" ain't actually cheating so it just has the display board too
        currentBoardState = self.board.get_display_board()

        #it'll remember things though
        #init arrays if they don't exist yet
        #can i just put this in when initting the class? yes but i just wanted it to be created only when hard mode is called
        if not hasattr(self, "safeMoves"):
            self.safeMoves = []
        if not hasattr(self, "mineFlags"):
            self.mineFlags = []

        #if there are safe cells it 'remembers', click those first
        while self.safeMoves:
            #since its col, row not row, col
            x, y = self.safeMoves.pop()
            #if its an unrevealed cell
            if currentBoardState[y][x] == "?":
                # print(f"Remembered safe move at ({x}, {y})")
                #click it
                self.board.reveal_square(x, y)
                return
            
        #if there are cells it remembers have to be mines, flag them
        while self.mineFlags:
            x, y, = self.mineFlags.pop()
            if currentBoardState[y][x] == "?":
                # print(f"Remembered mine flagged at ({x}, {y})")
                self.board.toggle_flag(x, y)
                return
        
        newSafeMoves = []
        newMineFlags = []
        #goes through board and figures out if there are cells it should remember
        for x in range(self.board.height):
            for y in range(self.board.width):
                #gets the value of the cell its looking at
                value = currentBoardState[x][y]
                #if the cell is covered or flagged (aka not an int) skip it, since we can't figure out info from whatever number is hidden
                if not isinstance(value, int):
                    continue
                #how many mines are around the current cell
                adjacentMinesNum = value
                #get the neighbors
                neighbors = self.getAdjacentCells(x, y)
                coveredNeighbors = [(col, row) for (row, col), v in neighbors if v == "?"]
                flaggedNeighbors = [(col, row) for (row, col), v in neighbors if v == "F"]
                #if the adjacentMinesNum == flagged Neighbors, then that means the other adjacent covered cells are all safe
                #                                               that is if there are covered neighbors
                if adjacentMinesNum == len(flaggedNeighbors) and coveredNeighbors:
                    # print(f"For cell ({x}, {y}), the neighbors:\n{coveredNeighbors}\nare safe")
                    #instead of doing a for loop to append each elem
                    newSafeMoves.extend(coveredNeighbors)
                #if the adjacentMinesNum == flaggedNeighbors + coveredNeighbords, then that means all the covered cells are mine
                if adjacentMinesNum == len(flaggedNeighbors) + len(coveredNeighbors) and coveredNeighbors:
                    # print(f"For cell ({x}, {y}), the neighbors:\n{coveredNeighbors}\nare mines")
                    newMineFlags.extend(coveredNeighbors)
        
        #Play what it deduced
        if newSafeMoves:
            #pick a cell and remove it from the array
            x, y = newSafeMoves.pop()
            #add the new  moves to the og arrays
            #to be used in a later turn
            self.safeMoves.extend(newSafeMoves)
            self.mineFlags.extend(newMineFlags)
            if currentBoardState[y][x] == "?":
                # print(f"Playing a save move at ({x}, {y})")
                self.board.reveal_square(x, y)
                return
            
        if newMineFlags:
            x, y = newMineFlags.pop()
            self.safeMoves.extend(newSafeMoves)
            self.mineFlags.extend(newMineFlags)
            if currentBoardState[y][x] == "?":
                # print(f"Flagging a known mine at ({x}, {y})")
                self.board.toggle_flag(x, y)
                return

        #if there truly is nothing it can deduce, then it'll look at the uncovered cells (within heigth and width range)
        choices = [(x, y) for y in range(self.board.height) for x in range(self.board.width) if currentBoardState[y][x]== "?"]
        #if there is a cell it can chooose from that
        if choices:
            #reveal a random one
            x, y = random.choice(choices)
            # print(f"No moves to deduce. Uncovering ({x}, {y})")
            self.board.reveal_square(x, y)
