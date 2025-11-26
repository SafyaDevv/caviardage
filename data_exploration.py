import pandas
import numpy
import json

file = "files/data_16k.json"

dataFrame = pandas.read_json(file)

print("Infos before cleaning non alphanumerical:")
dataFrame.info()

#print(dataFrame.head())

# dataFrame.to_csv("test.csv", index=False)

# ************** DATA CLEANING **************

dataFrame["poem"] = dataFrame["poem"].str.strip() #removing leading/trailing spaces

#remove rows with strings in poem column that contain non-letters (aside from spaces)
dataFrame = dataFrame[~dataFrame["poem"].str.contains(r"[^a-zA-Z\s]", na=False)]

#ensure no poems have randoms single letters (aside from a, i, o since those are words)
dataFrame = dataFrame[~dataFrame["poem"].str.contains(r"\b(?![aio]\b)[a-z]\b", 
                                                      na=False, case=False)]
dataFrame.info()

