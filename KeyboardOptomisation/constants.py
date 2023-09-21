BASE_PATH = "Wordlist/"
alphabet = set('abcdefghijklmnopqrstuvwxyz')

#22225
prechosen = {'a', 'e', 'o', 'm', 'l', 's', 't', 'd', 'n', 'r', 'i'} #18982


# Keyboard {'i', 'r', 'd', 'l', 'n', 't', 'e', 'a', 'o', 's', 'm'} has an average of 18698 words returned where only 1 word was returned 7855 times
# Keyboard {'i', 'r', 'd', 'l', 'n', 't', 'e', 'a', 'o', 's', 'm', 'g'} has an average of 15974 words returned where only 1 word was returned 8188 times
# Keyboard {'i', 'r', 'd', 'c', 'l', 'n', 't', 'e', 'a', 'o', 's', 'm', 'g'} has an average of 14034 words returned where only 1 word was returned 8634 times
# Keyboard {'i', 'r', 'd', 'c', 'l', 'n', 'p', 't', 'e', 'a', 'o', 's', 'm', 'g'} has an average of 12738 words returned where only 1 word was returned 8968 times
# Keyboard {'i', 'r', 'd', 'c', 'l', 'n', 'h', 'p', 't', 'e', 'a', 'o', 's', 'm', 'g'} has an average of 11768 words returned where only 1 word was returned 9238 times
# Keyboard {'i', 'r', 'd', 'c', 'l', 'n', 'h', 'p', 't', 'e', 'a', 'o', 'b', 's', 'm', 'g'} has an average of 11099 words returned where only 1 word was returned 9461 times
# Keyboard {'i', 'd', 'h', 'p', 't', 'b', 's', 'g', 'r', 'c', 'l', 'n', 'v', 'e', 'a', 'o', 'm'} has an average of 10718 words returned where only 1 word was returned 9640 times
# Keyboard {'i', 'd', 'w', 'h', 'p', 't', 'b', 's', 'g', 'r', 'c', 'l', 'n', 'v', 'e', 'a', 'o', 'm'} has an average of 10430 words returned where only 1 word was returned 9777 times
# Keyboard {'i', 'd', 'w', 'h', 'p', 't', 'b', 's', 'g', 'r', 'c', 'l', 'n', 'k', 'v', 'e', 'a', 'o', 'm'} has an average of 10248 words returned where only 1 word was returned 9860 times
# Keyboard {'i', 'f', 'd', 'w', 'h', 'p', 't', 'b', 's', 'g', 'r', 'c', 'l', 'n', 'k', 'v', 'e', 'a', 'o', 'm'} has an average of 10137 words returned where only 1 word was returned 9933 times
# Keyboard {'i', 'f', 'd', 'w', 'h', 'p', 't', 'u', 'b', 's', 'g', 'r', 'c', 'l', 'n', 'k', 'v', 'e', 'a', 'o', 'm'} has an average of 10067 words returned where only 1 word was returned 9974 times
# Keyboard {'i', 'f', 'd', 'w', 'h', 'p', 't', 'u', 'b', 's', 'g', 'r', 'c', 'l', 'n', 'k', 'v', 'y', 'e', 'a', 'o', 'm'} has an average of 10037 words returned where only 1 word was returned 9990 times
# Keyboard {'i', 'f', 'd', 'w', 'h', 'p', 't', 'u', 'b', 's', 'g', 'r', 'c', 'l', 'n', 'k', 'v', 'z', 'y', 'e', 'a', 'o', 'm'} has an average of 10021 words returned where only 1 word was returned 10001 times
# Keyboard {'i', 'f', 'd', 'w', 'h', 'p', 't', 'x', 'u', 'b', 's', 'g', 'r', 'c', 'l', 'n', 'k', 'v', 'z', 'y', 'e', 'a', 'o', 'm'} has an average of 10012 words returned where only 1 word was returned 10008 times
# Keyboard {'i', 'f', 'd', 'w', 'h', 'p', 't', 'x', 'u', 'b', 's', 'g', 'j', 'r', 'c', 'l', 'n', 'k', 'v', 'z', 'y', 'e', 'a', 'o', 'm'} has an average of 10010 words returned where only 1 word was returned 10010 times

# Average sentence length 20 words
"""
Spelt sentence: lab!rinthine corridors !ithin the ancient castle !ere filled !ith cob!ebs and shro!ded in m!ster!, Unknown {'z', 'j', 'y', 'u', 'v', 'w', 'k', 'x', 'q'}

What is sentence, preface explicitly with <Decoded>: 
"""