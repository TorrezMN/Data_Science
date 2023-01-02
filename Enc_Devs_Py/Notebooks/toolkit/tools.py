import itertools
import pandas as pd
from collections import Counter

# CLASES
df_class = pd.core.frame.DataFrame


def get_column_uniques(df: df_class, col: str):
    return list(set(itertools.chain.from_iterable([i.split(";") for i in df[col]])))
