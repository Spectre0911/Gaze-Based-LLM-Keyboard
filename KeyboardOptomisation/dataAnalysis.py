from matplotlib.lines import Line2D
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df358 = pd.read_csv('./Data/358.csv')
df359 = pd.read_csv('./Data/359.csv')
df350 = pd.read_csv('./Data/350.csv')

nttdf358 = pd.read_csv('./Data/ntt358.csv')
nttdf359 = pd.read_csv('./Data/ntt359.csv')
nttdf350 = pd.read_csv('./Data/ntt350.csv')

dfttft359 = pd.read_csv('./Data/ttft359.csv')

dfft359 = pd.read_csv('./Data/ft359.csv')

df458 = pd.read_csv(
    './Data/458.csv')
df459 = pd.read_csv(
    './Data/459.csv')
df450 = pd.read_csv(
    './Data/450.csv')

ttdata35 = [nttdf358, nttdf359, nttdf350]

data35 = [df358, df359, df350]
data45 = [df458, df459, df450]

temp = [dfttft359, dfft359, df459]

fullData = [data35, temp]

global_min = min(df["GPTScore"].min() for data in fullData for df in data)
global_max = max(df["GPTScore"].max() for data in fullData for df in data)

models = ['3.5', '4.5']
letter_counts = [8, 9, 10]
data_stats = []  # Store the mean, std, and labels for plotting

for model_idx, (model, data) in enumerate(zip(models, fullData)):
    for letter_idx, (letterCount, df) in enumerate(zip(letter_counts, data)):
        meanVal = df["GPTScore"].mean()
        stdVal = df["GPTScore"].std()
        print(model, meanVal, stdVal, letterCount)
        label = f"{model}-{letterCount}"
        data_stats.append((meanVal, stdVal, label))


color_palette = plt.cm.Set2(np.linspace(0, 1, len(letter_counts)))
color_map = {model: color for model, color in zip(models, color_palette)}

fig, ax = plt.subplots(figsize=(12, 12))  # Adjust the figsize as necessary
ax.patch.set_alpha(0)
fig.patch.set_alpha(0)

# Positions of the bars on the x-axis
positions = np.arange(len(data_stats))


for idx, (mean, std, label) in enumerate(data_stats):
    # Extract model from label for color mapping
    model, _ = label.split('-')
    ax.bar(idx, mean, yerr=std, label=model if idx < len(models)
           else "", color=color_map[model], capsize=5, alpha=0.75)

ax.set_ylim(bottom=0.8)

# Add some final touches to the plot
ax.set_ylabel('Sentence accuracy', fontsize=14)
ax.set_xlabel('Letter Count', fontsize=14)
ax.set_title('Sentence accuracy by model and letter count', fontsize=14)
ax.set_xticks(positions)
ax.set_xticklabels([stat[2].split("-")[1]
                   for stat in data_stats],  ha="right",  fontsize=14)


legend_elements = [Line2D([0], [0], color=color_map[model],
                          lw=4, label=f'Model: {model}') for model in models]
ax.legend(handles=legend_elements, title='Legend',
          bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=14)


fig.savefig('transparent_background.png',
            transparent=True, bbox_inches='tight')

plt.yticks(np.arange(0.8, 1.05, 0.01), fontsize=14)
plt.tight_layout()
plt.show()
