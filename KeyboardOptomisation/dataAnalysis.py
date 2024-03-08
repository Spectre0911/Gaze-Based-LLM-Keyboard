from matplotlib.lines import Line2D
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df358 = pd.read_csv('./Data/3.5-turbo-1106-8-letter.csv')
df359 = pd.read_csv('./Data/3.5-turbo-1106-9-letter.csv')
df350 = pd.read_csv('./Data/3.5-turbo-1106-10-letter.csv')

df458 = pd.read_csv(
    './Data/gpt-4-0125-preview-8-letter.csv')
df459 = pd.read_csv(
    './Data/gpt-4-0125-preview-9-letter.csv')
df450 = pd.read_csv(
    './Data/gpt-4-0125-preview-10-letter.csv')


data35 = [df358, df359, df350]
data45 = [df458, df459, df450]
fullData = [data35, data45]

global_min = min(df["GPTScore"].min() for data in fullData for df in data)
global_max = max(df["GPTScore"].max() for data in fullData for df in data)

models = ['3.5', '4.5']
letter_counts = [8, 9, 10]
data_stats = []  # Store the mean, std, and labels for plotting

for model_idx, (model, data) in enumerate(zip(models, fullData)):
    for letter_idx, (letterCount, df) in enumerate(zip(letter_counts, data)):
        meanVal = df["GPTScore"].mean()
        stdVal = df["GPTScore"].std()
        stdVal = df["GPTScore"].std()

        print(model_idx, meanVal, stdVal)

        label = f"{model}-{letterCount}"
        data_stats.append((meanVal, stdVal, label))


color_palette = plt.cm.Set2(np.linspace(0, 1, len(letter_counts)))
color_map = {letter_count: color for letter_count,
             color in zip(letter_counts, color_palette)}

fig, ax = plt.subplots(figsize=(12, 12))  # Adjust the figsize as necessary
ax.patch.set_alpha(0)
fig.patch.set_alpha(0)

# Positions of the bars on the x-axis
positions = np.arange(len(data_stats))

for idx, (mean, std, label) in enumerate(data_stats):
    # Extract letter count from label for color mapping
    _, letter_count_str = label.split('-')
    letter_count = int(letter_count_str)
    ax.bar(idx, mean, yerr=std, label=label if idx % len(letter_counts)
           == 0 else "", color=color_map[letter_count], capsize=5, alpha=0.75)

# Add some final touches to the plot
ax.set_ylabel('GPTScore')
ax.set_title('GPTScore by Model and Letter Count')
ax.set_xticks(positions)
ax.set_xticklabels([stat[2] for stat in data_stats], rotation=45, ha="right")

legend_elements = [Line2D([0], [0], color=color_map[letter_count], lw=4,
                          label=f'Letters: {letter_count}') for letter_count in letter_counts]
ax.legend(handles=legend_elements, title='Legend',
          bbox_to_anchor=(1.05, 1), loc='upper left')

fig.savefig('transparent_background.png',
            transparent=True, bbox_inches='tight')

plt.yticks(np.arange(0, 1.1, 0.05))
plt.tight_layout()
plt.show()
