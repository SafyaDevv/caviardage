### This script is the main script for this project
### it handles most steps of the data pipeline
### including data loading, cleaning, POS tagging, and visualisation
### used in streamlit_app.py for displaying data and visualisations

import pandas
import numpy
import matplotlib.pyplot as plot
import numpy

#STEP 1: DATA INGESTION

file = "files/data_16k.json"
blackout_df = pandas.read_json(file)

# Step 2: DATA PREPREPROCESSING / CLEANING

# Poems with non-alphabetical symbols, single random letters, and duplicates are removed
# + track of counts for visualisation

count_of_poems = len(blackout_df["poem"])

#Cleaning poems that don't match criterias + keeping count of what was removed for visualisation purposes

clean_df = blackout_df[~blackout_df["poem"].str.contains(r"[^a-zA-Z\s]", na=False)]  #alphabetical chars only
count_non_alpha_p = count_of_poems - len(clean_df)

clean_df = clean_df[~clean_df["poem"].str.contains(r"\b(?![aio]\b)[a-z]\b", 
                                                      na=False, case=False)] #no poems with random single letters that aren't words
count_random_letter = count_of_poems - len(clean_df)

clean_df.drop_duplicates(subset=["poem"], inplace=True, keep="first") #if there is duplicates, only keep first occurrence
count_of_duplicate = count_of_poems - len(clean_df)

clean_df["poem"] = clean_df["poem"].str.strip() #remove trailing/leading spaces


### Step 3: DATA PROCESSING

#updated dataset n/ new features applied to each poem, done in generate_dataset.py
clean_df_v2 = pandas.read_csv("files/better_blackout.csv") 

count_unknown_words = len(clean_df) - len(clean_df_v2) #count of rows removed during NLP in pos_handler.pos

### Step 4: ANALYSIS

#find all unique POS tag sequences in cleaned dataset
unique_pos = clean_df_v2["part-of-speech"].unique()
#print(f"Number of unique part of speech sequences in dataset: {len(unique_pos)}")
#print("List of unique POS tag sequences:\n ")
#print(*unique_pos, sep='\n')


### Step 5: VISUALISATION
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


