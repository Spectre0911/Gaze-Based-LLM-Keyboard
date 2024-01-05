import matplotlib.pyplot as plt
import numpy as np
from scipy.special import comb


class GraphPlotting:
    def wordCountOverKeyboardLength(self):
        keyboardLength = [i for i in range(8, 27)]
        wordCountReturned = [46793, 30957, 23493, 19097, 16148, 14205, 12804, 11863,
                             11192, 10769, 10453, 10259, 10138, 10061, 10025, 10012, 10008, 10008, 10008]
        singleWordReturned = [6444, 6972, 7478, 7921, 8303, 8669, 8970, 9209,
                              9456, 9611, 9751, 9839, 9910, 9964, 9992, 10004, 10008, 10008, 10008]

        width = 0.35  # the width of the bars
        ind = np.arange(len(keyboardLength))  # the label locations

        _, ax = plt.subplots(figsize=(10, 5))
        ax.bar(ind, wordCountReturned, width,
               label='Total number of matches returned', alpha=1)
        ax.bar(ind, singleWordReturned, width,
               label='Single matches returned', alpha=1)

        y_ticks = np.arange(0, 50000, 5000)
        ax.set_yticks(y_ticks)

        ax.set_xticks(ind)
        ax.set_xticklabels(keyboardLength)
        ax.set_title(
            'Matches returned over keyboard length for a sample size of 10000')

        ax.set_ylabel('Number of matches returned')
        ax.set_xlabel('Number of keys on keyboard')
        ax.legend()

        plt.show()

    def keyboardBruteForce(self, n):
        nValues = [i for i in range(9, 27)]
        print(nValues, comb(n, 1))
        nckValues = [comb(n, k) for k in range(1, 19)]

        width = 0.35  # the width of the bars
        ind = np.arange(len(nValues))  # the label locations

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(ind, nckValues, width, label='Number of configurations', alpha=1)

        # Set y-axis to logarithmic scale
        ax.set_yscale('log')

        ax.set_xticks(ind)
        ax.set_xticklabels(nValues)
        ax.set_title(f'Graph of nCk for n = {n} (Logarithmic Scale)')

        ax.set_ylabel('Number of configurations (Log Scale)')
        ax.set_xlabel('k (Number of characters)')

        plt.show()


plotter = GraphPlotting()
plotter.wordCountOverKeyboardLength()
# plotter.keyboardBruteForce(18)
