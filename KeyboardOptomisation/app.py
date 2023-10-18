import curses
from KeyboardCharacterOptomiser import createWordFrequencyMap, createWordTries
from constants import prechosen, alphabet


def main(stdscr, allWordTries, frequencyMaps):
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
                if wordLength > 0:
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

            # If wordLength is 0, just type a space
            if wordLength == 0:
                inputStr += char
            else:
                # Perform single word replacement
                speltWord = inputStr[len(inputStr)-wordLength:len(inputStr)]
                wordTrie = allWordTries[len(speltWord)]
                # Get all possible words, that match the spelt word
                alternatives = wordTrie.searchR(
                    speltWord, alphabet - prechosen, prechosen)[1]
                # Check if single word replacement is possible
                replacedWord, replaced = wordTrie.singleWordReplacement(
                    speltWord, prechosen)
                # If single word replacement did not occur
                if replaced == False:
                    freqMap = frequencyMaps[len(speltWord)]
                    alternatives = sorted(
                        alternatives, key=lambda x: freqMap[x])
                    if len(alternatives) > 0:
                        replacedWord = alternatives[0]
                    else:
                        # Need to add some additional functionality here to handle the case where the word is not in wordlist
                        pass

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
    frequencyMaps = createWordFrequencyMap()
    curses.wrapper(lambda stdscr: main(stdscr, alllWordTries, frequencyMaps))
