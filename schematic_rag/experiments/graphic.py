# experiments/graphic.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_for_article():
    df = pd.read_csv('experiments/results/results_history.csv')
    
    # 1. Grafic: Evoluția Accuracy & Runtime
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Plot Accuracy
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Accuracy (1.0 = 100%)', color='navy')
    ax1.plot(df.index, df['comp_accuracy'], color='navy', marker='o', linewidth=2, label='Comp. Accuracy')
    ax1.set_ylim(0, 1.1)
    
    # Plot Runtime pe axa secundară
    ax2 = ax1.twinx()
    ax2.set_ylabel('Runtime (seconds)', color='darkred')
    ax2.bar(df.index, df['runtime_sec'], alpha=0.2, color='darkred', label='Runtime')
    
    plt.title('Framework Performance: Accuracy vs. Computational Cost')
    fig.tight_layout()
    plt.savefig('experiments/results/accuracy_runtime_chart.png', dpi=300)
    print("✅ Grafic salvat în: experiments/results/accuracy_runtime_chart.png")

if __name__ == "__main__":
    plot_for_article()