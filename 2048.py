import random
import os
from os.path import dirname, realpath, join
import subprocess
import platform
import copy
import json
import pygame
from pynput import keyboard
import pyautogui

score = 0 # Defining score variable
won = False # Flag for the 2048 win
set_board = True #Flag for setting the board or loading the file
grid = ()   
first_move = True # Flag for just giving 2 on first move
biggest_tile = 2 # Start the count for the biggest tile
move_count = 0 # Counter for move
Ending = False # Flag for ending screen boxes headers
first_F = False
scape = True

appdir = dirname(realpath(__file__)) # Getts current app location
datadir = "2048data" # folder name for the game data
if not os.path.exists(join(appdir, datadir)):
    try:
        os.makedirs(join(appdir, datadir), exist_ok=True)  # Create nested directories if necessary
        # Create needed files with default values 
        with open(join(appdir, datadir, "preferences.txt"), 'w') as file :
            data_string = "True\nFalse\nTrue\nFalse"
            file.write(data_string)
        filenames = ["topscores_3.txt", "topscores_4.txt", "topscores_5.txt"]
        for filename in filenames : 
            with open(join(appdir, datadir, filename), 'w') as file :
                data_string = "0\n0\n0"
                file.write(data_string)
        filenames = ["save3score.txt", "save4score.txt", "save5score.txt"]
        for filename in filenames : 
            with open(join(appdir, datadir, filename), 'w') as file :
                data_string = "0,0,0"
                file.write(data_string)
        os_name = platform.system() # Gets os name
        # Define command for each os 
        if os_name == "Windows" :  
            command = ["attrib", "+H", "+R", join(appdir, datadir)]
        if os_name == "Linux" :
            command = ["chattr", "+h", join(appdir, datadir)]
        if os_name == "Darwin" : 
            command = ["chflags", "hidden", join(appdir, datadir)]
        try:
            subprocess.run(command, check=True) # Run the command to hide the data folder
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error hiding folder: {e}")
    except OSError as e:
      print(f"Error creating folder '{join(appdir, datadir)}': {e}")

def boolean_convert (filename) :
    try : 
        with open(filename, 'r') as file : 
            lines = file.readlines()
    except FileNotFoundError : 
        raise ValueError(f"File '{filename}' not found.")
    booleans = []
    for line in lines : 
        line = line.strip()
        if line.lower() == "true":
            booleans.append(True)
        elif line.lower() == "false" :
            booleans.append(False)
        else :
            raise ValueError(f"Invalid value '{line}' found in file.")
    return booleans

booleans = boolean_convert (join(appdir, datadir, "preferences.txt"))
hide, mute, automute, fast_input = booleans
if fast_input : 
    first_F  = True

def clear_screen() : # Clear screen function
    os.system('cls' if os.name == 'nt' else 'clear')  # Windows or Linux/macOS

def initialize_board() : # Initializes the game board with a grid of zeros
    return [[0] * grid for _ in range(grid)]

def place_random_tile(board):
    global first_move
    empty_cells = []  # Create an empty list to store empty cell coordinates

    # Find all empty cells
    for i in range(grid):
        for j in range(grid):
            if board[i][j] == 0:
                empty_cells.append((i, j))  # Append coordinates of empty cells

    if empty_cells:  # Check if there are any empty cells
        if first_move : # Just put 2 in first move
            first_choice = [2]
            i, j = random.choice(empty_cells)  # Select a random empty cell
            board[i][j] = random.choice(first_choice)
            first_move = False
        else :
            # Generate a weighted random choice with a 10x bias towards 2
            weighted_choices = [4] + [2] * 10
            i, j = random.choice(empty_cells)  # Select a random empty cell
            board[i][j] = random.choice(weighted_choices)

def score_box () : # Function for box that shows the game Stat 
    global grid, score, biggest_tile, move_count, Ending
    count = int(move_count / 6)
    width = int(grid * 6) - 1
    if not Ending : 
        top_border = "┌" + "─" * (width) + "┐"
    else : # Change the top berder in ending screen for header box
        top_border = "├" + "─" * (width) + "┤"
    bottom_border = "└" + "─" * (width) + "┘"
    # Making the strings for the box
    score_str = f"Score: {score:{width - len('Score: ')}}"
    Tile_str = f"Biggest Tile: {biggest_tile:{width - len('Biggest Tile: ')}}"
    move_str = f"Move: {count:{width - len('Move: ')}}"

    box = f"{top_border}\n│{score_str}│\n│{Tile_str}│\n│{move_str}│\n{bottom_border}"
    print (box)

def print_pattern(): # Cool Ascii art pattern
  pattern = [
      "\033[91m 22    ""\033[0m000   ""\033[92m4  4   ""\033[95m888 ",
      "\033[91m2  2  ""\033[0m0  00  ""\033[92m4  4  ""\033[95m8   8",
      "\033[91m  2   ""\033[0m0 0 0  ""\033[92m4444   ""\033[95m888 ",
      "\033[91m 2    ""\033[0m00  0     ""\033[92m4  ""\033[95m8   8",
      "\033[91m2222   ""\033[0m000      ""\033[92m4   ""\033[95m888 \033[0m"
  ]

  for row in pattern:
    print (row)

def setting_menu(): # Defining setting menu
    global hide, mute, automute, fast_input, user_input, first_F
    invin = False # Flag for invalid input
    while True : 
        clear_screen()
        if invin : # Error for invalid input
            print ("\033[31mInvalid input\033[0m")
            invin = False
        if hide : # check and print the status of settings
            hideS = "\033[32mEnabled\033[0m"
            hideSL = 7 # Length of the shit cause len is broken with ANSI codes
        else : 
            hideS = "\033[31mDisabled\033[0m"
            hideSL = 8
        if mute :
            muteS = "\033[32mEnabled\033[0m"
            muteSL = 7
        else : 
            muteS = "\033[31mDisabled\033[0m"
            muteSL = 8
        if automute :
            automuteS = "\033[32mEnabled\033[0m"
            automuteSL = 7
        else : 
            automuteS = "\033[31mDisabled\033[0m"
            automuteSL = 8
        if fast_input :
            fast_inputS = "\033[32mEnabled\033[0m"
            fast_inputSL = 7 
        else : 
            fast_inputS = "\033[31mDisabled\033[0m"
            fast_inputSL = 8

        arz = 30 # Width of setting box
        print ("┌" + "─"*arz + "┐" + "\n│" + " "*int((arz/2)-3) + "Setting" + " "*int((arz/2)-4) + "│") # Headder for setting box
        top_border = "├" + "─" * (arz) + "┤"
        bottom_border = "└" + "─" * (arz) + "┘"
        # Making strings for each setting
        hide_str = "Hide input guide" + " "*int(arz - 16 - hideSL) + hideS
        mute_str = "Mute sound" + " "*int(arz - 10 - muteSL) + muteS
        automute_str = "Automute" + " "*int(arz - 8 - automuteSL) + automuteS 
        fastinput_str = "Fast input mode" + " "*int(arz - 15 - fast_inputSL) + fast_inputS
        box = f"{top_border}\n│{hide_str}│\n│{mute_str}│\n│{automute_str}│\n│{fastinput_str}│\n{bottom_border}" # Make the box
        print (box) # Print the box
        print ("Automute stands for automatically mute sound in fast input mode") # Input guide
        print("""
Switch hide input guide           => Enter 'H'
Switch mute sound                 => Enter 'M'
Switch Automute                   => Enter 'A'
Switch Fast input mode            => Enter 'F'\033[32m
Save and Leave                    => Enter 'Q'\033[31m
Reset the settings to default     => Enter 'R'\033[0m
""")

        set_input = input("\033[93mEnter your Setting choice: \033[0m").lower() # Get the input
        valid_input_set = "hsfmaqr" # All valid inputs
        if set_input not in valid_input_set : # Checks if the input is valid
            invin = True
            continue
        if set_input == "h" : # Change the setting based on the input
            if hide : 
                hide = False
                continue
            else : 
                hide = True
                continue
        if set_input == "m" : 
            if mute : 
                mute = False 
                continue
            else : 
                mute = True
                continue
        if set_input == "a":
            if automute :
                automute = False
                continue
            else :
                automute = True
                continue
        if set_input == "f" :
            if fast_input :
                fast_input = False
                continue
            else : 
                fast_input = True
                first_F = True
                continue
        if set_input == "r" : # Reset back all settings to default 
            hide = True
            mute = False
            automute = True
            fast_input = False
            continue
        if set_input == "q": # Save and exit the setting menu
            with open(join(appdir, datadir, "preferences.txt"), 'w') as file : # Save the file 
                    data_string = "\n".join([str(hide), str(mute), str(automute), str(fast_input)])
                    file.write(data_string)
            clear_screen()
            print("\033[32mSetting Saved\033[0m") # Notify user
            user_input = ""
            break

clear_screen()

grid_size_options = { # Getting grid size with a dictionary for loading saved games
    "x": 3,
    "c": 4,
    "v": 5,
    "q": 0,
    "s": 999,
}

while True: # First input screen 
    try:
        print_pattern() 
        # Input guide for first input screen
        print ("""
Start a new game              => Enter your grid size (3-5)
Load 3*3 board save file      => Enter 'x' 
Load 4*4 board save file      => Enter 'C'
Load 5*5 board save file      => Enter 'V'
Leave the game                => Enter 'Q'
Edit preferences              => Enter 'S'
               """)
        user_input = input("\n\033[93mPlease enter a number between 3 and 5 or X, C, V to load or Q to leave: \033[0m").lower()

        if user_input.isdigit() and 2 < int(user_input) <= 5: # Check for valid number input (3-5)
            grid = int(user_input)
            clear_screen()
            break

        elif user_input in grid_size_options: # Check for loading saved games using dictionary
            grid = grid_size_options[user_input]
            if grid == 0 : # Esacpe the code if the input was Q (grid = 0)
                pyautogui.hotkey('ctrl', 'c')
            if grid == 999 :
                setting_menu()
                continue
            set_board = False
            filename = f"{appdir}/{datadir}/savefile{grid}.txt"  # Construct filename based on grid size
            scorename = f"{appdir}/{datadir}/save{grid}score.txt"
            try:
                with open(filename, 'r') as f: # Load the board
                    State = f.read()
                    board = json.loads(State)
                with open(scorename, 'r') as f : # Load stats to continue
                    data_string = f.read()
                data_list = data_string.split(",")
                score = int(data_list[0])  
                move_count = int(data_list[1])
                biggest_tile = int(data_list[2])
                clear_screen()
                print("\033[32mLoading done\033[0m")
            except FileNotFoundError: # Start new matching game if the savefile was missing
                clear_screen()
                print(f"\033[33m{grid}*{grid} Save file not found. Starting new game.\033[0m")
                board = initialize_board()
                preboard = board
                place_random_tile(board)
                if grid == 5 :
                    place_random_tile(board)
            break

        else: # Clear screen and prompt again for invalid input
            clear_screen()
            print("\033[31mInvalid input.\033[0m")

    except ValueError:
        clear_screen()
        print("\033[31mValue error.\033[0m")

color_codes = { # Color code dictionary for different number ranges
    2: "\033[91m",  # bright red for 2
    4: "\033[92m",  # bright green for 4
    8: "\033[95m",  # bright magenta for 8
    16: "\033[34m",  # blue for 16
    32: "\033[94m",  # bright blue for 32
    64: "\033[36m",  # cyan for 64
    128: "\033[46m\033[37m",  # cyan bg, white text for 128
    256: "\033[41m\033[37m",  # Red bg, white text for 256
    512: "\033[42m\033[37m",  # green bg, white text for 512
    1024: "\033[45m\033[37m",  # magenta bg, white text for 1028
    2048: "\033[43m\033[37m",  # yellow bg, white text for 2056
    4096: "\033[44m\033[37m",  # Blue bg, white text for 4096
    8192: "\033[101m\033[37m",  # Bright red bg, white text for 8192
    16384: "\033[102m\033[37m",  # Bright green bg, white text for 16384
    32768: "\033[103m\033[37m",  # Bright Yellow bg, white text for 32768
    65536: "\033[104m\033[37m",  # Bright Blue bg, white text for 65536
    131072: "\033[105m\033[37m",  # Bright Magenta bg, white text for 131072
    262144: "\033[106m\033[37m",  # Bright Cyan bg, white text for 262144
}

def print_board(board) : # Prints the current state of the game board to the console
    global Ending
    a = 0
    if not Ending : 
        print("┌─────" + "┬─────"*(grid - 1) + "┐")
    else : # Change top border for ending screen
        print("├─────" + "┬─────"*(grid - 1) + "┤")
    for row in board:
        # Center-align each tile within its cell using string formatting
        formatted_row = "│ " + "│ ".join([color_codes.get(x, "") + str(x).center(4) + "\033[0m" for x in row]) + "│"
        print(formatted_row)
        if a < (grid - 1) :
            a += 1
            print("├─────" + "┼─────"*(grid - 1) + "┤")
        else :
            print("└─────" + "┴─────"*(grid - 1) + "┘")

# Defining move functions
def move_up(board) :
    global score, won, biggest_tile, move_count
    move_count = move_count + 1 # Add one to move count
    for j in range(grid):
        column = [board[i][j] for i in range(grid)]
        column = [tile for tile in column if tile != 0]
        column += [0] * (grid - len(column))
        for i in range(grid - 1) :
            if column[i] == column[i + 1] :
                column[i] *= 2
                column[i + 1] = 0
                if scoring :
                    score += int(column[i])
                    if int(column[i]) == 2048 :
                        won = True # Flag the win
                if biggest_tile < int(column[i]) :
                    biggest_tile = int(column[i]) # Update the biggest tile count
        column = [tile for tile in column if tile != 0]
        column += [0] * (grid - len(column))
        for i in range(grid) :
            board[i][j] = column[i]

def move_down(board) :
    global score, won, biggest_tile, move_count
    move_count = move_count + 1
    for j in range(grid):
        column = [board[i][j] for i in range(grid -1, -1, -1)]
        column = [tile for tile in column if tile != 0]
        column += [0] * (grid - len(column))
        for i in range(grid - 1, 0, -1) :
            if column[i] == column[i - 1] :
                column[i] *= 2
                column[i - 1] = 0
                if scoring :
                    score += int(column[i])
                    if int(column[i]) == 2048 :
                        won = True
                if biggest_tile < int(column[i]) :
                    biggest_tile = int(column[i])
        column = [tile for tile in column if tile != 0]
        column += [0] * (grid - len(column))
        for i in range(grid -1, -1, -1):
            board[i][j] = column[grid - 1 - i]

def move_left(board) :
    global score, won, biggest_tile, move_count
    move_count = move_count + 1
    for i in range(grid) :
        row = board[i]
        row = [tile for tile in row if tile != 0]
        row += [0] * (grid - len(row))
        for j in range(grid -1) :
            if row[j] == row[j + 1] :
                row[j] *= 2
                row[j + 1] = 0
                if scoring :
                    score += int(row[j])
                    if int(row[j]) == 2048 :
                        won = True
                if biggest_tile < int(row[j]) :
                    biggest_tile = int(row[j])
        row = [tile for tile in row if tile != 0]
        row += [0] * (grid - len(row))
        board[i] = row 

def move_right(board) :
    global score, won, biggest_tile, move_count
    move_count = move_count + 1
    for i in range(grid) :
        row = board[i]
        row = [tile for tile in row if tile != 0]
        row = [0] * (grid - len(row)) + row
        for j in range(grid -1, 0, -1) :
            if row[j] == row[j - 1] :
                row[j] *= 2
                row[j - 1] = 0
                if scoring :
                    score += int(row[j])
                    if int(row[j]) == 2048 :
                        won = True
                if biggest_tile < int(row[j]) :
                    biggest_tile = int(row[j])
        row = [tile for tile in row if tile != 0]
        row = [0] * (grid - len(row)) + row
        board[i] = row

def move(board, direction): # Assigning keys to move functions
    if direction == "W":
        move_up(board)
    elif direction == "A":
        move_left(board)
    elif direction == "S":
        move_down(board)
    elif direction == "D":
        move_right(board)

def top_score_check(score, filename):
    try:
        # Read existing scores from the file
        with open(filename, 'r') as file:
            ex_scores = [int(line.strip()) for line in file]
    except FileNotFoundError:
        ex_scores = []

    all_scores = ex_scores + [score]  # Combine existing scores and the new score
    top_scores = sorted(all_scores, reverse=True)[:3]  # Keep only the top 3 scores
    if score in top_scores:
        print("\033[33mCongratulations! You have a new top score!\033[0m")  # Highlight new top score
    width = int(grid * 6) - 1
    header = f"Top scores in {grid}*{grid}"  # Showing previous top scores
    fir, sec, thir = top_scores 
    if score == fir : 
        fir = " "*(width - len(str(score)) - 5) + "\033[33m{}\033[0m".format(score)
    if score == sec : 
        sec = " "*(width - len(str(score)) - 5) + "\033[90m{}\033[0m".format(score)
    if score == thir : 
        thir =  " "*(width - len(str(score)) - 5) + "\033[31m{}\033[0m".format(score)
    # Making the box
    top_border = "┌" + "─" * width + "┐"
    bottom_border = "└" + "─" * width + "┘"
    mid_border = "├" + "─" * width + "┤"
    center = " " * (int((width - len(header)) / 2))  # Amount of space needed for center aligning
    First_str = f"\033[33m1st: \033[0m{fir:{width - len('1st: ')}}"
    Secord_str = f"\033[90m2nd: \033[0m{sec:{width - len('2nd: ')}}"
    third_str = f"\033[31m3rd: \033[0m{thir:{width - len('3rd: ')}}"
    header_str = f"{header:{width - len(center)}}"

    box = f"{top_border}\n│{center}\033[96m{header_str}\033[0m│\n{mid_border}\n│{First_str}│\n│{Secord_str}│\n│{third_str}│\n{bottom_border}"
    print(box)

    # Open the file in write mode and overwrite the top 3 scores
    with open(filename, 'w') as file:
        for top in top_scores:
            file.write(str(top) + "\n")

def play_sound(filename): # Defining function for playing sound using pygame
  try:
    pygame.init()
    sound = pygame.mixer.Sound(join(appdir, datadir, filename))
    sound.play()
  except FileNotFoundError:
    print(f"\033[31mError: Could not find sound effect '{filename}'\033[0m")

fvalidcheck = ""
def fast_input_fun(keyst): # Defining a function for everything in fast move
    global fvalidcheck, scoring, fast_input, board, preboard, Ending, scape, first_F
    clear_screen()
    fvalidcheck = copy.deepcopy(board) # Checking if the move do anything
    scoring = False
    if keyst == "w" : # Check to validate next move
        move_up (board)
    if keyst == "a" :
        move_left (board)
    if keyst == "s" :
        move_down (board)
    if keyst == "d" :
        move_right (board)
    if fvalidcheck == board :
        if not mute :
            play_sound('SFX2.wav')
        print ("\033[31myour move is invalid\033[0m")
        print ("\033[93mPress 'F' to exit fast input mode\033[0m")
        score_box()
        print_board(board)
    else : # Making next board
        board = copy.deepcopy(fvalidcheck)
        scoring = True
        preboard = copy.deepcopy(board) # Backup for Z 
        if keyst == "w" :
            move_up (board)
        if keyst == "a" :
            move_left (board)
        if keyst == "s" :
            move_down (board)
        if keyst == "d" :
            move_right (board)
        if won : # Check if won
            print ("\033[33m*** You have won the game ***\033[0m")
        print ("\033[93mPress 'F' to exit fast input mode\033[0m")
        score_box()
        place_random_tile(board)
        print_board(board)
        if not mute :
            play_sound('SFX1.wav') # Play the sound
        if 0 not in  board :
            # Check for game over
            bak = copy.deepcopy(board) # Backup for board
            # Making all move possibilites
            move_up(board)
            upcheck = copy.deepcopy(board)
            board = copy.deepcopy(bak)
            move_right(board)
            rightcheck = copy.deepcopy(board)
            board = copy.deepcopy(bak)
            move_left(board)
            leftcheck = copy.deepcopy(board)
            board = copy.deepcopy(bak)
            move_down(board)
            downcheck = copy.deepcopy(board)
            board = copy.deepcopy(bak)
            if downcheck == upcheck == leftcheck == rightcheck : # Checking if next move is possible
                pyautogui.press('enter')
                input() # Prevent the shit thats made with listener
                clear_screen()
                print ("\033[31m### GAME OVER ###\033[0m")
                header = "\033[33mGame Statistics\033[0m"
                Ending = True # Flag the ending so the box change
                width = int(grid * 6) - 1
                center = " " * (int((width - 15) / 2)) # Space for center aligning
                print ("┌" + "─" * (width) + "┐") # Print the header for the box
                print("│" + center + header + center + "│")
                score_box()
                header = "\033[32mGame Board\033[0m"
                center = " " * (int((width - 10) / 2))
                print ("┌" + "─" * (width) + "┐")
                print("│" + center + header + center + " " + "│")
                print_board(board)

                # top scores check at the end
                if grid == 3 : 
                    filename = join(appdir, datadir, "topscores_3.txt")
                    top_score_check(score, filename)
                if grid == 4 : 
                    filename = join(appdir, datadir, "topscores_4.txt")
                    top_score_check(score, filename)
                if grid == 5 : 
                    filename = join(appdir, datadir, "topscores_5.txt")
                    top_score_check(score, filename)

                print_pattern()
                input ("Press a key to exit.")
                scape = True # Flag for not double check the new record
                pyautogui.press("F") # Key sequence to exit fast mode easily
                pyautogui.press("esc")
                pyautogui.press("enter")
                pyautogui.press("q")
                pyautogui.press("enter")
                pyautogui.press("enter")

def on_press(key): # Key press listener function
    global fast_input, preboard, board, mute, move_count, first_F, scape
    try: # Checking input possibilites
        if key.char.upper() == 'W':
            fast_input_fun("w")
        elif key.char.upper() == 'A':
            fast_input_fun("a")
        elif key.char.upper() == 'S':
            fast_input_fun("s")
        elif key.char.upper() == 'D':
            fast_input_fun("d")
        elif key.char.upper() == 'F':
            clear_screen()
            fast_input = False
            first_F = False
            scape = False
            pyautogui.press('esc')
        elif key.char.upper() == 'Z': # Restoring latest board
            clear_screen()
            move_count = move_count - 6 # Subtract one from the move count
            print ("\033[93mPress 'F' to exit fast input mode\033[0m")
            score_box()
            board = copy.deepcopy(preboard) 
            print_board(board)
            if not mute :
                play_sound('SFX1.wav') # Play the sound
            print("\033[32mloading Previous state complete\033[0m")
        elif key.char.upper() == 'M': # Mute/Unmute the sound in fast input mode
            if mute :
                mute = False
            else :
                mute = True
        else : # Error for anything else
            clear_screen()
            if not mute :
                play_sound('SFX2.wav')
            print ("\033[31mWrong input\033[0m")
            print ("\033[93mPress 'F' to exit fast input mode\033[0m")
            score_box()
            print_board(board)
    except AttributeError:
        pass

def on_release(key): # Function made for exiting fast mode
    if key == keyboard.Key.esc:
        print("\033[32mFast input mode is disabled\033[0m")
        return False

if set_board : # Set the starting board
    board = initialize_board()
    preboard = board
    place_random_tile(board)
    if grid == 5 : # Place one more random tiles for bigger board
        place_random_tile(board)

# Main game loop
while True:
    move_direction = ""
    if not fast_input :
        if not hide : # Input guide  
            print ("Hide input guides         => Enter 'H'")
            print ("Leave the game            => Enter 'Q'")
            print ("Save the game             => Enter 'O'")
            print ("Enter fast input mode     => Enter 'F'")
            if not mute :
                print ("Mute the sound            => Enter 'M'")
            if mute :
                print ("Unmute the sound          => Enter 'M'")
        else :
            print ("for input guides enter 'H'")
        if won :
            print("\033[33m*** You have won the game ***\033[0m")
        score_box()
        print_board(board)
    if fast_input: # Checking for fast input
        scoring = True
        if automute :
            mute = True
        hide = True
        if first_F : # Once you enter the fast input mode there is nothing this make the game consistent
            if won :
                print("\033[33m*** You have won the game ***\033[0m")
            print ("\033[93mPress 'F' to exit fast input mode\033[0m")
            score_box ()
            print_board(board)
            first_F = False
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: # Setup Listener
            listener.join()
    else :
        move_direction = input("\033[93mEnter move (W/A/S/D): \033[0m").upper() # Normal input
    
        valid_moves = "WASDZQOHMF"  # String containing all valid moves
        if move_direction not in valid_moves:
            clear_screen()
            print("Invalid move. Use W/A/S/D to play or H for input guide")
            continue

        if move_direction == "Q": # Breaking
            clear_screen()
            header = "\033[33mGame Statistics\033[0m"
            Ending = True # Flag for end screen
            width = int(grid * 6) - 1
            center = " " * (int((width - 15) / 2)) # Space for Center alignment
            print ("┌" + "─" * (width) + "┐")
            print("│" + center + header + center + "│") # Print the header for Stat box
            score_box() # Print modified box (with ending flag)
            header = "\033[32mGame Board\033[0m"
            center = " " * (int((width - 10) / 2))
            print ("┌" + "─" * (width) + "┐")
            print("│" + center + header + center + " " + "│")
            print_board(board)
            if not scape : # Check if its normal q or lose in fast input mode
                # Check for the top score before breaking
                if grid == 3 : 
                    filename = join(appdir, datadir, "topscores_3.txt")
                    top_score_check(score, filename)

                if grid == 4 : 
                    filename = join(appdir, datadir, "topscores_4.txt")
                    top_score_check(score, filename)

                if grid == 5 : 
                    filename = join(appdir, datadir, "topscores_5.txt")
                    top_score_check(score, filename)
            print_pattern()
            input("Press a key to exit.")
            break
        
        if move_direction == "O" : # Saving the current state to a savefile
            clear_screen()
            # Save Current game board and stats
            if grid == 3 :
                with open(join(appdir, datadir, "savefile3.txt"), 'w') as file :
                    file.write(str(board))
                filename = join(appdir, datadir, "topscores_3.txt")
                top_score_check(score, filename)
                with open(join(appdir, datadir, "save3score.txt"), 'w') as file :
                    data_string = ",".join([str(score), str(move_count), str(biggest_tile)])
                    file.write(data_string)

            if grid == 4 :
                with open(join(appdir, datadir, "savefile4.txt"), 'w') as file :
                    file.write(str(board))
                filename = join(appdir, datadir, "topscores_4.txt")
                top_score_check(score, filename)
                with open(join(appdir, datadir, "save4score.txt"), 'w') as file :
                    data_string = ",".join([str(score), str(move_count), str(biggest_tile)])
                    file.write(data_string)

            if grid == 5 :
                with open(join(appdir, datadir, "savefile5.txt"), 'w') as file :
                    file.write(str(board))
                filename = join(appdir, datadir, "topscores_5.txt")
                top_score_check(score, filename)
                with open(join(appdir, datadir, "save5score.txt"), 'w') as file :
                    data_string = ",".join([str(score), str(move_count), str(biggest_tile)])
                    file.write(data_string)
            
            print ("\033[32mSave complete\033[0m")
            con = ()
            if con != "y" or "n":
                con = input ("\033[93mDo you want to continue the game(y/n)?\033[0m").lower()
                if con == "n" :
                    header = "\033[33mGame Statistics\033[0m"
                    Ending = True
                    width = int(grid * 6) - 1
                    center = " " * (int((width - 15) / 2))
                    print ("┌" + "─" * (width) + "┐")
                    print("│" + center + header + center + "│")
                    score_box()
                    header = "\033[32mGame Board\033[0m"
                    center = " " * (int((width - 10) / 2))
                    print ("┌" + "─" * (width) + "┐")
                    print("│" + center + header + center + " " + "│")
                    print_board (board)
                    print_pattern()
                    input ("Press a key to exit.")
                    break
                elif con == "y":
                    clear_screen()
                    print("\033[32mContinue the game\033[0m")
                    continue 
                else : 
                    print ("\033[32mInvalid input. Continue the game...\033[0m")

        if not move_direction:  # Check for empty input (not move_direction)
            clear_screen()
            play_sound('SFX2.wav')
            print("\033[31mNo input! Please enter a move (W/A/S/D)\033[0m")
            continue
        
        if move_direction == "Z": # Restoring last move in the game
            clear_screen()
            move_count = move_count - 6
            board = copy.deepcopy(preboard) 
            if not mute:
                play_sound('SFX1.wav') # PLay the sound
            print("\033[32mloading Previous state complete\033[0m")
            continue

        if move_direction == "M" : # Muting and unmuting the sound if needed
            if mute :
                mute = False
                clear_screen()
                continue
            if not mute :
                mute = True
                clear_screen()
                continue
        
        if move_direction == "H" : # Hiding the input guides
            if not hide :
                hide = True
                clear_screen()
                continue
            if hide :
                hide = False
                clear_screen()
                continue
        
        if move_direction == "F": # Enable the flag to enter fast input mode
            fast_input = True
            clear_screen()
            first_F = True
            continue
        
        if score > 1000 : # Hide input guides after a while in the game
            hide = True

        GOcheckboard = copy.deepcopy(board) # Backing up the board before making the check for next move
        scoring = False # Flaging the scoring to False so it dont count
        if 0 not in board :
            # Making a board for every next possibility 
            move_up (board)
            boardW = copy.deepcopy(board)
            board = copy.deepcopy(GOcheckboard)

            move_down (board)
            boardS = copy.deepcopy(board)
            board = copy.deepcopy(GOcheckboard)

            move_left (board)
            boardA = copy.deepcopy(board)
            board = copy.deepcopy(GOcheckboard)

            move_right (board)
            boardD = copy.deepcopy(board)
            board = copy.deepcopy(GOcheckboard)

            # Check for the game over
            if boardW == boardA == boardD == boardS :
                clear_screen()
                print ("\033[31m### GAME OVER ###\033[0m")
                header = "\033[33mGame Statistics\033[0m"
                Ending = True
                width = int(grid * 6) - 1
                center = " " * (int((width - 15) / 2))
                print ("┌" + "─" * (width) + "┐")
                print("│" + center + header + center + "│")
                score_box()
                header = "\033[32mGame Board\033[0m"
                center = " " * (int((width - 10) / 2))
                print ("┌" + "─" * (width) + "┐")
                print("│" + center + header + center + " " + "│")
                print_board(board)

                # top scores check at the end
                if grid == 3 : 
                    filename = join(appdir, datadir, "topscores_3.txt")
                    top_score_check(score, filename)
                if grid == 4 : 
                    filename = join(appdir, datadir, "topscores_4.txt")
                    top_score_check(score, filename)
                if grid == 5 : 
                    filename = join(appdir, datadir, "topscores_5.txt")
                    top_score_check(score, filename)

                print_pattern()
                input("Press a key to exit.")
                break
            else :
                board = copy.deepcopy(GOcheckboard)

        valid_move_check = copy.deepcopy(board) # Checking if the move do anything or not
        scoring = False # Flaging score so it wont count
        move(board, move_direction)
        if board == valid_move_check : # Validate next move
            clear_screen()
            print ("\033[31myour move is invalid\033[0m")
            play_sound('SFX2.wav')
            board = copy.deepcopy(valid_move_check)
            continue
        else :
            board = copy.deepcopy(valid_move_check)

        preboard = copy.deepcopy(board) # Backup for restoring
        scoring = True # Flaging score so it count
        move(board, move_direction)
        place_random_tile(board)
        if not mute :
            play_sound('SFX1.wav') # Play the sound
        clear_screen() 