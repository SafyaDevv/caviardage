import pandas
import numpy
import matplotlib.pyplot as plot
import numpy

file = "files/data_16k.json"
blackout_df = pandas.read_json(file)


# ************** DATA CLEANING **************
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