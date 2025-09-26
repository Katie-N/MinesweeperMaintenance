
from MinesweeperBoard import Minesweeper as MinesweeperBoard

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
    
    # NOTE: Their logic takes the column first then the row. No idea why since it is usually row then column. Don't get tripped up by this. 
    # To uncover a cell just do self.board.reveal_square(column, row) 
    # To flag a cell just do self.toggle_flag(column, row)

    # TODO: Implement actual AI logic for easy mode
    def make_easy_move(self):
        # Make random move
        print("AI making easy move")
        self.board.reveal_square(0, 0)

    # TODO: Implement actual AI logic for medium mode
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
                    return
                elif ((row-1 >= 0) and currentBoardState[row-1][col+2] == "?"):
                    self.board.reveal_square(col + 2, row-1)
                    return
           
        # Pattern 1, check by row from right wall. 
        col = self.board.width - 1 # - 1 because the columns are zero indexed. 
        for row in range(self.board.height):
            if (currentBoardState[row][col] == 1) and (currentBoardState[row][col-1] == 1):
                if ((row+1 < self.board.height) and currentBoardState[row+1][col-2] == "?"):
                    self.board.reveal_square(col-2, row+1)
                    return
                elif ((row-1 >= 0) and currentBoardState[row-1][col-2] == "?"):
                    self.board.reveal_square(col-2, row-1)
                    return
                
        # Pattern 1, check by column from top wall. 
        row = 0 # Lock to the top wall
        for col in range(self.board.width):
            if (currentBoardState[row][col] == 1) and (currentBoardState[row+1][col] == 1):
                if ((col + 1 < self.board.width) and currentBoardState[row+2][col+1] == "?"):
                    self.board.reveal_square(col+1, row+2)
                    return
                elif ((col - 1 < self.board.width) and currentBoardState[row+2][col-1] == "?"):
                    self.board.reveal_square(col-1, row+2)
                    return
            
        # Pattern 1, check by column from bottom wall.
        row = self.board.height - 1 # Lock to the bottom wall
        for col in range(self.board.width):
            if (currentBoardState[row][col] == 1) and (currentBoardState[row-1][col] == 1):
                if ((col+1 < self.board.width) and currentBoardState[row-2][col+1] == "?"):
                    self.board.reveal_square(col+1, row-2)
                    return
                elif ((col-1 < self.board.width) and currentBoardState[row-2][col-1] == "?"):
                    self.board.reveal_square(col-1, row-2)
                    return

        # Pattern 2, If there is a cell with 3 '1's in around one of its corners, then it must be a mine and should be flagged. 
        # 1 1
        # 1 ?
        # Safe Move:
        # 1 1
        # 1 F

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
                            return
                    
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
                   
        print("No moves. Making random move")

    # TODO: Implement actual AI logic for hard mode
    def make_hard_move(self):
        # Implement hard difficulty logic
        print("AI making hard move")
        self.board.reveal_square(0, 0)
