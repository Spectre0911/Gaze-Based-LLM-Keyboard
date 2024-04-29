from matplotlib.lines import Line2D
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# GPT3.5 with thinking time
# ttdf359 = pd.read_csv('./Data/tt359.csv')

# GPT3.5 without thinking time
nttdf359 = pd.read_csv('./Data/ntt359.csv')

# GPT 4 with thinking time
ttdf459 = pd.read_csv('./Data/tt459.csv')

# GPT 4 without thinking time
nttdf459 = pd.read_csv('./Data/ntt459.csv')

# Alternative System prompt
as359 = pd.read_csv('./Data/359AS.csv')

# First prompt
fp359 = pd.read_csv('./Data/359FP.csv')

# First prompt 459
fp459 = pd.read_csv('./Data/459FP.csv')

# Fine tuned 359
ft359 = pd.read_csv('./Data/359FT.csv')

# Fine tuned mackenzie modle
ft359N = pd.read_csv('./Data/359FTN.csv')

data = [ttdf459, nttdf459, ft359]

types = ["Simple", "Colloquial", "Descriptive", "Complex", "Random"]
row_indices = {
    "Simple": (0, 19),          # Rows 0-19 (20 rows)
    "Colloquial": (20, 39),     # Rows 20-39 (20 rows)
    "Descriptive": (40, 59),    # Rows 40-59 (20 rows)
    "Complex": (60, 79),        # Rows 60-79 (20 rows)
    "Random": (80, 99)          # Rows 80-99 (20 rows)
}

for df in data:
    print("-------------------------------")
    print(df["GPTScore"].mean())
    print(df["GPTScore"].std())
    for type in types:
        # Slicing the dataframe according to the type
        start_idx, end_idx = row_indices[type]
        subset_df = df.iloc[start_idx:end_idx+1]

        # Computing statistics
        meanVal = subset_df["GPTScore"].mean()
        stdVal = subset_df["GPTScore"].std()

        # Printing results for each type
        # print(f"{type}: Mean={meanVal}, Std={stdVal}")
