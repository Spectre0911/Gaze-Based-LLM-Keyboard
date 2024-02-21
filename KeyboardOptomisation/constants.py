BASE_PATH = "./Wordlist/"
alphabet = set('abcdefghijklmnopqrstuvwxyz')

# prechosen = {'l', 'i', 's', 't', 'n', 'a', 'r', 'e'}
# prechosen = {'a', 'd', 'e', 'i', 'l', 'n', 'o', 'r', 's', 't'}

prechosen = {'a', 't', 'r', 'l', 'e', 's', 'o', 'n'}

# Keyboard {'i', 's', 't', 'a', 'l', 'e', 'n', 'r'} has an average of 46793 words returned where only 1 word was returned 6444 times
# Keyboard {'i', 's', 't', 'o', 'a', 'l', 'e', 'n', 'r'} has an average of 30957 words returned where only 1 word was returned 6972 times
# Keyboard {'i', 's', 't', 'o', 'd', 'a', 'l', 'e', 'n', 'r'} has an average of 23493 words returned where only 1 word was returned 7478 times
# Keyboard {'i', 's', 't', 'o', 'd', 'a', 'l', 'e', 'n', 'm', 'r'} has an average of 19097 words returned where only 1 word was returned 7921 times
# Keyboard {'i', 's', 't', 'p', 'o', 'd', 'a', 'l', 'e', 'n', 'm', 'r'} has an average of 16148 words returned where only 1 word was returned 8303 times
# Keyboard {'b', 'i', 's', 't', 'p', 'o', 'd', 'a', 'l', 'e', 'n', 'm', 'r'} has an average of 14205 words returned where only 1 word was returned 8669 times
# Keyboard {'b', 'i', 's', 't', 'p', 'o', 'd', 'h', 'a', 'l', 'e', 'n', 'm', 'r'} has an average of 12804 words returned where only 1 word was returned 8970 times
# Keyboard {'b', 'i', 's', 't', 'p', 'o', 'd', 'h', 'a', 'g', 'l', 'e', 'n', 'm', 'r'} has an average of 11863 words returned where only 1 word was returned 9209 times
# Keyboard {'b', 'i', 's', 't', 'p', 'o', 'd', 'h', 'a', 'g', 'l', 'e', 'n', 'c', 'm', 'r'} has an average of 11192 words returned where only 1 word was returned 9456 times
# Keyboard {'b', 't', 'p', 'h', 'g', 'a', 'w', 'i', 's', 'o', 'd', 'l', 'e', 'n', 'c', 'm', 'r'} has an average of 10769 words returned where only 1 word was returned 9611 times
# Keyboard {'b', 't', 'p', 'h', 'g', 'a', 'v', 'w', 'i', 's', 'o', 'd', 'l', 'e', 'n', 'c', 'm', 'r'} has an average of 10453 words returned where only 1 word was returned 9751 times
# Keyboard {'b', 't', 'p', 'h', 'y', 'g', 'a', 'v', 'w', 'i', 's', 'o', 'd', 'l', 'e', 'n', 'c', 'm', 'r'} has an average of 10259 words returned where only 1 word was returned 9839 times
# Keyboard {'b', 't', 'p', 'h', 'y', 'g', 'a', 'v', 'k', 'w', 'i', 's', 'o', 'd', 'l', 'e', 'n', 'c', 'm', 'r'} has an average of 10138 words returned where only 1 word was returned 9910 times
# Keyboard {'b', 't', 'p', 'h', 'y', 'g', 'a', 'v', 'k', 'w', 'i', 's', 'o', 'd', 'l', 'e', 'n', 'c', 'm', 'r', 'f'} has an average of 10061 words returned where only 1 word was returned 9964 times
# Keyboard {'b', 't', 'p', 'h', 'y', 'g', 'a', 'v', 'k', 'w', 'i', 's', 'o', 'd', 'l', 'e', 'n', 'c', 'm', 'r', 'u', 'f'} has an average of 10025 words returned where only 1 word was returned 9992 times
# Keyboard {'b', 't', 'p', 'h', 'y', 'g', 'a', 'j', 'v', 'k', 'w', 'i', 's', 'o', 'd', 'l', 'e', 'n', 'c', 'm', 'r', 'u', 'f'} has an average of 10012 words returned where only 1 word was returned 10004 times
# Keyboard {'b', 't', 'p', 'h', 'y', 'g', 'a', 'j', 'v', 'k', 'w', 'i', 's', 'o', 'd', 'l', 'e', 'n', 'c', 'm', 'x', 'r', 'u', 'f'} has an average of 10008 words returned where only 1 word was returned 10008 times
# Keyboard {'b', 't', 'p', 'h', 'y', 'g', 'a', 'j', 'q', 'v', 'k', 'w', 'i', 's', 'o', 'd', 'l', 'e', 'n', 'c', 'm', 'x', 'r', 'u', 'f'} has an average of 10008 words returned where only 1 word was returned 10008 times
