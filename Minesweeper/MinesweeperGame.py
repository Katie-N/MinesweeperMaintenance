"""
Module: MinesweeperGame
Class: Game
Description: Organizes and runs the Minesweeper game using Pygame.
            Title screen, gameplay loop, rendering, and input handling.
Inputs: User interaction via GUI.
Outputs: Game window with interactive Minesweeper board.
External Sources: None
Authors: Kiara [Sam] Grimsley, Reeny Huang, Lauren D'Souza, Audrey Pan, Ella Nguyen, Hart Nurnberg
Maintainers: Katie Nordberg, Kundana Dongala, Vivian Lara, Christina Sorensen, and Navya Nittala
Created: September 19, 2025 (original prototype August 25, 2025)
Last Modified: September 19, 2025
"""

import os
import pygame as pg
import pygame_textinput as textinput
from MinesweeperBoard import Minesweeper
from AIPlayer import AIPlayer

# Board layout (fixed 10x10)
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

# Window size limit
MIN_WINDOW = (550, 550)

# Paths for assets
BASE_DIR = os.path.dirname(__file__)
FLAG_PATH = os.path.join(BASE_DIR, "Assets", "flag.png")
MINE_PATH = os.path.join(BASE_DIR, "Assets", "skull.png")
CURSOR_PATH = os.path.join(BASE_DIR, "Assets", "cursor.png")
FONT_PATH = os.path.join(BASE_DIR, "Assets", "pixelfont.ttf")

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_LINE = (255, 255, 255)
HIDDEN = (247, 225, 215)
REVEALED_EMPTY = (222, 219, 210)
REVEALED_NUMBER = (176, 196, 177)
MINE_RED = (219, 110, 110)
BACKGROUND = (74, 87, 89)
TITLE_TEXT = (240, 228, 220)
GENERAL_TEXT = (176, 196, 177)
TRANSPARENT_RED = (255, 155, 155, 180)
TRANSPARENT_GREEN = (155, 255, 155, 200)

# Maintenance Note: Added Button class for mode selection and difficulty selection buttons
# This class makes a button in pygame that will automatically trigger an event if it is clicked on, and will change colors when hovered over.
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pg.font.Font(FONT_PATH, 20) # You can load a custom font here

    def draw(self, surface):
        # Change color on hover
        if self.rect.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(surface, self.hover_color, self.rect)
        else:
            pg.draw.rect(surface, self.color, self.rect)

        # Render text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True # Button was clicked
        return False

class Game:
    def __init__(self):
        """Initialize the game."""
        self.minesweeper = None
        self.quit = False
        self.start_ticks = None  # Set when the game actually starts
        self.end_time = None     # Frozen final time
        self.last_config = None  
        self.cursor_img = None   
        self.flag_img = None    
        self.mine_img = None     
        pg.init()

    def start_game(self, width: int, height: int, num_mines: int, mode: str, difficulty: str):
        """Start a new minesweeper board with given width, height, and num_mines."""
        self.minesweeper = Minesweeper(width, height, num_mines, mode, difficulty)
        self.start_ticks = pg.time.get_ticks()  # milliseconds since pg.init()
        self.end_time = None
        self.last_config = {           
        "width": width,
        "height": height,
        "num_mines": num_mines,
        "mode": mode,
        "difficulty": difficulty
    }
    def _reset_with_same_config(self): 
        """Reset the game with the same configuration as last time. Returns whose turn it is and AI delay"""         
        cfg = self.last_config
        if not cfg:
            return "human", None
        self.start_game(cfg["width"], cfg["height"], cfg["num_mines"], cfg["mode"], cfg["difficulty"])
        if cfg["mode"] == "Auto":
            return "AI", pg.time.get_ticks() + 1000  # match AI delay
        return "human", None


    def exit_game(self):
        """Perform any game cleanup here (if needed), then quit()."""
        pg.mouse.set_visible(True)
        pg.quit()

    def play_minesweeper():
        """Static method to play Minesweeper."""
        game = Game()
        game.run()

    def mouse_to_grid(self, mx: int, my: int, grid_x0, grid_y0, cell_size, grid_width, grid_height):
        """Convert mouse pixel coordinates (mx, my) to grid coordinates (gx, gy), or None if click outside of board"""
        if not (grid_x0 <= mx < grid_x0 + cell_size * grid_width # within grid x
                and grid_y0 <= my < grid_y0 + cell_size * grid_height): # within grid y
            return None # Clicked outside grid area
        gx = (mx - grid_x0) // cell_size
        gy = (my - grid_y0) // cell_size
        return int(gx), int(gy)

    def _clamp_size(self, w, h):
        """Clamp window size to minimum dimensions."""
        min_w, min_h = MIN_WINDOW
        w = max(min_w, w)
        h = max(min_h, h)
        return w, h


    def run(self):
        """Main game loop. Title screen followed by game."""
        screen = pg.display.set_mode((600, 600), pg.RESIZABLE)
        clock = pg.time.Clock()
        HIGHLIGHT_COLOR = (0, 0, 0)  # Gold for AI highlight
        highlight_duration = 500  # ms
        ai_highlight_cell = None
        ai_highlight_time = None
        goto_play_again_screen = False
        play_again_at = None                 

        if self.last_config and self.last_config["mode"] == "Auto":  # If last game was Auto, AI starts first
            turn = "AI"
            timeAICanMove = pg.time.get_ticks() + AI_DELAY


        # Load assets, with defaults if loading fails
        try:
            font = pg.font.Font(FONT_PATH, 24)
            title_font = pg.font.Font(FONT_PATH, 30)
        except Exception as e:
            print("Custom font failed to load:", e)
            font = pg.font.SysFont(None, 24)
            title_font = pg.font.SysFont(None, 30)
        try:
            self.cursor_img = pg.image.load(CURSOR_PATH).convert_alpha()
            pg.mouse.set_visible(False) # Hide system cursor, use custom
        except Exception as e:
            print("Cursor image failed to load:", e)
            self.cursor_img = None
            pg.mouse.set_visible(True) # Show system cursor if custom fails
        try:
            self.flag_img = pg.image.load(FLAG_PATH).convert_alpha()
        except Exception as e:
            print("Flag image failed to load:", e)
            self.flag_img = None
        try:
            self.mine_img = pg.image.load(MINE_PATH).convert_alpha()
        except Exception as e:
            print("Mine image failed to load:", e)
            self.mine_img = None


        # Cap mines at 20 as per requirements. Validator restricts input to 2 digits, 0-20
        mines_input = textinput.TextInputVisualizer(manager=textinput.TextInputManager(validator=lambda x: (x.isdigit() and int(x) <= 20 and len(x) < 3) or x == ''),
                                                    font_object=font,
                                                    font_color=WHITE,
                                                    cursor_color=WHITE
                                                    )
        mode = None  # Game mode selected by player. Either "Auto", "Interactive", or "Solo"
        difficulty = None  # Difficulty selected by player. Either "Easy", "Medium", or "Hard"
        turn = "human"  # Track whose turn it is, either "human" or "AI"
        AI_DELAY = 1000  # milliseconds delay for AI moves

        # Title screen loop
        while not self.minesweeper and not self.quit:
            screen.fill(BACKGROUND)
            pg.display.set_caption("Minesweeper -- Title Screen")

            # Responsive layout variables
            w, h = screen.get_size()
            x_center = w // 2
            title_margin = h * 0.3
            mine_text_margin = title_margin + h*0.1
            text_input_margin = mine_text_margin + h*0.1
            hint_margin = text_input_margin + h*0.1

            # Render title text centered at top
            title_text = title_font.render("Welcome to Minesweeper", True, TITLE_TEXT)
            title_text_rect = title_text.get_rect(center=(x_center, title_margin))
            screen.blit(title_text, title_text_rect)

            # Render text centered below title
            mines_text = font.render("Enter Mine Count (10-20): ", True, GENERAL_TEXT)
            mines_text_rect = mines_text.get_rect(center=(x_center, mine_text_margin))
            screen.blit(mines_text, mines_text_rect)

            # Create buttons for each mode
            # Define colors
            button_color = (170, 147, 204)
            button_hover_color = (131, 106, 168)
            text_color = (255, 255, 255)

            # The row of buttons should be underneath the rest of the text
            row_of_modes_y = hint_margin + h*0.1 

            # Create buttons for each mode
            def drawModeButtons(selected_mode = None):
                current_button_color = button_color
                if selected_mode == "Auto":
                    # Color it with the hover color because it is selected
                    current_button_color = button_hover_color
                auto_button = Button(0, row_of_modes_y, int(w//3), 50, "Auto", current_button_color, button_hover_color, text_color)
                # Reset to original color
                current_button_color = button_color

                if selected_mode == "Interactive":
                    # Color it with the hover color because it is selected
                    current_button_color = button_hover_color
                interactive_button = Button(int(w//3), row_of_modes_y, int(w//3), 50, "Interactive", current_button_color, button_hover_color, text_color)
                # Reset to original color
                current_button_color = button_color

                if selected_mode == "Solo":
                    # Color it with the hover color because it is selected
                    current_button_color = button_hover_color
                solo_button = Button(2 * int(w//3), row_of_modes_y, int(w//3), 50, "Solo", current_button_color, button_hover_color, text_color)

                auto_button.draw(screen) # Draw the button
                interactive_button.draw(screen) # Draw the button
                solo_button.draw(screen) # Draw the button

                # Return callbacks to the buttons so their events can be handled
                return auto_button, interactive_button, solo_button 
            
            # Make sure the buttons are defined here, not just drawn, so events can be handled.
            auto_button, interactive_button, solo_button = drawModeButtons(mode)

            # Create buttons for each difficulty (Easy/Medium/Hard)
            # The row of buttons should be underneath the rest of the text
            row_of_difficulties_y = row_of_modes_y + h*0.1 

            def drawDifficultyButtons(selected_difficulty = None):
                current_button_color = button_color
                if selected_difficulty == "Easy":
                    # Color it with the hover color because it is selected
                    current_button_color = button_hover_color
                easy_button = Button(0, row_of_difficulties_y, int(w//3), 50, "Easy", current_button_color, button_hover_color, text_color)
                # Reset to original color
                current_button_color = button_color

                if selected_difficulty == "Medium":
                    # Color it with the hover color because it is selected
                    current_button_color = button_hover_color
                medium_button = Button(int(w//3), row_of_difficulties_y, int(w//3), 50, "Medium", current_button_color, button_hover_color, text_color)
                # Reset to original color
                current_button_color = button_color

                if selected_difficulty == "Hard":
                    # Color it with the hover color because it is selected
                    current_button_color = button_hover_color
                hard_button = Button(2 * int(w//3), row_of_difficulties_y, int(w//3), 50, "Hard", current_button_color, button_hover_color, text_color)

                easy_button.draw(screen) # Draw the button
                medium_button.draw(screen) # Draw the button
                hard_button.draw(screen) # Draw the button

                # Return callbacks to the buttons so their events can be handled
                return easy_button, medium_button, hard_button 
            
            # Only draw the difficulty buttons if AI will be playing (which is only when on Interactive or Auto mode)
            if mode == "Interactive" or mode == "Auto":
                # Make sure the buttons are defined here, not just drawn, so events can be handled.
                easy_button, medium_button, hard_button = drawDifficultyButtons(difficulty)
            else:
                easy_button = medium_button = hard_button = None
            
            # reset_btn = Button(10, 10, 110, 36, "Reset", (110, 110, 130), (140, 140, 170), WHITE)

            # Updates mine and render mine-count input field
            events = pg.event.get()
            mines_input.update(events)
            mines_input_rect = mines_input.surface.get_rect(center=(x_center, text_input_margin))
            screen.blit(mines_input.surface, mines_input_rect)

            # Render hint text
            hint_text = font.render("Press Enter to Start", True, (GENERAL_TEXT))
            hint_text_rect = hint_text.get_rect(center=(x_center, hint_margin))
            screen.blit(hint_text, hint_text_rect)

            # Handle key presses and screen resize
            for event in events:
                if event.type == pg.QUIT:
                    self.quit = True
                    break
                elif event.type == pg.VIDEORESIZE:
                    new_w, new_h = self._clamp_size(event.w, event.h)
                    cur_w, cur_h = screen.get_size()
                    if (new_w, new_h) != (cur_w, cur_h):
                        screen = pg.display.set_mode((new_w, new_h), pg.RESIZABLE)
                elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN: # Return/enter key
                    # Start game if mine count provided, mine count is within 10-20 range
                    # Maintenance Note: added check to ensure that the mode and difficulty are selected before starting the game
                    if (mines_input.value and 10 <= int(mines_input.value) <= 20 and mode in ["Auto", "Interactive", "Solo"]):
                        if ((mode == "Interactive" or mode == "Auto") and difficulty in ["Easy", "Medium", "Hard"]) or (mode == "Solo"):
                            num_mines = int(mines_input.value)
                            self.start_game(BOARD_WIDTH, BOARD_HEIGHT, num_mines, mode, difficulty)
                elif event.type == pg.MOUSEBUTTONDOWN and self.minesweeper:
                    # If game finished, capture Yes/No before board clicks
                    if self.minesweeper.is_game_over() or self.minesweeper.is_game_won():  
                        if yes_btn.handle_event(event):                                      
                            turn, timeAICanMove = self._reset_with_same_config()        
                            ai_highlight_cell = None                                     
                            ai_highlight_time = None                                      
                            continue                                                       
                        elif no_btn.handle_event(event):                                      
                            self.quit = True                                              
                            break                                                       
                elif auto_button.handle_event(event):
                    mode = "Auto"
                    print("Auto was selected")
                    drawModeButtons("Auto")
                elif interactive_button.handle_event(event):
                    mode = "Interactive"
                    print("Interactive was selected")
                    drawModeButtons("Interactive")
                elif solo_button.handle_event(event):
                    mode = "Solo"
                    print("Solo was selected")
                    drawModeButtons("Solo")
                elif (mode == "Interactive" or mode == "Auto") and easy_button.handle_event(event):
                    difficulty = "Easy"
                    print("Easy was selected")
                    drawModeButtons("Easy")
                elif (mode == "Interactive" or mode == "Auto") and medium_button.handle_event(event):
                    difficulty = "Medium"
                    print("Medium was selected")
                    drawModeButtons("Medium")
                elif (mode == "Interactive" or mode == "Auto") and hard_button.handle_event(event):
                    difficulty = "Hard"
                    print("Hard was selected")
                    drawModeButtons("Hard")
                # elif reset_btn.handle_event(event):    
                #     if self.last_config:              
                #         turn, timeAICanMove = self._reset_with_same_config()  
                #         ai_highlight_cell = None       
                #         ai_highlight_time = None       

            # Custom cursor
            if self.cursor_img is not None:
                mx, my = pg.mouse.get_pos()
                screen.blit(self.cursor_img, (mx, my))
            
            # reset_btn.draw(screen)

            pg.display.update()
            clock.tick(60)

        # Before entering gameplay loop, set initial turn and AI move timer for the autosolver mode
        if mode == "Auto":
            turn = "AI"  # AI starts first in Auto mode
            timeAICanMove = pg.time.get_ticks() + AI_DELAY # I put a delay here even though its the first turn so the user has time to see the empty board
        # Gameplay loop
        while not self.quit:
            if not self.minesweeper.is_game_over() and not self.minesweeper.is_game_won():
                pg.display.set_caption("Minesweeper -- Playing")
                # Let the AI make a move if it is its turn and a sufficient delay has passed
                if turn == "AI" and timeAICanMove and pg.time.get_ticks() >= timeAICanMove:
                    ai_player = AIPlayer(self.minesweeper, difficulty)
                    ai_x, ai_y = ai_player.make_move()
                    ai_highlight_cell = (ai_x, ai_y)
                    ai_highlight_time = pg.time.get_ticks()
                    timeAICanMove = None
            w, h = screen.get_size()
            grid_size = min(w, h) * 0.8
            cell_size = int(grid_size // BOARD_WIDTH)
            grid_width = BOARD_WIDTH * cell_size
            grid_height = BOARD_HEIGHT * cell_size
            grid_x0 = (w - grid_width) // 2
            grid_y0 = (h - grid_height) // 2

            
            # Post-game overlay buttons (positions computed later)
            # We create them each frame so they adapt to resize
            overlay_btn_width = 130
            overlay_btn_height = 44
            center_x = w // 2
            center_y = h // 2 + 50
            yes_btn = Button(center_x - overlay_btn_width - 15, center_y, overlay_btn_width, overlay_btn_height,
                             "Yes", (60, 130, 80), (90, 170, 120), WHITE)
            no_btn = Button(center_x + 15, center_y, overlay_btn_width, overlay_btn_height,
                            "No", (140, 70, 70), (180, 100, 100), WHITE)

            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # Safe exit
                    self.quit = True
                    break
                elif event.type == pg.VIDEORESIZE: # Resize window
                    new_w, new_h = self._clamp_size(event.w, event.h)
                    cur_w, cur_h = screen.get_size()
                    if (new_w, new_h) != (cur_w, cur_h):
                        screen = pg.display.set_mode((new_w, new_h), pg.RESIZABLE)
                elif reset_btn.handle_event(event):          
                    turn, timeAICanMove = self._reset_with_same_config()  
                    ai_highlight_cell = None                      
                    ai_highlight_time = None  
                elif event.type == pg.MOUSEBUTTONDOWN and self.minesweeper: # Click
                    if self.minesweeper.is_game_over() or self.minesweeper.is_game_won():   
                        if yes_btn.handle_event(event):                                  
                            turn, timeAICanMove = self._reset_with_same_config()      
                            ai_highlight_cell = None                                  
                            ai_highlight_time = None                                
                            continue                                                 
                        elif no_btn.handle_event(event):                               
                            self.quit = True                                          
                            break                                                  
                        continue  # ignore board clicks while overlay is up         
                    # Only let the person click on the cell if it is their turn.
                    if turn == "human":
                        hit = self.mouse_to_grid(*event.pos, grid_x0, grid_y0, cell_size, BOARD_WIDTH, BOARD_HEIGHT)
                        if hit is None:
                            continue  # Clicked margin or outside grid
                        grid_x, grid_y = hit
                        if event.button == 1: # Left click reveal
                            cellWasUncovered = self.minesweeper.reveal_square(grid_x, grid_y)
                            # Only check the mode and make the AI play if a cell was actually uncovered
                            if cellWasUncovered and mode == "Interactive": 
                                turn = "AI"
                                timeAICanMove = pg.time.get_ticks() + AI_DELAY
                                
                                
                        elif event.button == 3: # Right click flag
                            self.minesweeper.toggle_flag(grid_x, grid_y)

            # AI highlight logic
            if ai_highlight_cell and ai_highlight_time:
                if pg.time.get_ticks() - ai_highlight_time >= highlight_duration:
                    # self.minesweeper.reveal_square(*ai_highlight_cell)
                    ai_highlight_cell = None
                    ai_highlight_time = None
                    if mode == "Interactive":
                        turn = "human"
                        timeAICanMove = None
                    elif mode == "Auto":
                        turn = "AI"
                        timeAICanMove = pg.time.get_ticks() + AI_DELAY
            # Update timer
            if self.start_ticks is not None:
                if self.end_time is not None:
                    elapsed_seconds = self.end_time
                else:
                    elapsed_seconds = (pg.time.get_ticks() - self.start_ticks) // 1000
            else:
                elapsed_seconds = 0

            # Draw the grid
            screen.fill(BACKGROUND)
            board = self.minesweeper.get_display_board()
            for y in range(self.minesweeper.height):
                for x in range(self.minesweeper.width):
                    value = board[y][x]
                    icon = None
                    if value == -1:
                        color = MINE_RED
                        icon_size = int(cell_size * 0.5)
                        if self.mine_img is not None:
                            icon = pg.transform.smoothscale(self.mine_img, (icon_size, icon_size))
                        else:
                            icon = pg.Surface((icon_size, icon_size))
                            icon.fill(MINE_RED)
                    elif value == 0:
                        color = REVEALED_EMPTY
                        icon = font.render("0", True, WHITE)
                    elif value == "?":
                        color = HIDDEN
                        icon = None
                    elif value == "F":
                        color = HIDDEN
                        icon_size = int(cell_size * 0.5)
                        if self.flag_img is not None:
                            icon = pg.transform.smoothscale(self.flag_img, (icon_size, icon_size))
                        else:
                            icon = pg.Surface((icon_size, icon_size))
                            icon.fill(BLACK)
                    else:
                        color = REVEALED_NUMBER
                        icon = font.render(str(value), True, WHITE)

                    cell_rect = pg.Rect(grid_x0 + x * cell_size, grid_y0 + y * cell_size, cell_size, cell_size)
                    pg.draw.rect(screen, color, cell_rect)
                    pg.draw.rect(screen, GRID_LINE, cell_rect, 1)
                    if icon is not None:
                        screen.blit(icon, icon.get_rect(center=cell_rect.center))
                    # Highlight AI cell
                    if ai_highlight_cell == (x, y):
                        pg.draw.rect(screen, HIGHLIGHT_COLOR, cell_rect, 4)

            # Draw labels and UI elements
            # Turn indicator
            turn_text = font.render(f"Turn: {'AI' if turn == 'AI' else 'Player'}", True, (255, 255, 0) if turn == 'AI' else (0, 255, 0))
            screen.blit(turn_text, (w//2 - turn_text.get_width()//2, 10))

            # Column labels A–J (top)
            for col_index, letter in enumerate("ABCDEFGHIJ"):
                text_surface = font.render(letter, True, GENERAL_TEXT)
                text_rect = text_surface.get_rect(center=(
                    grid_x0 + col_index * cell_size + cell_size // 2,
                    grid_y0 - 20
                ))
                screen.blit(text_surface, text_rect)

            # Row labels 1–10 (left)
            for row_index in range(BOARD_HEIGHT):
                text_surface = font.render(str(row_index + 1), True, GENERAL_TEXT)
                text_rect = text_surface.get_rect(center=(
                    grid_x0 - 20,
                    grid_y0 + row_index * cell_size + cell_size // 2
                ))
                screen.blit(text_surface, text_rect)

            # Timer display
            time_text = font.render(f"TIME: {elapsed_seconds}", True, GENERAL_TEXT)
            screen.blit(time_text, (
                w - time_text.get_width() - 10,
                h - time_text.get_height() - 10
            ))

            # Flag Count
            flag_rect = pg.Rect(w/2, h*12/13, 10, 10)
            pg.draw.rect(screen, BACKGROUND, flag_rect)
            flags = font.render(f'Flags Remaining: {str(self.minesweeper.flags_remaining)}', True, WHITE)
            screen.blit(flags, flags.get_rect(center=flag_rect.center))

            # Game end screen overlay
            if self.minesweeper.is_game_over(): # Loss
                pg.display.set_caption("Minesweeper -- You Lose")
                if self.end_time is None: # Freeze final time
                    self.end_time = (pg.time.get_ticks() - self.start_ticks) // 1000
                goto_play_again_screen = True 
                if play_again_at is None:              
                    play_again_at = pg.time.get_ticks() + 900  
                win_width, win_height = screen.get_size()
                overlay = pg.Surface((win_width, win_height), pg.SRCALPHA) # Create an overlay surface that allows for transparency
                overlay.fill(TRANSPARENT_RED, (0, win_height // 2 - 45, win_width, 60))
                screen.blit(overlay, (0, 0))
                text = font.render("Game Over", True, BLACK)
                screen.blit(text, text.get_rect(center=(win_width // 2, win_height // 2 - 15)))
            elif self.minesweeper.is_game_won(): # Win
                pg.display.set_caption("Minesweeper -- You Win!")
                if self.end_time is None: # Freeze final time
                    self.end_time = (pg.time.get_ticks() - self.start_ticks) // 1000
                goto_play_again_screen = True
                if play_again_at is None:               # NEW
                    play_again_at = pg.time.get_ticks() + 900  # NEW
                win_width, win_height = screen.get_size()
                overlay = pg.Surface((win_width, win_height), pg.SRCALPHA) # Create an overlay surface that allows for transparency
                overlay.fill(TRANSPARENT_GREEN, (0, win_height // 2 - 30, win_width, 60))
                screen.blit(overlay, (0, 0))
                text = font.render("You Win!", True, BLACK)
                screen.blit(text, text.get_rect(center=(win_width // 2, win_height // 2 - 15)))
            
            reset_btn = Button(10, 10, 110, 36, "Reset", (110, 110, 130), (140, 140, 170), WHITE)
            reset_btn.draw(screen)

            # Custom cursor
            if self.cursor_img is not None:
                mx, my = pg.mouse.get_pos()
                screen.blit(self.cursor_img, (mx, my))

            pg.display.flip()
            if goto_play_again_screen and not self.quit:
                if play_again_at is not None and pg.time.get_ticks() < play_again_at:
                    clock.tick(60)
                    # (The overlay is already drawn this frame; just wait another frame.)
                    continue
                choice = None
                while choice is None and not self.quit:
                    w, h = screen.get_size()
                    screen.fill(BACKGROUND)

                    # Title
                    try:
                        # reuse loaded fonts if available in scope
                        pass
                    except:
                        pass
                    title_surf = title_font.render("Play Again?", True, TITLE_TEXT)

                    # Center positions
                    title_rect = title_surf.get_rect(center=(w // 2, h // 2 - 60))

                    # Soft band behind text
                    band = pg.Surface((int(w * 0.8), 120), pg.SRCALPHA)
                    band.fill((0, 0, 0, 90))
                    screen.blit(band, (w // 2 - band.get_width() // 2, h // 2 - 100))

                    screen.blit(title_surf, title_rect)

                    # Buttons (reuse Button class; no font_size kw)
                    btn_w, btn_h = 160, 56
                    gap = 24
                    left_x = (w - (btn_w * 2 + gap)) // 2
                    btn_y = h // 2 + 10

                    yes_btn = Button(left_x, btn_y, btn_w, btn_h, "YES", (60, 130, 80), (90, 170, 120), WHITE)
                    no_btn  = Button(left_x + btn_w + gap, btn_y, btn_w, btn_h, "NO", (140, 70, 70), (180, 100, 100), WHITE)

                    # subtle plate behind buttons
                    strip = pg.Surface((btn_w * 2 + gap + 20, btn_h + 20), pg.SRCALPHA)
                    strip.fill((0, 0, 0, 70))
                    screen.blit(strip, (left_x - 10, btn_y - 10))

                    yes_btn.draw(screen)
                    no_btn.draw(screen)

                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            self.quit = True
                            break
                        elif event.type == pg.VIDEORESIZE:
                            new_w, new_h = self._clamp_size(event.w, event.h)
                            cur_w, cur_h = screen.get_size()
                            if (new_w, new_h) != (cur_w, cur_h):
                                screen = pg.display.set_mode((new_w, new_h), pg.RESIZABLE)
                        elif event.type == pg.KEYDOWN:
                            if event.key in (pg.K_y, pg.K_RETURN):
                                choice = "yes"
                            elif event.key in (pg.K_n, pg.K_ESCAPE):
                                choice = "no"
                        elif yes_btn.handle_event(event):
                            choice = "yes"
                        elif no_btn.handle_event(event):
                            choice = "no"

                    if self.cursor_img is not None:
                        mx, my = pg.mouse.get_pos()
                        screen.blit(self.cursor_img, (mx, my))


                    pg.display.flip()
                    clock.tick(60)

                # Apply choice
                if not self.quit:
                    if choice == "yes":
                        turn, timeAICanMove = self._reset_with_same_config()
                        ai_highlight_cell = None
                        ai_highlight_time = None
                        goto_play_again_screen = False  # back to gameplay with fresh board
                        play_again_at = None
                        continue  # restart gameplay loop 
                    else:
                        self.quit = True
                        play_again_at = None 
                        break  # exit  loop

            clock.tick(60)
        self.exit_game()