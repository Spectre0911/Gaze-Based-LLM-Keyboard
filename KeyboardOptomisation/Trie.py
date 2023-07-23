class TrieNode:
    def __init__(self):
        self.children = {}  # Hash map to store child nodes
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

    def searchR(self, regex):
        words = []

        def dfs(currentWord=""):
            node = self.root
            for char in regex:
                if char == "_":
                    for child in node.children:
                        dfs(currentWord + child)
                elif char not in node.children:
                    return
                else:
                    node = node.children[char]
            if node.is_end_of_word:
                words.append(currentWord)
        dfs()
        return words

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
