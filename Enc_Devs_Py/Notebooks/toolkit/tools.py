import itertools
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np


def random_hex():
    """Generates a random dark Material color in hex format.

    Returns:
    A string representing the random dark Material color in hex format, e.g. '#121212'.
    """

    # List of dark Material colors
    dark_material_colors = [
        "#121212",
        "#1E88E5",
        "#00897B",
        "#39BBB0",
        "#26C6DA",
        "#42A5F5",
        "#64B5F6",
        "#9C27B0",
        "#E91E63",
        "#F44336",
        "#D81B60",
        "#880E4F",
    ]

    # Choose a random color from the list
    random_color = random.choice(dark_material_colors)

    return random_color


def replace_column_content(df, col, repl):
    """Replaces the contents of a column in a Pandas DataFrame with a given string,
    using regular expressions.

    Args:
    df: A Pandas DataFrame.
    col: The column in the DataFrame to replace the contents of.
    repl: A string to be replaced in the column.

    Returns:
    None.
    """
    df[col].replace(
        repl,
        regex=True,
        inplace=True,
    )


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


def get_percentage(value):
    """Returns the corresponding percentage in integer value for the given value.

    Args:
      value: A float value between 0 and 1.

    Returns:
      An integer value representing the percentage.
    """

    # Multiply the value by 100 to get the percentage.
    percentage = value * 100

    # Round the percentage to the nearest integer value.
    percentage = round(percentage)

    return f"{percentage}%"


def percentage_to_normal(val):
    return val.mul(100).round(1).astype(str) + " %"


def explode_pie(pie_size):
    """Returns a list of values to explode pie chart."""
    exp = [random.uniform(0.01, 0.05) for i in range(0, pie_size)]
    return exp


def get_column_uniques(df, col):
    """Print each of the UNIQUE values in a column where it is needed. Like so:
    ROW -> item 1; item 2; item 2, item 3;
    will print this:
    ite 1, item 2, item 3
    """

    return list(
        set(itertools.chain.from_iterable([i.split(";") for i in df[col].dropna()]))
    )


def print_column_uniques(df, col):
    """Print each of the UNIQUE values in a column where it is needed. Like so:
    ROW -> item 1; item 2; item 2, item 3;
    will print this:
    ite 1, item 2, item 3
    """

    print(set(itertools.chain.from_iterable([i.split(";") for i in df[col]])))


def make_dataframe(df, col, cat_col, count_col):
    """
    Creates a Pandas DataFrame from a column with multiple categories.

    Args:
    df: The Pandas DataFrame.
    col: The column with multiple categories.
    cat_col: The column name of the new DataFrame that will contain the unique categories.
    count_col: The column name of the new DataFrame that will contain the number of times each category appears.

    Returns:
    A Pandas DataFrame with the unique categories and their counts.
    """

    # Drop all rows with float values from the DataFrame.
    df = df.dropna(subset=[col])

    # Get all unique categories in the column.
    categories = set(
        itertools.chain.from_iterable([i.split(";") for i in df[col].values])
    )

    # Create a dictionary to store the category counts.
    category_counts = {}
    for category in categories:
        category_counts[category] = df[df[col].str.contains(category)].shape[0]

    # Create a new DataFrame from the category counts dictionary.
    new_df = pd.DataFrame(data=category_counts.items(), columns=[cat_col, count_col])

    return new_df


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
        df[col] = df[col].fillna(False)
        cats[i] = df[df[col].str.contains(i)].shape[0]

    df = pd.DataFrame(
        data=[i for i in cats.items()],
        columns=[x_label.replace(" ", ""), y_label.replace(" ", "")],
    )  # .set_index(x_label.replace(' ',''))

    return df


def get_normal_uniques_col_count(df, col):
    c = set(
        itertools.chain.from_iterable(
            [i.split(";") for i in df[col].value_counts(normalize=True).keys()]
        )
    )
    cats = {i: 0 for i in c}
    for i in c:
        cats[i] = df[df[col].str.contains(i)].shape[0]

    return cats


def get_uniques_col_count(df, col):
    c = set(
        itertools.chain.from_iterable(
            [i.split(";") for i in df[col].value_counts().keys()]
        )
    )
    cats = {i: 0 for i in c}
    for i in c:
        cats[i] = df[df[col].str.contains(i)].shape[0]

    return cats


def make_vertical_grouped_chart(df, g1, g2, col, labels, config):
    """
    group_config={
    'title':'1_linea_de_codigo by Gender \n',
    'c1_label':'Hombres',
    'c2_label':'Mujeres',
    'xlabel':'\n 1_linea_de_codigo level.',
    'ylabel':'Total count.\n',
    }

    """

    g1_count = get_uniques_col_count(g1, col)
    g2_count = get_uniques_col_count(g2, col)
    labels = get_column_uniques(df, col)

    # Values
    g1_val = [g1_count.get(i, 0) for i in labels]
    g2_val = [g2_count.get(i, 0) for i in labels]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, g1_val, width, label=config.get("c1_label", ""))
    rects2 = ax.bar(x + width / 2, g2_val, width, label=config.get("c2_label", ""))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(config.get("ylabel", ""))
    ax.set_title(config.get("title", ""))
    ax.set_xlabel(config.get("xlabel", ""))
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()

            ax.annotate(
                "{}".format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()


def make_horizontal_grouped_chart(df, g1, g2, col, labels, config):
    """
    group_config={
    'title':'1_linea_de_codigo by Gender \n',
    'c1_label':'Hombres',
    'c2_label':'Mujeres',
    'xlabel':'\n 1_linea_de_codigo level.',
    'ylabel':'Total count.\n',
    }

    """

    g1_count = get_uniques_col_count(g1, col)
    g2_count = get_uniques_col_count(g2, col)
    labels = get_column_uniques(df, col)

    # Values
    g1_val = [g1_count.get(i, 0) for i in labels]
    g2_val = [g2_count.get(i, 0) for i in labels]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.barh(x - width / 2, g1_val, width, label=config.get("c1_label", ""))
    rects2 = ax.barh(x + width / 2, g2_val, width, label=config.get("c2_label", ""))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(config.get("xlabel", ""))
    ax.set_title(config.get("title", ""))
    ax.set_xlabel(config.get("ylabel", ""))
    ax.set_yticks(x)
    ax.set_yticklabels(labels)
    ax.legend()

    for k, v in enumerate(rects1):
        height = v.get_height()

        if len(labels) >= 10:
            # Set the position of the annotation text
            x_pos = v.get_x() + v.get_width() + 1.5
        else:
            # Set the position of the annotation text
            x_pos = v.get_x() + v.get_width() + 1

        # x_pos = v.get_x() + v.get_width() / 2
        y_pos = v.get_y() - height * 0.5
        # y_pos = v.get_y() + height

        # Add the annotation text
        if int(g1_val[k]) != 0:
            # x_pos = v.get_x() + v.get_width()
            # ax.annotate(str(g1_val[k]), (x_pos, y_pos), ha='center', va='bottom')
            ax.annotate("  " + str(g1_val[k]), (x_pos, y_pos), ha="center", va="bottom")

    for k, v in enumerate(rects2):
        height = v.get_height()

        # Set the position of the annotation text
        # x_pos = v.get_x() + v.get_width()+1

        if len(labels) >= 10:
            # Set the position of the annotation text
            x_pos = v.get_x() + v.get_width() + 1
        else:
            # Set the position of the annotation text
            x_pos = v.get_x() + v.get_width() + 0.5

        # x_pos = v.get_x() + v.get_width() + 5
        # x_pos = v.get_x() + v.get_width() / 2
        y_pos = v.get_y() - height * 0.05 - 0.05
        # y_pos = v.get_y() + height

        # Add the annotation text
        if int(g2_val[k]) != 0:
            # ax.annotate(str(g2_val[k]), (x_pos, y_pos), ha='center', va='bottom')
            ax.annotate("  " + str(g2_val[k]), (x_pos, y_pos), ha="center", va="bottom")

    fig.tight_layout()
    plt.show()


def make_normalized_df(df, col):
    """Splits each row content by ";" and counts how many times each 'unique' value splitted by ';' appears in the column and returns a df with the keys and the percentage of times that appear in the column, forcing the numbers to be 'float' values.

    Args:
    df: The dataframe to work.
    col: The column to work.

    Returns:
    A Pandas DataFrame with the following columns:
    * categories: The unique values splitted by ";" in the column.
    * total count: The percentage of times that each category appears in the column.
    """
    # Split each row content by ";"
    df_split = df[col].str.split(";").explode()

    # Count how many times each unique value appears in the column
    df_counts = df_split.value_counts().reset_index(name="total count")

    # Calculate the percentage of times each category appears in the column
    df_counts["total count"] = (
        df_counts["total count"] / df_counts["total count"].sum() * 100
    )

    # Rename the columns
    df_counts.columns = ["categories", "total count"]

    # Set the index to the 'categories' column
    df_counts = df_counts.set_index("categories")

    return df_counts


def make_horizontal_bar(df, col, titulo, x_label, y_label, legend):
    """Makes a horizontal bar chart from a Pandas DataFrame.

    Args:
        df: A Pandas DataFrame.
        col: The column string name to plot.
        titulo: The string title of the chart.
        x_label: The 'x label' string name to be shown in the chart.
        y_label: The 'y label' string name to be shown in the chart.
        legend: Boolean value to set 'legends' to the chart.

    Returns:
        None.
    """

    # Making a plot for this column.
    fig = plt.figure(figsize=(9, 5))

    aux_df = make_df(df, col, "categorias", "conteo")

    aux_df_plot = aux_df.plot(kind="barh", title=f"{titulo} \n", legend=legend)

    aux_df_column_uniques = get_column_uniques(df, col)

    aux_df_plot.set_yticks(
        [k for k, v in enumerate(aux_df_column_uniques)], minor=False
    )

    aux_df_plot.set_yticklabels(
        [i for i in aux_df_column_uniques],
        fontdict=None,
        minor=False,
    )

    aux_df_plot.set_xlabel(f"{x_label}")
    aux_df_plot.set_ylabel(f"{y_label}")

    cat_values = [i for i in aux_df.conteo.value_counts().keys()]

    # Plot annotations.
    for k, v in enumerate(cat_values):
        aux_df_plot.annotate(v, (v, k), va="center")

        # nv_ed_plot.annotate(v, (v,k),va='center')

    plt.show()


def make_custom_horizontal_bar(df, col, titulo, x_label, y_label, legend):
    """Makes a horizontal bar chart from a Pandas DataFrame.

    Args:
        df: A Pandas DataFrame.
        col: The column string name to plot.
        titulo: The string title of the chart.
        x_label: The 'x label' string name to be shown in the chart.
        y_label: The 'y label' string name to be shown in the chart.
        legend: Boolean value to set 'legends' to the chart.

    Returns:
        None.
    """

    # Making a plot for this column.
    fig = plt.figure(figsize=(9, 5))

    # aux_df = make_df(df, col, "categorias", "conteo")

    aux_df_plot = df.plot(kind="barh", title=f"{titulo} \n", legend=legend)

    aux_df_column_uniques = get_column_uniques(df, "Category")

    aux_df_plot.set_yticks(
        [k for k, v in enumerate(aux_df_column_uniques)], minor=False
    )

    aux_df_plot.set_yticklabels(
        [i for i in aux_df_column_uniques],
        fontdict=None,
        minor=False,
    )

    aux_df_plot.set_xlabel(f"{x_label}")
    aux_df_plot.set_ylabel(f"{y_label}")

    cat_values = [i for i in df["count"].value_counts().keys()]

    # Plot annotations.
    for k, v in enumerate(cat_values):
        aux_df_plot.annotate(v, (v, k), va="center")

        # nv_ed_plot.annotate(v, (v,k),va='center')

    plt.show()
