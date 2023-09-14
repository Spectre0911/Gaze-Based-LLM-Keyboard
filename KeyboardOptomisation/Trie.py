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

    def searchR(self, regex, B):
        words = []
        count = [0]

        def dfs(regex, currentWord, node):
            if not regex:
                if node.is_end_of_word:
                    count[0] += 1
                    words.append(''.join(currentWord))
                return

            char = regex[0]
            children = node.children

            if char == "_":
                inter = B.intersection(children)
                for child in inter:
                    dfs(regex[1:], currentWord + [child], children[child])
            elif char in children:
                dfs(regex[1:], currentWord + [char], children[char])

        dfs(list(regex), [], self.root)
        return (count, words)

    def spellSearch(self, regex, B):
        words = []

        def dfs(regex, currentWord, node):
            if not regex:  # Base case: If the regex is empty, add the currentWord to the list
                if node.is_end_of_word:
                    words.append(currentWord)
                return

            char = regex[0]
            children = node.children

            if char in B:
                inter = B.intersection(children)
                for child in inter:
                    dfs(regex[1:], currentWord + child, children[child])
            elif char not in children:
                return
            else:
                dfs(regex[1:], currentWord + char, children[char])

        dfs(regex, "", self.root)
        return words

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
