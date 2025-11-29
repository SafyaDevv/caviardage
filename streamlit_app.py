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

    col1, col2 = st.columns(2, border=True)
    st.write(
        "Explore the dataset ✨",
        )
    
    "🔎 Find poems with specific \"part of speech\""
    #left column
    with col1:
        part_of_speech_tags = "ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ VERB".split()

        selected_pos = st.selectbox(
            "Select a type of \"part of speech\":",
            part_of_speech_tags
        )
    #right column
    with col2:
        filter = clean_df_v2["part-of-speech"].apply(
        lambda pos: selected_pos in pos)
        
        filtered_poems = clean_df_v2[filter]
        
        st.write(f"Poems containing POS tag: **{selected_pos}**")
        st.write(filtered_poems[["poem", "part-of-speech"]])








    toggle_df = st.toggle("See cleaned dataset with POS tags")
    if toggle_df:
        st.subheader("Cleaned Dataset with POS Tags")
        st.dataframe(clean_df_v2, use_container_width=True)


