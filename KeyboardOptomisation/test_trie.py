from Trie import Trie
from constants import alphabet
def test_insert_and_search():
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") == True
    assert trie.search("app") == False

def test_spellWord():
    trie = Trie()
    charSet = set(['a', 'p', 'l', 'e'])
    assert trie.spellWord("apple", charSet) == "apple"
    assert trie.spellWord("orange", charSet) == "__a__e"

def test_searchR():
    trie = Trie()
    trie.insert("apple")
    trie.insert("pen")
    trie.insert("pea")
    trie.insert("peach")
    charSet = set(['a', 'p', 'l', 'e'])
    unknownCharacterSet = alphabet - charSet
    

    count, words = trie.searchR("apple", unknownCharacterSet, charSet)
    assert count[0] == 1
    assert "apple" in words

    count, words = trie.searchR("pe_", unknownCharacterSet, charSet)
    assert count[0] == 1
    assert "pen" in words
    assert "pea" not in words
