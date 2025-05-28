import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd

# Internal import 
import utils

def plot(
    df_all, 
    columns,
    dir_graph,
    level=None, 
    xlabel=None, 
    ylabel=None,
    ylim=None, 
    figsize=(16, 9), 
    width=0.3, 
    yscale="log",
    title=None,
    show=True,
    show_values=True,
    show_errors=True,
    save_formats=("svg", "png")
):

    n_variants = len(df_all)
    n_columns = len(columns)

    x = np.arange(n_variants)

    fig, ax = plt.subplots(figsize=figsize)

    palette = sns.color_palette("tab10", n_colors=n_columns)

    for i, (val_col, err_col, label) in enumerate(columns):
        values = df_all[val_col]
        errors = df_all[err_col]

        bars = ax.bar(
            x + (i - (n_columns - 1) / 2) * width,
            values,
            width=width,
            yerr=errors if show_values else None,
            label=label,
            color=palette[i],
            error_kw={"capsize": 5, "ecolor": "red", "elinewidth": 2}
        )

        # values
        if show_values:
            for bar, value in zip(bars, values):
                # height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    2e-3, # values position
                    f"{value:.3f}",    
                    ha="center",
                    va="center",
                    fontsize="large",
                    color="black",
                    fontweight="bold",
                )

        # error
        if show_errors:            
            for bar, value, error in zip(bars, values, errors):
                top = value + error
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    top * 1.1,  # error position
                    f"±{error:.3f}",
                    ha="center",
                    va="bottom",
                    fontsize="large",
                    color="red",
                )

    ax.set_xticks(x)
    ax.set_xticklabels(df_all.index.to_list(), rotation=0, ha="center")

    ax.set_xlabel(xlabel, fontsize="large")
    ax.set_ylabel(ylabel, fontsize="large")
    ax.set_title(title, fontsize="xx-large")

    ax.set_yscale(yscale)
    
    if yscale == "log":
        yticks = np.logspace(0, 10, num=10 + 1, base=10)
        ax.set_yticks(yticks)
    
    if ylim:
        ax.set_ylim(*ylim)

    ax.set_xlim(x[0] - 0.5, x[-1] + 0.5)

    ax.tick_params(axis="x", labelsize="x-large")
    ax.tick_params(axis="y", labelsize="x-large")

    ax.legend(loc="upper right", fontsize="x-large")

    ax.grid(True, axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

    plt.tight_layout()

    filename = f"level_{level}" if level else "all_level"

    for ext in save_formats:
        file = f"{dir_graph}/{filename}.{ext}"
        plt.savefig(file, format=ext)    
        print(f"Graph {file} was created")

    if show:
        plt.show()
    else:
        plt.close()


def generate_plots_from_csv(
    csv_path,
    dir_graph,
    variants_dict,
    columns,
    ylabel="Tempo (ms)",
    xlabel="Algoritmos",
    yscale="log",
    figsize=(16, 9),
    save_formats=("svg", "png"),
    show=True,
    show_values=True,
    show_erros=True,
):
    """
    Generates bar plots with error bars from a benchmark CSV file.

    For each level defined in the variants_dict, this function creates a bar plot comparing
    different variants, with optional error bars and value annotations.

    Args:
        csv_path (str): Path to the CSV file containing the benchmark data.
        dir_graph (str): Directory where the plots will be saved.
        variants_dict (dict): Dictionary mapping levels to lists of variants.
        columns (list[tuple]): List of tuples (value_column, error_column, label) representing 
            the data to plot.
        ylabel (str, optional): Label for the Y-axis. Defaults to "Time (ms)".
        xlabel (str, optional): Label for the X-axis. Defaults to "Algorithms".
        yscale (str, optional): Scale for the Y-axis, either "log" or "linear". Defaults to "log".
        figsize (tuple, optional): Figure size in inches. Defaults to (16, 9).
        save_formats (tuple, optional): File formats to save (e.g., ("svg", "png")). Defaults to ("svg", "png").
        show (bool, optional): If True, displays the plots. Defaults to True.
        show_values (bool, optional): If True, displays values on top of the bars. Defaults to True.
        show_erros (bool, optional): If True, displays error values. Defaults to True.
    """
    
    df = pd.read_csv(csv_path, index_col="variant")
    variants_by_level = utils.get_variants_by_level(df, variants_dict)

    for level, variants in variants_by_level.items():
        df_subset = df.loc[variants]

        plot(
            df_subset,
            columns=columns,
            level=level,
            dir_graph=dir_graph,
            yscale=yscale,
            ylabel=ylabel,
            ylim=(1e-3, 1e4),
            figsize=figsize,
            title=f"Nível {level}",
            show=show,
            show_values=show_values,
            show_errors=show_erros,
            save_formats=save_formats
        )
