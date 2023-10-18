import curses
from KeyboardCharacterOptomiser import createWordTries
from constants import prechosen


def main(stdscr, allWordTries):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    inputStr = ""
    stdscr.addstr("Start typing (press 'ESC' to exit): ")
    promptLength = len("Start typing (press 'ESC' to exit): ")
    wordLength = 0
    while True:
        charCode = stdscr.getch()
        y, x = stdscr.getyx()
        updateScreen = False  # a flag to indicate if we need to update the screen

        if charCode == 27:  # ESC key
            break
        elif charCode == curses.KEY_BACKSPACE or charCode == 127:
            if x > promptLength:
                inputStr = inputStr[:x - promptLength -
                                    1] + inputStr[x - promptLength:]
                updateScreen = True
                wordLength -= 1
                moveAmount = -1
        elif 33 <= charCode <= 126:  # Excluding space which has a charCode of 32
            char = chr(charCode)
            if char not in prechosen:
                char = '%'
            wordLength += 1
            inputStr = inputStr[:x - promptLength] + \
                char + inputStr[x - promptLength:]
            updateScreen = True
            moveAmount = 1
        elif charCode == 32:  # Handling space separately
            char = chr(charCode)
            # NEED TO CHECK THIS LINE FOR DELETION BUG ERRORS
            word = inputStr[len(inputStr)-wordLength:len(inputStr)]
            replacedWord = allWordTries[len(word)].singleWordReplacement(
                word, prechosen)
            beforeWord = inputStr[:len(inputStr)-wordLength]
            inputStr = beforeWord + replacedWord + char
            wordLength = 0
            updateScreen = True
            moveAmount = 1

        # Update the screen if needed
        if updateScreen:
            stdscr.addstr(y, promptLength, inputStr + " ")
            stdscr.move(y, x + moveAmount)

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()


if __name__ == "__main__":
    alllWordTries = createWordTries()
    curses.wrapper(lambda stdscr: main(stdscr, alllWordTries))
