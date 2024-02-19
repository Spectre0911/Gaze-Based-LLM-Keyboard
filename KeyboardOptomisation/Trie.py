from constants import BASE_PATH, alphabet, prechosen


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def singleWordReplacement(self, speltWord, keyboard):
        searchRes = self.searchR(
            speltWord, keyboard)
        wordCount = searchRes[0][0]
        words = searchRes[1]
        if wordCount == 1:
            return (words[0], True)
        return (speltWord, False)

    def spellWord(self, word, characterSet):
        """
        Spells the word with the available characters in the character set

        Args:
            word (String): A word within the wordlist
            characterSet (Set): A set of characters representing the available characters on the keyboard

        Returns:
            _type_: _description_
        """
        normalisedWord = ""
        normalisedWord = "".join(
            [c if c in characterSet else "%" for c in word])
        return normalisedWord

    def searchR(self, word, characterSet):
        """
        Searches for the word in the trie recursively, and returns the words that match the the normalised word and the number of them

        Args:
            word (String): The word to be searched for
            characterSet (String): The characters that can be used

        Returns:
            (Int, List): (Number of words that match the normalised word, List of words that match the normalised word)
        """
        words = []
        count = [0]

        def dfs(word, currentWord, node):
            if not word:
                if node.is_end_of_word:
                    count[0] += 1
                    words.append(''.join(currentWord))
                return

            char = word[0]
            children = node.children

            if char == "%":
                nextWord = word[1:]
                for child in children:
                    if child not in characterSet:
                        dfs(nextWord, currentWord + [child], children[child])
            elif char in children:
                dfs(word[1:], currentWord + [char], children[char])

        dfs(self.spellWord(word, characterSet), [], self.root)
        return (count, words)
