import streamlit as st
import data_cleaning as data_exp
import matplotlib.pyplot as plot
import numpy

st.title("Caviardage 📜🐙")

data = data_exp.dataFrame
cleanData = data_exp.cleanDf

#st.set_page_config(layout="wide") #make page full width

st.write(
    "Woop woop here comes the data.",
)

fig = plot.figure(data_exp.plotDataCleaningChart())
st.pyplot(fig)

expand = st.expander("The original Blackout dataset", icon=":material/info:")
expand.dataframe(data, use_container_width=True)

expand = st.expander("The cleaned dataset", icon=":material/info:")
expand.dataframe(cleanData, use_container_width=True)




#TRYING OUT TOGGLES
#displayDataFrame = st.toggle("Display full original dataset")

# if displayDataFrame:
#     st.subheader("The original Blackout dataset")
#     st.dataframe(data, use_container_width=True)

