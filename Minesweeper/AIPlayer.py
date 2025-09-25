
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
    
    # To uncover a cell just do self.board.reveal_square(x, y) 
    # To flag a cell just do self.toggle_flag(x,y)

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

    # TODO: Implement actual AI logic for hard mode
    def make_hard_move(self):
        # Implement hard difficulty logic
        print("AI making hard move")
        self.board.reveal_square(0, 0)
