import itertools
import pandas as pd
import random


def get_color(g, t):
    # Light
    color_hombres_light = (12 / 255, 50 / 255, 196 / 255, 0.5)
    color_mujeres_light = (255 / 255, 192 / 255, 203 / 255, 0.5)
    color_neutro_light = (149 / 255, 165 / 255, 166 / 255, 0.5)
    # Dark
    color_hombres_dark = (12 / 255, 50 / 255, 196 / 255, 0.8)
    color_mujeres_dark = (255 / 255, 192 / 255, 203 / 255, 0.8)
    color_neutro_dark = (149 / 255, 165 / 255, 166 / 255, 0.8)
    # NONE COLOR
    color_none = (49 / 255, 15 / 255, 6 / 255, 0.8)

    cl = {
        "Male": color_hombres_light,
        "Female": color_mujeres_light,
        "I do not share.": color_neutro_light,
    }
    cd = {
        "Male": color_hombres_dark,
        "Female": color_mujeres_dark,
        "I do not share.": color_neutro_dark,
    }

    if t == "light":
        return cl.get(g, color_none)
    else:
        return cd.get(g, color_none)


def percentage_to_normal(df):
    return df.mul(100).round(1).astype(str) + " %"


def explode_pie(exp_range):
    """Returns a list of values to explode pie chart."""
    exp = [random.uniform(0.01, 0.05) for i in range(0, exp_range)]
    return exp


def get_column_uniques(df, col):
    """Print each of the UNIQUE values in a column where it is needed. Like so:
    ROW -> item 1; item 2; item 2, item 3;
    will print this:
    ite 1, item 2, item 3
    """

    return list(set(itertools.chain.from_iterable([i.split(";") for i in df[col]])))


def print_column_uniques(df, col):
    """Print each of the UNIQUE values in a column where it is needed. Like so:
    ROW -> item 1; item 2; item 2, item 3;
    will print this:
    ite 1, item 2, item 3
    """

    print(set(itertools.chain.from_iterable([i.split(";") for i in df[col]])))


def make_df(df, col, x_label, y_label):
    """
    Returns a dataframe from column values.
    Column format:

    ---> Ed. Secundaria;Ed. Universitaria;Master

    """
    c = set(
        itertools.chain.from_iterable(
            [i.split(";") for i in df[col].value_counts().keys()]
        )
    )
    cats = {i: 0 for i in c}
    for i in c:
        cats[i] = df[df[col].str.contains(i)].shape[0]
    df = pd.DataFrame(
        data=[i for i in cats.items()],
        columns=[x_label.replace(" ", ""), y_label.replace(" ", "")],
    )  # .set_index(x_label.replace(' ',''))

    return df
