import csv, re, exrex # Need to install exrex
import pandas as pd
import seaborn as sns #need to install #scipy as well
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
#sns.set(style="ticks")
pattern2 = list(exrex.generate('[A-H][1-9]|[A-H][1][0-2]'))
with open('/home/chain-ed-reaction/project/python_programs/result-26_03_2020_09_23.csv' , 'r') as f:

    results_df = pd.read_csv(f, delimiter = '\t' )
    t0_results_df = results_df.iloc[[0]].values[0]
    normalized_values = results_df.sub(t0_results_df)
    num = 0

    cols = 12
    rows = len(pattern2) // cols + 1
    figsize = (20, 20)
    def trim_axs(axs, N):
#        """
#        Reduce *axs* to *N* Axes. All further Axes are removed from the figure.
#        """
        axs = axs.flat
        for ax in axs[N:]:
            ax.remove()
        return axs[:N]
    fig, axs = plt.subplots(nrows= rows, ncols= cols,  figsize=figsize)
    fig.subplots_adjust(hspace=1)
    fig.suptitle('Growth Analysis')
    axs = trim_axs(axs, len(pattern2))
    print(1)
    with PdfPages('result.pdf') as pdf:
        for ax, pattern2 in zip(axs, pattern2):
            ax.set_ybound(lower=0.00, upper=1.00)
            ax.set_xbound(lower=0, upper=144)
            #ax.set_aspect(aspect='equal', adjustable='box', anchor='C')
            #ax.set(xlim=(0, 144), ylim=(0.00, 1.00), aspect='equal', adjustable='box', anchor='C')
            print(2)
            ax.set_title('Well=%s' % str(pattern2))
            sns.set_style("whitegrid")
            sns.lineplot(data = normalized_values, x = 'Iteration', y = pattern2, ax=ax, size_norm="Normalize")
    plt.title('Growth Analysis') 
    plt.show(fig)
    
        
    pdf.savefig(fig)  # or you can pass a Figure object to pdf.savefig
    plt.close()
print("Done")