import curses
from constants import alphabet, prechosen, BASE_PATH


def main(stdscr):
    # Do not display characters pressed by user
    curses.noecho()
    # Character-at-a-time input
    curses.cbreak()
    # Enables keypad mode to capture function keys, arrow keys, etc.
    stdscr.keypad(True)

    print("Start typing (press 'ESC' to exit): ", end="", flush=True)

    while True:
        char = stdscr.getch()
        # Check if it's the 'ESC' key to exit
        if char == 27:
            break
        # Handle backspace or delete key
        elif char == curses.KEY_BACKSPACE or char == 127:
            y, x = stdscr.getyx()  # Get current cursor position
            stdscr.move(y, max(x - 1, 0))  # Move cursor back by one
            stdscr.addch(' ')  # Display space to "delete" character
            stdscr.move(y, max(x - 1, 0))  # Move cursor back again
        else:
            stdscr.addch(char)
        stdscr.refresh()

    # Restore terminal settings
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()


curses.wrapper(main)
