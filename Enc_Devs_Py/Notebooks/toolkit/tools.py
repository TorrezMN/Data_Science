import itertools
import pandas as pd


def print_column_uniques(df, col):
    """Print each of the UNIQUE values in a column where it is needed. Like so:
    ROW -> item 1; item 2; item 2, item 3;
    will print this:
    ite 1, item 2, item 3
    """

    print(set(itertools.chain.from_iterable([i.split(";") for i in df[col]])))


def make_df(df, col):
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
        data=[i for i in cats.items()], columns=["cat", "count"]
    ).set_index("cat")

    return df
