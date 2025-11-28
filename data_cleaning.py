import pandas
import numpy
import matplotlib.pyplot as plot
import numpy
from grammar import get_grammar_check

file = "files/data_16k.json"

dataframe = pandas.read_json(file)

# dataFrame.to_csv("test.csv", index=False)

# ************** DATA CLEANING **************

count_of_poems = len(dataframe["poem"]) #count before cleaning

clean_df = dataframe[~dataframe["poem"].str.contains(r"[^a-zA-Z\s]", na=False)] #keep all poems but the one in nonAlphaPoems

count_non_alpha_p = count_of_poems - len(clean_df) #count of poems with non-alpha characters

clean_df = clean_df[~clean_df["poem"].str.contains(r"\b(?![aio]\b)[a-z]\b", 
                                                      na=False, case=False)] #ensure no poems have randoms single letters (aside from a, i, o since those are words)

count_random_letter = count_of_poems - len(clean_df) #count of poems with single random letters

clean_df.drop_duplicates(subset=["poem"], inplace=True, keep="first") #when there is duplicated poems, only keep one of them

count_of_duplicate = count_of_poems - len(clean_df)

clean_df["poem"] = clean_df["poem"].str.strip() #removing leading/trailing spaces

print(get_grammar_check(dataframe)) #prints poems marked as having good grammar in cleaned dataset (should be none)

#Dropping grammar-check column from cleaned dataset as it's all false values
clean_df = clean_df.drop(columns=["grammar-check"])

#Function returning a pie chart showing an overview of the data cleaning process
#Used in streamlit_app.py
def plot_data_cleaning_chart():

    labels = ['Poems with non-alphabetical symbols', 'Poems with single random letters', 'Duplicate poems', 'Poems kept in cleaned dataset']
    numbers = (count_non_alpha_p, count_random_letter, count_of_duplicate, len(clean_df))
    colours = ["#959595", "#E0BEFF", "#92A2FF", "#572ba9"]
    explodedSlices = [0.2, 0.2, 0.2, 0.1] 

    # Creating plot
    fig = plot.figure(figsize=plot.figaspect(1))
    plot.title("Data Cleaning Overview", fontsize=14)
    plot.pie(numbers,
        labels=None,
        explode=explodedSlices,
        colors=colours,
        autopct="%1.0f%%",
        pctdistance=1.15,
        startangle=140,
        wedgeprops={"linewidth": 1, "edgecolor": "black"},
        textprops={"fontsize": 12}
    )

    plot.legend(labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(0.22, 0),
        frameon=True,
        fontsize=9,
        title_fontsize=10)

    plot.tight_layout(pad=1.5)
    #plot.show()
    return fig

# ******** GENERATING STATS ON CLEANED DATASET ********