# IS445_Tung_Justin_Functions.py

"""
A python file that stores the final functions for Justin Tung's IS445 Fall 2023 Final Project
Specifically, the 'General_Public' Notebook.

"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import plotly.graph_objects as go
from webcolors import hex_to_rgb


def zero_out(df: pd.DataFrame, change: str, where: str, to) -> pd.DataFrame:
    """
    A utility functions that is basically one big "where" function from SQL
    This function does not have reason to exist except in a desperate attempt to remain DRY
    :param df: the dataframe
    :param change: the field you want to change
    :param where: where you want the field to change
    :param to: what you want to change the field to
    :return df: the return dataframe
    """
    df.loc[df['edible'] == where, change] = to
    return df


def make_mushroom_bar(stems: list, caps: list, r: list, names: list):
    """
    Makes mushroom-looking bar plots from a set of caps and stems
    caps are positive values and stems are negative, but the yscale is in absolute value
    :param caps: a list of cap values
    :param stems: a list of stem values
    :param r: a list of spacings for each set of bars
    :param names: a list of names to go along the yticks
    """
    fig, ax = plt.subplots()
    ax.set_facecolor('#b4b387')
    plt.ylim(-10000, 10000)
    plt.bar(r, stems, color='#ffd39b', edgecolor='#000000', width=4, hatch='|||')
    plt.bar(r, caps, bottom=0, color='#bb2124', edgecolor='#ffffff', width=9.3, hatch='.')
    plt.xticks(r, names, size=8)
    plt.xlabel("Odor")
    plt.title("Odor and Eatability")
    plt.legend(['Edible', 'Poisonous'], bbox_to_anchor=(1, 1))
    plt.yscale('symlog')
    ax.set_yticklabels(abs(ax.get_yticks()))

    plt.show()


def find_mode(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """
    This function takes a dataframe and a category as a string,
    then returns the dataframe sorted by the values in that category
    :param df: the input dataframe
    :param category: a string of the category to find the mode in
    :return df_category: a df with the modal category
    """
    df_category = df.groupby(category)[category].count()
    df_category = df_category.sort_values(ascending=False)
    df_category = pd.DataFrame(df_category)
    df_category['Percent'] = df_category / 84.16
    return df_category


def make_donut_chart(df_color: pd.DataFrame, color_column: str):
    """
    takes a dataframe and a column as a string,
    creates and displays a graph object,
    uses a dict to match colors in the dataframe,
    :param df_color: a dataframe of the isolated column
    :param color_column: the name of the column as a string
    """
    rcParams['font.size'] = 14.0
    colors = {'brown': '#845321',
              'gray': '#808080',
              'black': '#111110',
              'red': '#df5c52',
              'yellow': '#f4eeb1',
              'chocolate': '#7B3F00',
              'orange': '#FFA500',
              'white': '#f6f6f6',
              'buff': '#edd8b9',
              'pink': '#ffc0cb',
              'cinnamon': '#D2691E',
              'green': '#6b8e23',
              'purple': '#b59bb8'}
    labels = list(df_color.index.values)
    df_color.plot(kind='pie',
                  y=color_column,
                  pctdistance=1.1,
                  figsize=(6, 6),
                  labels=None,
                  colors=[colors[key] for key in labels],
                  wedgeprops={"edgecolor": "black",
                              'linewidth': 0.1,
                              'antialiased': True})
    title = color_column.replace('-', ' ').title()
    plt.title(f'{title}\n\n', x=0.5, y=0.9)
    plt.ylabel('')
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(0.95, 0.7),
               labels=round(df_color['Percent'], 1),
               edgecolor='white')
    my_circle = plt.Circle((0, 0), 0.3, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)


def numeralize_categories(categories: list, df: pd.DataFrame) -> pd.DataFrame:
    """
    A utility function to help with Sankey Diagram.
    Numbers unique nodes for the Sankey Diagram,
    sequentially from the dataframe.
    Repopulates the numbers into the input dataframe
    :param categories: this is a list of the columns to serialize and convert
    :param df: the dataframe to be numeralized
    :return df: the numeralized dataframe
    """
    total_cats = 0  # accumulator for sequencing rows across columns
    for category in categories:
        cat_uniques = list(pd.unique(df[category]))
        cat_nums = []
        for i in range(0, len(cat_uniques)):
            cat_nums.append(i + total_cats)
        df[category] = df[category].replace(cat_uniques, cat_nums)
        total_cats += len(cat_uniques)
    return df


def convert_color(color_link: list) -> list:
    """
    Converts hex to rgb, then rgb to rgba to achieve tranparency.
    :param color_link: an input list of hex colors
    :return rgb_link_color: an output list of RGBA colors with standard alpha
    """
    rgb_link_color = ['rgba({},{},{}, 0.6)'.format(
        hex_to_rgb(x)[0],
        hex_to_rgb(x)[1],
        hex_to_rgb(x)[2]) for x in color_link]
    return rgb_link_color


def create_sankey(nodes: dict, links: dict):
    """
    Creates Sankey graphs with hover interactivity.
    Takes a nodes and links, and uses pre-established colors to create cohesive sankey diagrams.
    Converts hex to rgb, then rgb to rgba to achieve tranparency.
    :param nodes: a dict of nodes, as specified by go.Sankey syntax
    :param links: a dict of links, as specified by go.Sankey syntax
    """
    fig = go.Figure(data=[go.Sankey(node=nodes,
                                    link=links,
                                    orientation="v",
                                    )])
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = ['TeX Gyre Bonum'] + rcParams['font.serif']
    fig.update_layout(title_text="Mushroom Habitats and Growth Patterns", font_size=16,
                      font_family="serif",
                      title_font_family='TeX Gyre Bonum',
                      font_color="black",
                      width=950, height=900, margin_b=150)
    fig.show()
