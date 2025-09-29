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

------------------------------------------------------------------------------------------------------------------------------

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

------------------------------------------------------------------------------------------------------------------------------

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

------------------------------------------------------------------------------------------------------------------------------

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

------------------------------------------------------------------------------------------------------------------------------
