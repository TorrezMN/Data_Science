import itertools
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np

 
       
def replace_column_content(df,col, repl):
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
    repl
    ,
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

    return list(set(itertools.chain.from_iterable([i.split(";") for i in df[col].dropna()])))


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

def get_uniques_col_count(df, col):
    c = set(
        itertools.chain.from_iterable(
            [i.split(";") for i in df[col].value_counts().keys()]
        )
    )
    cats = {i: 0 for i in c}
    for i in c:
        cats[i] = df[df[col].str.contains(i)].shape[0]

    return(cats)


def make_vertical_grouped_chart (df, g1,g2,col,labels, config):

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
    labels = get_column_uniques(df,col)

    # Values
    g1_val = [g1_count.get(i,0) for i in labels ]
    g2_val = [g2_count.get(i,0) for i in labels ]
   
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, g1_val, width, label=config.get('c1_label',''))
    rects2 = ax.bar(x + width/2, g2_val, width, label=config.get('c2_label',''))
    
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(config.get('ylabel',''))
    ax.set_title(config.get('title',''))
    ax.set_xlabel(config.get('xlabel',''))
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    
    autolabel(rects1)
    autolabel(rects2)
    
    fig.tight_layout()
    
    plt.show()
    
        
    
def make_horizontal_grouped_chart (df, g1,g2,col,labels, config):
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

    
    for k,v in enumerate(rects1):
        height = v.get_height()
        
        # Set the position of the annotation text
        x_pos = v.get_x() + v.get_width() 
        #x_pos = v.get_x() + v.get_width() / 2
        y_pos = v.get_y()  -0.05
        #y_pos = v.get_y() + height
        
        # Add the annotation text
        if (int(g1_val[k])!=0):
            #x_pos = v.get_x() + v.get_width() 
            #ax.annotate(str(g1_val[k]), (x_pos, y_pos), ha='center', va='bottom')
            ax.annotate(str(v.get_width() ), (x_pos+3, y_pos), ha='center', va='bottom')


    for k,v in enumerate(rects2):
        height = v.get_height()
        
        # Set the position of the annotation text
        x_pos = v.get_x() + v.get_width()
        #x_pos = v.get_x() + v.get_width() + 5
        #x_pos = v.get_x() + v.get_width() / 2
        y_pos = v.get_y()  
        #y_pos = v.get_y() + height
        
        # Add the annotation text
        if (int(g2_val[k])!=0):
            #ax.annotate(str(g2_val[k]), (x_pos, y_pos), ha='center', va='bottom')
            ax.annotate(str(v.get_width() ), (x_pos+3, y_pos), ha='center', va='bottom')
    



    
    
    fig.tight_layout()
    plt.show()
