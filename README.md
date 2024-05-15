## 2048 Game in Python

**How to Play:**

1. **Run the 2048** 
2. **Choose Grid Size:** You'll be prompted to enter a number (3, 4, or 5) to choose the grid size or a letter "X" to load 3x3, "C" to load 4x4 and "V" to load 5x5 saved game for that size. or you can enter setting menu to edit yout preferences.
3. **Make Moves:** Use the following keys to move the tiles:
    - **W**: Move Up
    - **A**: Move Left
    - **S**: Move Down
    - **D**: Move Right
4. **Win the Game:** Reach a tile with the number 2048 to win!

**Additional Inputs:**

- **H**: Hide/show the input guides (for a cleaner look).
- **M**: Mute or unmute the sound effects.
- **O**: Save the current game state to a file.
- **Z**: Restore the previous move (useful for undoing mistakes).
- **F**: Bring you to "Fast mode" so you dont need to hit Enter every time (press F in fast mode to exit fast mode)
- **Q**: Quit the game.

* the game automaticly hide input guides after 100 points
* in fast mode the sound is mute and the guides are hidden (you can disable this in setting menu)
* you cant save your game state in fast mode and you have do in normal game
* you cant exit the app in the fast mode

**Loading Saved Games:**

- You can load saved games by entering 'x', 'c', or 'v' at the beginning, corresponding to saved games for grid sizes 3x3, 4x4, and 5x5 respectively.

**Top Scores:**

- The game keeps track of your top scores for each grid size.

**Sound Effects:**

- The game uses sound effects for some actions (enable/disable with 'M').If you faced any error on that, make sure the `pygame` library is installed for sound to work. (First open cmd by search or Win+R, then type "pip install pygame")

**Game Features:**

- Colorful display of tiles based on their value.
- Being able to pickup where you left the game at anytime
- Keep track of your top scores
- Nice sound effects
- Clear screen functionality for a better playing experience.
- User-friendly input handling and guidance.
- Fast input mode 
- Setting menu to edit yout preferences

This code provides a fun and challenging 2048 game experience. Enjoy playing!
