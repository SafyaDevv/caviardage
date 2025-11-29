### This script is the main script for this project
### it handles most steps of the data pipeline
### including data loading, cleaning, POS tagging, and visualisation
### used in streamlit_app.py for displaying data and visualisations

import pandas
import numpy
import matplotlib.pyplot as plot
import numpy

file = "files/data_16k.json"
blackout_df = pandas.read_json(file)

# Step 1: DATA CLEANING 
# Poems with non-alphabetical symbols, single random letters, and duplicates are removed
# + track of counts for visualisation

count_of_poems = len(blackout_df["poem"])

#removing poems with non-alphabetical symbols
clean_df = blackout_df[~blackout_df["poem"].str.contains(r"[^a-zA-Z\s]", na=False)] 
count_non_alpha_p = count_of_poems - len(clean_df)

#removing poems with single random letters that are not words (a, i, o are valid)
clean_df = clean_df[~clean_df["poem"].str.contains(r"\b(?![aio]\b)[a-z]\b", 
                                                      na=False, case=False)] 
count_random_letter = count_of_poems - len(clean_df)

#removing duplicate poems, keeping first occurrence
clean_df.drop_duplicates(subset=["poem"], inplace=True, keep="first") 
count_of_duplicate = count_of_poems - len(clean_df)

clean_df["poem"] = clean_df["poem"].str.strip()


### Step 2: PART-OF-SPEECH TAGGING
### imported updated dataset with POS tagging applied to each poem
clean_df_v2 = pandas.read_csv("files/better_blackout.csv")

#get count of poems removed due to unrecognised words
count_unknown_words = len(clean_df) - len(clean_df_v2)

### Step 3: ANALYSIS OF CLEANED DATASET

#find all unique POS tag sequences in cleaned dataset
unique_pos = clean_df_v2["part-of-speech"].unique()
#print(f"Number of unique part of speech sequences in dataset: {len(unique_pos)}")
#print("List of unique POS tag sequences:\n ")
#print(*unique_pos, sep='\n')


### Step 4: VISUALISATION
### used in streamlit_app.py and report

'''Function returning a pie chart showing an overview of the data cleaning process
used in streamlit_app.py'''
def plot_cleaning_pie_chart():

    labels = ['Poems with non-alphabetical symbols', 'Poems with single random letters', 'Duplicate poems', 'Poems with unrecognisable words', 'Poems kept in cleaned dataset']
    numbers = (count_non_alpha_p, count_random_letter, count_of_duplicate, count_unknown_words, len(clean_df))
    colours = ["#959595", "#E0BEFF", "#92A2FF","#000000", "#572ba9"]
    explodedSlices = [0.2, 0.2, 0.2, 0.2, 0.1] 

    # Creating plot
    fig = plot.figure(figsize=plot.figaspect(1))
    plot.title("Data Cleaning Overview", fontsize=14)
    plot.pie(numbers,
        labels=None,
        explode=explodedSlices,
        colors=colours,
        autopct="%1.1f%%",
        pctdistance=1.3,
        startangle=160,
        wedgeprops={"linewidth": 1, "edgecolor": "black"},
        textprops={"fontsize": 12}
    )

    plot.legend(labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(0.5, 0),
        frameon=True,
        fontsize=8,
        title_fontsize=10)

    plot.tight_layout(pad=1.5)
    #plot.show()
    return fig


