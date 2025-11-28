import pandas
import numpy
import json
import matplotlib.pyplot as plot
import numpy

file = "files/data_16k.json"

dataFrame = pandas.read_json(file)

# dataFrame.to_csv("test.csv", index=False)

# ************** DATA CLEANING **************

countOfPoems = len(dataFrame["poem"]) #count before cleaning

cleanDf = dataFrame[~dataFrame["poem"].str.contains(r"[^a-zA-Z\s]", na=False)] #keep all poems but the one in nonAlphaPoems

countNonAlphaPoems = countOfPoems - len(cleanDf) #count of poems with non-alpha characters

cleanDf = cleanDf[~cleanDf["poem"].str.contains(r"\b(?![aio]\b)[a-z]\b", 
                                                      na=False, case=False)] #ensure no poems have randoms single letters (aside from a, i, o since those are words)

countRandomLetterPoems = countOfPoems - len(cleanDf) #count of poems with single random letters

cleanDf.drop_duplicates(subset=["poem"], inplace=True, keep="first") #when there is duplicated poems, only keep one of them

countOfDuplicatePoems = countOfPoems - len(cleanDf)

cleanDf["poem"] = cleanDf["poem"].str.strip() #removing leading/trailing spaces


#Function returning a pie chart showing an overview of the data cleaning process
#Used in streamlit_app.py
def plotDataCleaningChart():

    labels = ['Poems with non-alphabetical symbols', 'Poems with single random letters', 'Duplicate poems', 'Poems kept in cleaned dataset']
    numbers = (countNonAlphaPoems, countRandomLetterPoems, countOfDuplicatePoems, len(cleanDf))
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

# *** LOOKING AT GRAMMAR CHECKS ***
#goodGrammar = cleanDf[cleanDf["grammar-check"] == True]
#print(len(goodGrammar)) #NO POEMS IN CLEANED DATASET ARE MARKED AS HAVING GOOD GRAMMAR

#Storing Poems marked as having "good grammar" in the original dataset:
goodGrammarOrigDf = dataFrame[dataFrame["grammar-check"] == True] 
print(goodGrammarOrigDf["poem"])