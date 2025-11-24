import pandas
import json

file = "files\data_16k.json"

dataFrame = pandas.read_json(file)

print(dataFrame.head())

# dataFrame.to_csv("test.csv", index=False)

