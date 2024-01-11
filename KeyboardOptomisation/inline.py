import curses
from KeyboardCharacterOptomiser import createWordFrequencyMap, createWordTries
from constants import prechosen, alphabet


def main(stdscr, allWordTries, frequencyMaps):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    inputStr = ""
    singleWordReplacedStr = ""
    prompt = "Start typing (press 'ESC' to exit): "

    stdscr.addstr(prompt)
    promptLength = len(prompt)

    prevWordLength = 0
    curWordLength = 0

    alternatives = []
    curAlternativeIndex = 1

    while True:
        charCode = stdscr.getch()
        char = chr(charCode)
        y, x = stdscr.getyx()
        updateScreen = False  # a flag to indicate if we need to update the screen

        if charCode == 27:  # ESC key
            break
        elif charCode == curses.KEY_UP:
            if curAlternativeIndex > 0 and curAlternativeIndex < len(alternatives):
                curAlternativeIndex -= 1
                inputStr = replaceWord(inputStr[:len(
                    inputStr)-1], prevWordLength, " ", alternatives[curAlternativeIndex])
                moveAmount = 0
                updateScreen = True

        elif charCode == curses.KEY_DOWN:
            if curAlternativeIndex >= 0 and curAlternativeIndex < len(alternatives) - 1:
                curAlternativeIndex += 1
                # print(alternatives, alternatives[curAlternativeIndex])
                inputStr = replaceWord(inputStr[:len(
                    inputStr)-1], prevWordLength, " ", alternatives[curAlternativeIndex])
                moveAmount = 0
                updateScreen = True

        elif charCode == curses.KEY_BACKSPACE or charCode == 127:
            if x > promptLength:
                inputStr = inputStr[:x - promptLength -
                                    1] + inputStr[x - promptLength:]
                updateScreen = True
                if curWordLength > 0:
                    curWordLength -= 1
                moveAmount = -1

        elif 33 <= charCode <= 126:  # Excluding space which has a charCode of 32
            if char not in prechosen:
                char = '%'
            inputStr = inputStr[:x - promptLength] + \
                char + inputStr[x - promptLength:]
            updateScreen = True
            curWordLength += 1
            moveAmount = 1

        elif charCode == 32:  # Handling space separately
            speltWord = inputStr[len(inputStr)-curWordLength:len(inputStr)]
            inputStr, singleWordReplacedStr, previousAlternatives = onSpace(allWordTries, frequencyMaps,
                                                                            inputStr, singleWordReplacedStr, curWordLength, char)
            # This is a very temporary fix, ideally we should look at storing these alternatives to avoid recomputation
            alternatives = [speltWord]
            alternatives += previousAlternatives
            alternatives.append(speltWord)
            curAlternativeIndex
            prevWordLength = curWordLength
            curWordLength = 0
            updateScreen = True
            moveAmount = 1

        # Update the screen if needed
        if updateScreen:
            stdscr.move(y, promptLength)
            stdscr.clrtoeol()
            stdscr.addstr(y, promptLength, inputStr)
            stdscr.move(y, x + moveAmount)

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()


def onSpace(allWordTries, frequencyMaps, inputStr, singleWordReplacedStr, curWordLength, char):
    if curWordLength == 0:
        inputStr += char
        singleWordReplacedStr += char

    else:
        # Perform single word replacement
        speltWord = inputStr[len(inputStr)-curWordLength:len(inputStr)]
        wordTrie = allWordTries[len(speltWord)]
        # Get all possible words, that match the spelt word
        alternatives = wordTrie.searchR(
            speltWord, alphabet - prechosen, prechosen)[1]
        # Check if single word replacement is possible
        replacedWord, replaced = wordTrie.singleWordReplacement(
            speltWord, prechosen)
        # If single word replacement did not occur
        singleWordReplacedStr += replacedWord + char
        if replaced == False:
            freqMap = frequencyMaps[len(speltWord)]
            alternatives = sorted(
                alternatives, key=lambda x: freqMap[x])
            if len(alternatives) > 0:
                replacedWord = alternatives[0]
            else:
                # Need to add some additional functionality here to handle the case where the word is not in wordlist
                pass

        inputStr = replaceWord(inputStr, curWordLength, char, replacedWord)
    return inputStr, singleWordReplacedStr, alternatives


def replaceWord(inputStr, curWordLength, char, replacedWord):
    beforeWord = inputStr[:len(inputStr)-curWordLength]
    inputStr = beforeWord + replacedWord + char
    return inputStr


if __name__ == "__main__":
    allWordTries = createWordTries()
    frequencyMaps = createWordFrequencyMap()
    curses.wrapper(lambda stdscr: main(stdscr, allWordTries, frequencyMaps))
