import pandas
import numpy
import json
import matplotlib.pyplot as plot
import numpy

file = "files/data_16k.json"

dataFrame = pandas.read_json(file)

print("Infos before cleaning up:")
dataFrame.info()

# dataFrame.to_csv("test.csv", index=False)

# ************** DATA CLEANING **************

alphaPoems = dataFrame["poem"].str.contains(r"[^a-zA-Z\s]", na=False) 
cleanDf = dataFrame[~alphaPoems] #remove rows with strings in poem column that contain non-letters (aside from spaces)

print("count of alpha poems: ", len(alphaPoems))

cleanDf = cleanDf[~cleanDf["poem"].str.contains(r"\b(?![aio]\b)[a-z]\b", 
                                                      na=False, case=False)] #ensure no poems have randoms single letters (aside from a, i, o since those are words)
#count of poems with random single letters
#INSERT

cleanDf.drop_duplicates(subset=["poem"], inplace=True, keep="first") #when there is duplicated poems, only keep one of them
#count of poems that were duplicates
#INSERT

#Pie chart showing categories of poems removed
#INSERT


cleanDf.info()

cleanDf["poem"] = cleanDf["poem"].str.strip() #removing leading/trailing spaces


