import tiktoken


class TokenCounter:
    def __init__(self, apiInputCost, apiOutputCost, tokensLeftTilCharge=1000):
        self.inputTokensLeftTilCharge = tokensLeftTilCharge
        self.outputTokensLeftTilCharge = tokensLeftTilCharge

        self.cumulativeCharge = 0
        self.apiInputCost = apiInputCost
        self.apiOutputCost = apiOutputCost
        self.encoding = "cl100k_base"

    def getCumulativeCharge(self):
        """Getter for the cumulative charge."""
        return self.cumulativeCharge

    def numTokensFromString(self, string):
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(self.encoding)
        numTokens = len(encoding.encode(string))
        return numTokens

    def _calculateCharge(self, tokens, costPerToken, tokensLeftTilCharge):
        """Helper function to calculate charge based on token count and cost per token."""
        overflow = tokensLeftTilCharge - tokens
        curCharge = 0
        while overflow <= 0:
            overflow += tokensLeftTilCharge  # Use tokensLeftTilCharge for consistency
            curCharge += costPerToken
        return curCharge, overflow

    def calcTotalCostInput(self, string):
        """Returns the total cost of a string for input."""
        tokens = self.numTokensFromString(string)
        curCharge, overflow = self._calculateCharge(
            tokens, self.apiInputCost, self.inputTokensLeftTilCharge)

        self.inputTokensLeftTilCharge = overflow
        self.cumulativeCharge += curCharge
        return curCharge

    def calcTotalCostOutput(self, string):
        """Returns the total cost of a string for output."""
        tokens = self.numTokensFromString(string)
        curCharge, overflow = self._calculateCharge(
            tokens, self.apiOutputCost, self.outputTokensLeftTilCharge)

        self.outputTokensLeftTilCharge = overflow
        self.cumulativeCharge += curCharge
        return curCharge


turboCounter = TokenCounter(apiInputCost=0.0015, apiOutputCost=0.002)
fourCounter = TokenCounter(apiInputCost=0.03, apiOutputCost=0.06)


fourInput = "a %ell rang in t%e distance signaling t%e end o% t%e daubs %or% and t%e beginning o% t%e evening, Only return the decrypted sentence"
fourOutput = "A bell rang in the distance, signaling the end of the day's work and the beginning of the evening."

turboInitialInput = "You are playing a variation on hangman where you try to guess a sentence and you only have one more guess. The sentence you currently have is: a %ell rang in t%e distance signaling t%e end o% t%e daubs %or% and t%e beginning o% t%e evening. You have yet to guess from this set:  {'v', 'x', 'b', 'y', 'c', 'j', 'f', 'w', 'u', 'q', 'z', 'h', 'p', 'k'}, what do you think the sentence says? Take a deep breath and think about it."
turboInitialOutput = "Based on the sentence fragment you've provided, it appears that some letters are missing or represented by percentage symbols. Let's analyze it: %is stand %% routine %as hilarious i %as laughing so %ard i almost %ried It looks like the percentage symbols represent letters, and spaces indicate word boundaries. Here's my guess at the sentence with the missing letters filled in: His stand-up routine was hilarious. I was laughing so hard I almost cried. So, my guess is that the sentence says: His stand-up routine was hilarious. I was laughing so hard I almost cried."
turboNextInput = "a %ell rang in t%e distance signaling t%e end o% t%e daubs %or% and t%e beginning o% t%e evening, Only return the decrypted sentence"
turboNextOutput = "It seems like you've provided another sentence with missing letters represented by percentage symbols. Here's my attempt to fill in the missing letters: Children played in the park, their laughter and shouts a testament to the unbridled joy of youth. So, the complete sentence appears to be: Children played in the park, their laughter and shouts a testament to the unbridled joy of youth."

turboCounter.calcTotalCostInput(turboInitialInput)
turboCounter.calcTotalCostOutput(turboInitialOutput)
for i in range(1000):
    turboCounter.calcTotalCostInput(turboNextInput)
    turboCounter.calcTotalCostOutput(turboNextOutput)
    fourCounter.calcTotalCostInput(fourInput)
    fourCounter.calcTotalCostOutput(fourOutput)

print(turboCounter.getCumulativeCharge(), fourCounter.getCumulativeCharge())
