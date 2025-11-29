import streamlit as st
from data_pipeline import clean_df, blackout_df, clean_df_v2, plot_cleaning_pie_chart
import matplotlib.pyplot as plot
import numpy

st.title("Caviardage 📜🐙")


### SETTING UP SIDEBAR
page = st.sidebar.selectbox(
    "Select a page:",
    ["Overview", "Data Exploration", "See all versions of dataset"]
)

### OVERVIEW PAGE
if page == "Overview":
#st.set_page_config(layout="wide") #make page full width
    st.write(
        "Woop woop here comes the data.",
    )

    fig = plot.figure(plot_cleaning_pie_chart())
    st.pyplot(fig)

### DATA EXPLORATION PAGE
if page == "Data Exploration":

    st.write(
        "Explore the dataset ✨",
        )
    
    
    "✦•······················•✦•······················•✦"*3

    "🔎 Find poems with specific \"part of speech\""

    #choose how to filter poems
    part_of_speech_tags = "ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ VERB".split()

    selected_pos = st.selectbox(
            "Select a type of \"part of speech\":",
            part_of_speech_tags
        )
    
    #filter  poems
    filter = clean_df_v2["part-of-speech"].apply(
    lambda pos: selected_pos in pos)
    filtered_poems = clean_df_v2[filter]

    #display poems
    st.write(f"Poems containing POS tag: **{selected_pos}**")
    st.write(filtered_poems[["poem", "part-of-speech"]])

### VERSION HISTORY PAGE
if page == "See all versions of dataset":

    expand = st.expander("Cleaned Dataset with POS Tags", icon=":material/info:")
    expand.dataframe(clean_df_v2, use_container_width=True)    
 
    expand = st.expander("The cleaned dataset", icon=":material/info:")
    expand.dataframe(clean_df, use_container_width=True)

    expand = st.expander("The original Blackout dataset", icon=":material/info:")
    expand.dataframe(blackout_df, use_container_width=True)


    


