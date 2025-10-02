## Project Requirements

**Project 1 Functionality**
- Game setup, gameplay, mine flagging, player interface, and game conclusion must all work, even if inherited code was buggy.

**Artificial Intelligence (AI) Solver**
- AI plays on the same board as the player.
- Turns alternate between player and AI (interactive mode) or AI solves automatically.
    - Easy: AI uncovers random cells, avoids flagged/uncovered.
    - Medium: AI uncovers randomly until a safe cell (zero adjacent mines), then uses revealed numbers to uncover adjacent cells.
    - Hard: AI always uncovers a safe cell (never detonates a mine; simulates perfect knowledge).

**Custom Addition**
- Propose and implement one new feature to enhance the game.
- Describe the feature with a UML diagram (class, sequence, or use case).

---------------------------------------------------------------------------------------

# Meeting Notes

## First Team Meeting
**Date:** Wednesday, September 24th, 2025

**Attendees:**
- Kundana Dongala
- Katie Nordberg
- Christina Sorensen
- Vivian Lara

### Agenda & Discussion Points
- Assign roles (Project Manager, Scrum Master, Developer)
- Decide on game logic for Easy, Medium, and Hard modes
- Assign tasks to each person

### Updates & Decisions Made
- Scrum meetings scheduled for Wednesdays at 1 PM
- All members are developers
- Team communication to be maintained via text updates
- Formal Roles:
    - Project Manager/Scrum Master: Kundana Dongala
    - Developers: Navya Nittala, Katie Nordberg, Christina Sorensen, Vivian Lara

### Action Items
- Talk to TA about expectations for the three game modes
- Finalize decisions during TA meeting and begin coding assignments (Katie Nordberg, Christina Sorensen, Vivian Lara)
- Kundana and Navya to check in, complete assigned tasks, and submit absence report if not present

### Upcoming Meetings
**Next TA Meeting:**
    - Date: Thursday, September 25th
    - Time: 9:30 AM
    - Location: EATON 3001
**Next Scrum Meeting:**
    - Date: Friday, September 26th
    - Time: 5 PM
    - Location: EATON 2
**Next Team Meeting:**
    - Date: Wednesday, October 1st
    - Time: 1 PM
    - Platform: Teams

---------------------------------------------------------------------------------------

## Second Team Meeting
**Date:** Thursday, September 25th

**Attendees:**
- Katie Nordberg
- Christina Sorensen
- Vivian Lara

### Agenda & Discussion Points
- TA explained requirements
- Katie discussed the plan for dividing up tasks
- Focus on developing the AI first
- Additional features to consider:
    - Add sound effects and custom features
    - Show whose turn it is and highlight the AI’s chosen cell (e.g., darken or circle before it disappears)
    - Add a replay button so players can restart the game after win/lose

### Updates & Decisions Made
- After win/lose, the game should restart
- Katie will implement Medium AI
- Team debated AI implementation strategies and used a whiteboard for clarification
    - Decided on three AI modes:
        - Interactive (AI and human alternate turns)
        - Auto (AI only)
        - Solo (human only)
- Finalized AI logic (see diagram/picture)
- Vivian will implement Hard AI
- Christina will implement Easy AI
- Kundana and Navya will implement extra features 

### Action Items
- Each member to begin implementing their assigned AI logic
- Explore adding replay button and UI indicators (turn highlight, AI move indicator)
- Discuss custom features further in next meeting

### Upcoming Meetings
**Next Scrum Meeting:**
    - Date: Friday, September 26th
    - Time: 5 PM
    - Location: EATON 2
**Next Team Meeting:**
    - Date: Wednesday, October 1st
    - Time: 1 PM
    - Platform: Teams 
**Next TA Meeting:**
    - Date: Thursday, October 2nd
    - Time: 9:30 AM
    - Location: EATON 3001

---------------------------------------------------------------------------------------

## Third Team Meeting
**Date:** Friday, September 26th

**Attendees:**
- Katie Nordberg
- Christina Sorensen
- Vivian Lara
- Kundana Dongala 

### Agenda & Discussion Points
- Quick updates from each member (was only a 5-minute meeting)
- Decided to implement a feature to show whose turn it is and which cell the AI clicked on (e.g., darken or circle before it disappears)

### Updates & Decisions Made
- Feature, documentation and notes assigned to Kundana
- Katie, Christina, and Vivian continuing with their assigned AI tasks
- Navya working on replay button feature

### Action Items
- Kundana: Implement turn indicator and AI move highlight
- Navya: Implement replay button
- Other members: Continue progress on assigned AI logic

### Upcoming Meetings
**Next Team Meeting:**
    - Date: Wednesday, October 1st
    - Time: 1 PM
    - Platform: Teams 
**Next TA Meeting:**
    - Date: Thursday, October 2nd
    - Time: 9:30 AM
    - Location: EATON 3001
**Next Scrum Meeting:**
    - Date: Friday, October 3rd
    - Time: 5 PM
    - Location: EATON 2

---------------------------------------------------------------------------------------
## Fourth Team Meeting
**Date:** Wednesday October 1st

**Attendees:**
- Katie Nordberg
- Christina Sorensen
- Vivian Lara
- Kundana Dongala 

### Agenda & Discussion Points
- Quick updates from each member
- talk through what needs to be done in the last couple of days 

### Updates & Decisions Made
- Christina:
    - Implemented Easy AI feature and did testing
    - Caught bug where the user was getting more turns than the AI (flags issue)

- Katie:
    - Testing, reset button, Medium and Hard AI implementation
    - Fixed bug where AI was always choosing (0,0):
        - Code wasn’t calling AI make_move function
        - Refactored code so y,x coordinate is returned
        - Commented out line 387 in MinesweeperGame.py (avoided duplicate reveal logic)
    - Changed highlight color from yellow to black (for visibility)
    - Reset button:
        - Removed logic from main title
        - Ensured button logic is drawn on screen (reset_btn.draw())
        - Adjusted drawing order so it’s visible
    - Added 121 pattern (to exceed requirements)
    - Cleaned up Hard AI code (removed commented-out sections)

- Vi
    - Implemented Medium AI mode with strategies:
        - Flag surrounding covered cells if number of covered cells = number of mines
        - Reveal surrounding covered cells if flagged cells = number of mines
    - These strategies implemented as Pattern 4 and Pattern 6 in code

- Kundana:
    - Implemented feature to show whose turn it is and highlight the AI’s chosen cell
    - Updated all meeting notes and shared Google Sheet with tasks, estimated time, and actual time tracking
    - Adjusted gameplay:
        - AI can flag multiple times in a turn, but user cannot
        - For user, a flag counts as a move/turn
    - Adjusted reset button placement (moved to bottom) and aligned play-again page layout

- Navya
    - Pushed reset/play again feature: Added self.last_config so game remembers board configuration and implemented _reset_with_same_config to reset with identical settings
    - added separate “Play Again?” screen after Game Over/Win popup with Yes/No button

- Observations (AI moves before dying):
    10 mines: Easy – 4, Medium – 15, Hard – 41
    20 mines: Easy – 6, Medium – 20, Hard – 27

### Action Items
- Kundana: Fix issue where right-clicking on an already flagged mine still counts as a turn; keep notes and estimations updated
- Katie: Create system architecture diagram for Hard AI mode
- Vivian: Create system architecture diagram for Medium AI mode
- Christina: Create system architecture diagram for Easy AI mode
- Navya: Create 2 diagrams (Reset button and Play Again feature)
- Everyone is incharge of testing 

### Upcoming Meetings
**Next TA Meeting:**
    - Date: Thursday, October 2nd
    - Time: 9:30 AM
    - Location: EATON 3001
**Next Scrum Meeting:**
    - Date: Friday, October 3rd
    - Time: 5 PM
    - Location: EATON 2

---------------------------------------------------------------------------------------

## Fifth Team Meeting
**Date:** Thursday, October 2nd

**Attendees:**
- Katie Nordberg
- Christina Sorensen
- Vivian Lara
- Kundana Dongala 

### Agenda & Discussion Points
- Review progress since last meeting (Easy, Medium, Hard AI, Reset/Play Again, Turn Indicator)
- Confirm requirements for final deliverables and any extra features (121 pattern, highlighting, replay screen)
- Discuss system architecture diagrams for Easy, Medium, Hard, Reset/Replay features
- Share observations on AI performance (moves until losing: Easy, Medium, Hard) and get TA’s feedback
- Have him play the game 
- Confirm expectations for project submission and presentation

### Updates & Decisions Made

### Action Items

### Upcoming Meetings
**Next Scrum Meeting:**
    - Date: Friday, October 3rd
    - Time: 5 PM
    - Location: EATON 2
---------------------------------------------------------------------------------------