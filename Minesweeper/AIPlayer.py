
from MinesweeperBoard import Minesweeper as MinesweeperBoard
import random

class AIPlayer:
    def __init__(self, board: MinesweeperBoard, difficulty: str):
        self.board = board
        self.difficulty = difficulty
    
    # This function will make a move based on the selected difficulty level
    # It returns the (col, row) of the move made. 
    # This means its important that every move function returns those values.
    def make_move(self):
        if self.difficulty == "Easy":
            return self.make_easy_move()
        elif self.difficulty == "Medium":
            return self.make_medium_move()
        elif self.difficulty == "Hard":
            return self.make_hard_move()
    
    def getAdjacentValues(self, row, col):
        currentBoardState = self.board.get_display_board()
        try:
            left = currentBoardState[row][col - 1] if (col - 1 >= 0) else None
        except IndexError:
            left = None
        try:
            top = currentBoardState[row-1][col] if (row - 1 >= 0) else None
        except IndexError:
            top = None
        try:
            topleft = currentBoardState[row-1][col - 1] if (col - 1 >= 0 and row - 1 >= 0) else None
        except IndexError:
            topleft = None
        try:
            topright = currentBoardState[row-1][col+1] if (row - 1 >= 0 and col + 1 < self.board.width) else None
        except IndexError:
            topright = None
        try:
            right = currentBoardState[row][col+1] if (col + 1 < self.board.width) else None
        except IndexError:
            right = None
        try:
            bottomright = currentBoardState[row+1][col+1] if (row + 1 < self.board.height and col + 1 < self.board.width) else None
        except IndexError:
            bottomright = None
        try:
            bottom = currentBoardState[row+1][col] if (row + 1 < self.board.height) else None
        except IndexError:
            bottom = None
        try:
            bottomleft = currentBoardState[row+1][col-1] if (col - 1 >= 0 and row + 1 < self.board.height) else None
        except IndexError:
            bottomleft = None

        return left, topleft, top, topright, right, bottomright, bottom, bottomleft

    # NOTE: Their logic takes the column first then the row. No idea why since it is usually row then column. Don't get tripped up by this. 
    # To uncover a cell just do self.board.reveal_square(column, row) 
    # To flag a cell just do self.toggle_flag(column, row)

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
    
    # This function will make a random move on the board
    def make_easy_move(self):
        print("AI making easy move")

        # Randomly selects a cell to uncover
        (x, y) = (random.randint(0, self.board.width - 1), random.randint(0, self.board.height - 1))
        # Keeps picking random cells until an unrevealed cell is found
        while self.board.get_display_board()[y][x] != "?" and self.board.get_display_board()[y][x] != "F":
            (x, y) = (random.randint(0, self.board.width - 1), random.randint(0, self.board.height - 1))

        # Uncovers the selected cell
        self.board.reveal_square(x, y)
        return x, y

    # This function will make a strategic move based on the same information the player has using various minesweeper strategies
    # It uses logic by referencing defined patterns it finds on the board and will either flag or uncover a cell each time this function is called. 
    def make_medium_move(self):
        # Implement medium difficulty logic
        print("AI making medium move")
        # If no safe moves, make random move
        # Otherwise, make a strategic move
        # Since the medium AI should not have any special knowledge we will use the display board instead of the regular board. 
        currentBoardState = self.board.get_display_board()

        # Key: 
        #   * = any value
        #   Number = revealed square with that number
        #   ? = unrevealed square
        #   F = flagged square
        #   | = wall of the board
        #   X = Uncover the cell

        # Pattern: | 1 1 *
        #          | ? ? ?
        # Safe move: 
        #          | 1 1 *
        #          | ? ? X
        # Logic: Along a wall, if 2 adjacent revealed squares show a 1 and there are 3 covered cells below the squares, then the third square can be safely uncovered. 
        # This logic also goes for when the pattern is rotated in any direction.

        # Pattern 1, check by row from left wall. 
        col = 0
        for row in range(self.board.height):
            if (currentBoardState[row][col] == 1) and (currentBoardState[row][col+1] == 1):
                if ((row+1 < self.board.height) and currentBoardState[row+1][col+2] == "?"):
                    self.board.reveal_square(col + 2, row+1)
                    return col + 2, row+1
                elif ((row-1 >= 0) and currentBoardState[row-1][col+2] == "?"):
                    self.board.reveal_square(col + 2, row-1)
                    return col + 2, row-1
           
        # Pattern 1, check by row from right wall. 
        col = self.board.width - 1 # - 1 because the columns are zero indexed. 
        for row in range(self.board.height):
            if (currentBoardState[row][col] == 1) and (currentBoardState[row][col-1] == 1):
                if ((row+1 < self.board.height) and currentBoardState[row+1][col-2] == "?"):
                    self.board.reveal_square(col-2, row+1)
                    return col-2, row+1
                elif ((row-1 >= 0) and currentBoardState[row-1][col-2] == "?"):
                    self.board.reveal_square(col-2, row-1)
                    return col-2, row-1
                
        # Pattern 1, check by column from top wall. 
        row = 0 # Lock to the top wall
        for col in range(self.board.width):
            if (currentBoardState[row][col] == 1) and (currentBoardState[row+1][col] == 1):
                if ((col + 1 < self.board.width) and currentBoardState[row+2][col+1] == "?"):
                    self.board.reveal_square(col+1, row+2)
                    return col+1, row+2
                elif ((col - 1 < self.board.width) and currentBoardState[row+2][col-1] == "?"):
                    self.board.reveal_square(col-1, row+2)
                    return col-1, row+2
            
        # Pattern 1, check by column from bottom wall.
        row = self.board.height - 1 # Lock to the bottom wall
        for col in range(self.board.width):
            if (currentBoardState[row][col] == 1) and (currentBoardState[row-1][col] == 1):
                if ((col+1 < self.board.width) and currentBoardState[row-2][col+1] == "?"):
                    self.board.reveal_square(col+1, row-2)
                    return col+1, row-2
                elif ((col-1 < self.board.width) and currentBoardState[row-2][col-1] == "?"):
                    self.board.reveal_square(col-1, row-2)
                    return col-1, row-2

        # Pattern 2, If there is a cell with 3 '1's in around one of its corners, then it must be a mine and should be flagged. 
        # 1 1
        # 1 ?
        # Safe Move:
        # 1 1
        # 1 F
        for row in range(self.board.height):
            for col in range(self.board.width):
                currentCell = currentBoardState[row][col]
                # For every covered cell, check if it has a corner of 1s
                if currentCell == "?":
                    left, topleft, top, topright, right, bottomright, bottom, bottomleft = self.getAdjacentValues(row,col)
                    
                    # There are 4 corners to check
                    # left, top left, top
                    if left == 1 and topleft == 1 and top == 1 and (self.getAdjacentValues(row-1,col-1).count('?') + self.getAdjacentValues(row-1,col-1).count('F')) == 1:
                        self.board.toggle_flag(col, row)
                        return col, row
                    # top, top right, right
                    if top == 1 and topright == 1 and right == 1 and (self.getAdjacentValues(row-1,col+1).count('?') + self.getAdjacentValues(row-1,col+1).count('F')) == 1:
                        self.board.toggle_flag(col, row)
                        return col, row
                    # right, bottom right, bottom
                    if right == 1 and bottomright == 1 and bottom == 1 and (self.getAdjacentValues(row+1,col+1).count('?') + self.getAdjacentValues(row+1,col+1).count('F')) == 1:
                        self.board.toggle_flag(col, row)
                        return col, row
                    # bottom, bottom left, left
                    if bottom == 1 and bottomleft == 1 and left == 1 and (self.getAdjacentValues(row+1,col-1).count('?') + self.getAdjacentValues(row+1,col-1).count('F'))== 1:
                        self.board.toggle_flag(col, row)
                        return col, row

        # Pattern 3, similar to pattern 1 but for a mine. If there are 2 consecutive 2's off of a wall with uncovered cells on one side and covered cells on the other side, then the 2 covered cells can be flagged and the third cell can be uncovered.
        # | * *
        # | 2 2
        # | ? ? *
        # Safe Move:
        # | * *
        # | 2 2
        # | F F X

        # Pattern 4, if the number of flags surrounding an uncovered cell == the number of that cell, then all unflagged covered cells around that cell can be safely uncovered. 
        # This pattern will fail if the user incorrectly flags a non-mine however this is not a bug but a feature. 
        # Examine each cell in the board
        # Loop through each row in the board
        for row in range(self.board.height):
            # Loop through each column in the board
            for col in range(self.board.width):
                # This is the current cell being examined. 
                cellValue = currentBoardState[row][col]
                # If the current cell is a non-zero number, check if the surrounding flags add up to the number.
                if type(cellValue) is int and cellValue > 0:
                    coveredCells = []
                    numFlags = 0
                    # Loop through each cell in the 3x3 grid surrounding the current cell
                    for i in range(row-1, row+2):
                        for j in range(col-1, col+2):
                            # Make sure i and j are within the bounds of the board before trying to access those indices
                            if i >= 0 and i < self.board.height and j >= 0 and j < self.board.width:
                                if currentBoardState[i][j] == "F":
                                    numFlags += 1
                                elif currentBoardState[i][j] == "?":
                                    coveredCells.append((i,j))
                    
                    # If the number of flags in adjacent cells equals the cell value then we should uncover one of the adjacent covered cells
                    # (Because all mine cells have been identified with flags.)
                    if (numFlags == cellValue):
                        # Just pick the first covered cell in the list to uncover.
                        for cell in coveredCells:
                            self.board.reveal_square(cell[1], cell[0])
                            return cell[1], cell[0]
                    
        # Pattern 5, similar to pattern 1 but for mines. If there is a wall with a 1 then a 2 off the wall, the third cell in the adjacent row/column is a mine and should be flagged.
        # TODO: Either come back to pattern 5 or scrap it but right now it is not functioning properly. It needs a check so that the entire row opposite is clear, not just the opposite cell. 
        # Ex. | F * *
        #     | 1 2 F
        #     | ? ? ? <- This cell got flagged

        # Pattern:
        # | * * *
        # | 1 2
        # | ? ? ?
        # Safe Move:
        # | * * *
        # | 1 2
        # | ? ? F
        # Pattern 5, check by row from left wall. 
        # col = 0
        # for row in range(self.board.height):
        #     if (currentBoardState[row][col] == 1) and (currentBoardState[row][col+1] == 2):
        #         # If the lower right cell is covered
        #         if ((row+1 < self.board.height) and (currentBoardState[row+1][col+2] == "?")):
        #             # The opposite cell needs to be either non-existent (as in off the board) or uncovered for this pattern to be matched. 
        #             # If the upper right cell is uncovered or off the board then we can safely flag the lower right cell.
        #             if ((row-1 < 0) or (currentBoardState[row-1][col+2] != "?")):
        #                 print("Flagging mine at:", col + 2, row+1)
        #                 self.board.toggle_flag(col + 2, row+1)
        #                 return
        #         # If the upper right cell is covered
        #         elif ((row-1 >= 0) and currentBoardState[row-1][col+2] == "?"):
        #             # If the lower right cell is uncovered or off the board then we can safely flag the lower right cell.
        #             if ((row+1 >= self.board.height) or (currentBoardState[row+1][col+2] != "?")):
        #                 print("Flagging mine at:", col + 2, row-1)
        #                 self.board.toggle_flag(col + 2, row-1)
        #                 return
                   
        # Pattern 6: If the value of an uncovered cell equals the sum of the covered adjacent cells, then they should be flagged.
        for row in range(self.board.height):
            for col in range(self.board.width):
                cellValue = currentBoardState[row][col]
                # Skip covered cells
                if cellValue == "?" or cellValue == "F":
                    continue

                adjCells = self.getAdjacentValues(row, col)
                print(adjCells)
                left, topleft, top, topright, right, bottomright, bottom, bottomleft = self.getAdjacentValues(row, col)
                if adjCells.count("?") + adjCells.count("F") == cellValue:
                    if left == "?":
                        self.board.toggle_flag(col-1, row)
                        return col - 1, row
                    if topleft == "?":
                        self.board.toggle_flag(col-1, row-1)
                        return col - 1, row-1
                    if top == "?":
                        self.board.toggle_flag(col, row-1)
                        return col, row-1
                    if topright == "?":
                        self.board.toggle_flag(col+1, row-1)
                        return col + 1, row-1
                    if right == "?":
                        self.board.toggle_flag(col+1, row)
                        return col + 1, row
                    if bottomright == "?":
                        self.board.toggle_flag(col+1, row+1)
                        return col + 1, row+1
                    if bottom == "?":
                        self.board.toggle_flag(col, row+1)
                        return col, row + 1

        print("No moves. Making random move")
        return self.make_easy_move()

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
                return x, y
            
        #if there are cells it remembers have to be mines, flag them
        while self.mineFlags:
            x, y, = self.mineFlags.pop()
            if currentBoardState[y][x] == "?":
                # print(f"Remembered mine flagged at ({x}, {y})")
                self.board.toggle_flag(x, y)
                return x,y
        
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
                return x, y
            
        if newMineFlags:
            x, y = newMineFlags.pop()
            self.safeMoves.extend(newSafeMoves)
            self.mineFlags.extend(newMineFlags)
            if currentBoardState[y][x] == "?":
                # print(f"Flagging a known mine at ({x}, {y})")
                self.board.toggle_flag(x, y)
                return x,y

        #if there truly is nothing it can deduce, then it'll look at the uncovered cells (within heigth and width range)
        choices = [(x, y) for y in range(self.board.height) for x in range(self.board.width) if currentBoardState[y][x]== "?"]
        #if there is a cell it can chooose from that
        if choices:
            #reveal a random one
            x, y = random.choice(choices)
            # print(f"No moves to deduce. Uncovering ({x}, {y})")
            self.board.reveal_square(x, y)
            return x,y
