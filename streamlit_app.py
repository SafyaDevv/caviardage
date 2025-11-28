import streamlit as st
from data_cleaning import clean_df, blackout_df, plot_data_cleaning_chart
import matplotlib.pyplot as plot
import numpy

st.title("Caviardage 📜🐙")

#st.set_page_config(layout="wide") #make page full width

st.write(
    "Woop woop here comes the data.",
)

fig = plot.figure(plot_data_cleaning_chart())
st.pyplot(fig)

#clean_df and blackout_df are imported from data_cleaning.py
expand = st.expander("The original Blackout dataset", icon=":material/info:")
expand.dataframe(blackout_df, use_container_width=True)

expand = st.expander("The cleaned dataset", icon=":material/info:")
expand.dataframe(clean_df, use_container_width=True)

#TRYING OUT TOGGLES
#displayDataFrame = st.toggle("Display full original dataset")

# if displayDataFrame:
#     st.subheader("The original Blackout dataset")
#     st.dataframe(data, use_container_width=True)

