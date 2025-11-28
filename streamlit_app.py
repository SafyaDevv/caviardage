import streamlit as st
from data_pipeline import clean_df, blackout_df, clean_df_v2, plot_cleaning_pie_chart
import matplotlib.pyplot as plot
import numpy

st.title("Caviardage 📜🐙")


### SETTING UP SIDEBAR
page = st.sidebar.selectbox(
    "Select a page:",
    ["Overview", "Data Exploration"]
)

### OVERVIEW PAGE
if page == "Overview":
#st.set_page_config(layout="wide") #make page full width
    st.write(
        "Woop woop here comes the data.",
    )

    fig = plot.figure(plot_cleaning_pie_chart())
    st.pyplot(fig)

    #clean_df and blackout_df are imported from data_cleaning.py
    expand = st.expander("The original Blackout dataset", icon=":material/info:")
    expand.dataframe(blackout_df, use_container_width=True)

    expand = st.expander("The cleaned dataset", icon=":material/info:")
    expand.dataframe(clean_df, use_container_width=True)

### DATA EXPLORATION PAGE
if page == "Data Exploration":
    st.write(
        "Explore the cleaned dataset with POS tags.",
    )






    toggle_df = st.toggle("See cleaned dataset with POS tags")
    if toggle_df:
        st.subheader("Cleaned Dataset with POS Tags")
        st.dataframe(clean_df_v2, use_container_width=True)


