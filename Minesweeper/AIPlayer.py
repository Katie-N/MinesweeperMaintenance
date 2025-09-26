
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

        # Loop through each row until it gets to the second to last row. 
        # This pattern is not possible on the last row because there are no cells under the last row
       
        # Pattern 1, check by row from left wall. 
        col = 0
        for row in range(self.board.width - 1):
            if (currentBoardState[row][col] == 1) and (currentBoardState[row][col+1] == 1) and (currentBoardState[row+1][col+2] == "?"):
                self.board.reveal_square(col + 2, row + 1)
                return
        # Pattern 1, check by row from right wall. 
        col = self.board.width - 1 # - 1 because the columns are zero indexed. 
        for row in range(self.board.width - 1):
            if (currentBoardState[row][col] == 1) and (currentBoardState[row][col-1] == 1) and (currentBoardState[row+1][col-2] == "?"):
                self.board.reveal_square(col-2, row + 1)
                return

    # TODO: Implement actual AI logic for hard mode
    def make_hard_move(self):
        # Implement hard difficulty logic
        print("AI making hard move")
        self.board.reveal_square(0, 0)
