## 2048 Game in Python

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

**How to Play:**

1. **Run the 2048** Download the `.exe ` file from [releases in github](https://github.com/Behroz666/py2048/releases) and run it.(if you are using linux or mac follow the instruction for [runing the code your self](https://github.com/Behroz666/py2048#:~:text=libraries%20and%20dependencies%20to%20run%20the%20code))
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

**`.EXE` releases**

- `.exe` files are made by `pyinstaller`. you can made this `.exe` file yoursel! first of all you need to install `pyinstaller` by entering this commands on `cmd` (you can open up `cmd` with `Win + R`): `pip install pyinstaller`. then you need to open the folder you cloned the repository(with `git clone https://github.com/Behroz666/py2048`) and right click and choose `open in terminal` (you can do this by `cd` command too). then this command will make `.exe` file for you: `pyinstaller --onefile 2048.py`. 

**libraries and dependencies to run the code**

- First of all you need python to run this code. You can download python from `https://www.python.org/downloads/`.

- You can install all dependecies by runing `pip install -r requirements.txt`

- This code use `pynput` and `pyautogui` libraries. if you want to use the code be sure to install libraries by entering these commands on `cmd` (you can open up `cmd` with `Win + R`): `pip install pynput` and `pip install pyautogui`

- The game uses sound effects for some actions (enable/disable with 'M').If you faced any error on that, make sure the `pygame` library is installed for sound to work. (First open `cmd` by search or `Win+R`, then type `pip install pygame`)