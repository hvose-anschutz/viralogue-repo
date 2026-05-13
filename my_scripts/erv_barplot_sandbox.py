#!/usr/bin/env python3

"""Makes a barplot of ERV family and species."""

import colorsys
import random
import warnings
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

def pivot_barplot(my_df: pd.DataFrame, pattern: str="family"):
    """
    Aggregates and calculates percentage of each family
    in a provided DataFrame.
    """

    if pattern != "family":
        new_df = my_df[my_df['ERV Family'].str.contains(pattern)]
        total_sub_values = new_df["count"].sum()
        new_df['raw_counts'] = new_df['count']
        #new_df.loc[:,'Name'] = pattern
        new_df['count'] = new_df['count'].apply(lambda x: x / total_sub_values)

        df_to_pivot = dict(zip(new_df["ERV"], new_df["count"]))

        sorted_items_desc = sorted(df_to_pivot.items(), key=lambda item: item[1], reverse=True)
        sorted_dict_desc = dict(sorted_items_desc)

        print("Sorted by value (descending):", sorted_dict_desc)
        print("with total values of " + str(total_sub_values))

        sorted_dict_desc["Name"] = pattern

        final_df = pd.DataFrame([sorted_dict_desc])

    else:
        new_fam_dict = {"Name":"Families"}
        all_families = my_df["ERV Family"].unique()

        for fam in all_families:
            get_count = my_df[my_df["ERV Family"] == fam].shape[0]
            fam_total = len(my_df["ERV Family"])
            print("there are " + str(get_count) + " for family " + fam)
            new_fam_dict[fam] = get_count / fam_total

        final_df = pd.DataFrame([new_fam_dict])

    final_df_pivot = final_df.pivot_table(index="Name",values=final_df.keys(),aggfunc=sum)

    return final_df_pivot

def gradient_hex(start_hex: str, end_hex: str, steps: int) -> list[str]:
    """
    Generate a list of hex color codes forming a gradient between two colors.

    Args:
        start_hex (str): The starting hex color code (e.g., "#FF0000").
        end_hex (str): The ending hex color code (e.g., "#0000FF").
        steps (int): The number of gradient steps (including start and end).

    Returns:
        list[str]: List of hex color codes forming the gradient.
    """
    # Remove '#' if present
    start_hex = start_hex.lstrip('#')
    end_hex = end_hex.lstrip('#')

    # Convert hex to RGB integers
    start_rgb = tuple(int(start_hex[i:i+2], 16) for i in (0, 2, 4))
    end_rgb = tuple(int(end_hex[i:i+2], 16) for i in (0, 2, 4))

    # Generate interpolated colors
    gradient = []
    for step in range(steps):
        ratio = step / (steps - 1) if steps > 1 else 0
        r = round(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
        g = round(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
        b = round(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
        gradient.append(f'#{r:02X}{g:02X}{b:02X}')

    random.shuffle(gradient)

    return gradient

def distinct_colors(n: int, lightness: float = 0.5, saturation: float = 0.7) -> list[str]:
    """
    Generate n visually distinct colors by evenly spacing hues in HSL color space.
    """
    colors = []
    for i in range(n):
        h = i / n  # evenly spaced hue
        l = lightness
        s = saturation
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        colors.append(f'#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}')
    return colors

###############################################################
# CHANGE THIS CODE

ERV_LIST = "PRJNA1238225_allspecies_ERV_1.txt"
OUTFILE = "L1_stacked_barplot.svg"
SAVE_FIGURE = False
MY_PATTERN = "ERV"
###############################################################

if __name__ == "__main__":

    df = pd.read_table(ERV_LIST,names=["ERV","count","ERV Family"])

    print(df.head())

    df_pivot = pivot_barplot(df,pattern=MY_PATTERN)

    # big_gradient = distinct_colors(df_pivot.shape[1])
    # random.shuffle(big_gradient)
    #big_gradient = sns.color_palette("husl", df_pivot.shape[1]).as_hex()
    if MY_PATTERN != "family":
        step_num = int(df_pivot.shape[1]/4)
        big_gradient_1 = gradient_hex("#365E19","#C7462C",step_num)
        big_gradient_2 = gradient_hex("#2E5283","#EEA125",step_num)
        big_gradient_3 = gradient_hex("#7BC6CB","#7A385A",step_num)
        big_gradient_4 = gradient_hex("#FF8400","#54386E",step_num)
        big_gradient = big_gradient_1 + big_gradient_4 + big_gradient_3 + big_gradient_2
        random.shuffle(big_gradient)
    else:
        big_gradient = ["#7E1D09","#2E5283","#F6A730","#365E19","#9F9046"]

    my_plot = df_pivot.plot(kind="bar",stacked=True,color=big_gradient)
    my_plot.set_axisbelow(True)
    my_plot.spines['top'].set_visible(False)
    my_plot.spines['right'].set_visible(False)
    my_plot.spines['left'].set_visible(False)
    my_plot.grid(axis="y",linestyle='--',alpha=0.7)
    my_plot.grid(axis="x",visible=False)
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left",ncol=6)
    plt.ylabel('Percentage of L1')
    plt.xticks(rotation=0)
    if SAVE_FIGURE:
        plt.savefig(OUTFILE, bbox_inches='tight')
    plt.show()
