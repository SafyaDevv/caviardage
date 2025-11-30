import streamlit as st
from data_pipeline import blackout_df, clean_df, clean_df_v2, plot_cleaning_pie_chart

import matplotlib.pyplot as plot
import numpy

st.title("Caviardage 📜🐙")

### SETTING UP SIDEBAR
page = st.sidebar.selectbox(
    "Select a page:",
    ["Overview", "Data Exploration", "See all versions of dataset"],
    )
st.sidebar.write("More stuff here?!")

### OVERVIEW PAGE
  
st.set_page_config(layout="wide") #make page full width

if page == "Overview":
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
    
    
    "✦•····················•✦•····················•✦"*4

    "🔎 Find poems with specific \"part of speech\""

    #choose how to filter poems
    part_of_speech_tags = "ADJ ADP ADV AUX CCONJ DET INTJ NOUN NUM PART PRON PROPN PUNCT SCONJ VERB".split()
    part_of_speech_labels = "Adjective Adposition Adverb Auxiliary Coordinating_conjunction Determiner Interjection Noun Numeral Particle Pronoun Proper_noun Punctuation Subordinating_conjunction Verb".split()

    user_selection = st.multiselect(
            "Select a type of \"part of speech\":",
            part_of_speech_tags,
            default = None
        )
    
    #filter poems, only show poems with selected pos tags
    filter = clean_df_v2["part-of-speech"].apply(
    lambda pos_list: all(pos in pos_list for pos in user_selection))
    filtered_poems = clean_df_v2[filter]

    #this function return the long version(s) of the part of speech tag(s) based on user selection
    def match_label_to_tag(selection):
        list_of_labels = []
        for tag in part_of_speech_tags:
            if tag in selection:
                list_of_labels.append(part_of_speech_labels[part_of_speech_tags.index(tag)])
        return list_of_labels

    selection_label = match_label_to_tag(user_selection)
        
    #display poems
    st.write(f"Poems containing *(in any order)*: **{selection_label}**")
    "There are ", len(filtered_poems), " poems to display."
    st.write(filtered_poems[["poem", "part-of-speech"]])

    "✦•····················•✦•····················•✦"*4

    "🔎 Find poems with specific sentiment expressed"

    col1, col2 = st.columns(2)

    sentiment_tags = ["Negative emotion", "Positive emotion", "Neutral emotion"]
    subjectivity_tags = ["Objective", "Subjective", "Neutral Objectivity"]

    ###choose how to filter poems
    #left column, sentiment polarity selection
    with col1:
        polarity_selection = st.segmented_control(
                "Type of emotion",
                sentiment_tags,
                default="Negative emotion")

    #left column, sentiment subjectivity selection
    with col2:
        subjectivity_selection = st.segmented_control(
                "Subjectivity of text",
                subjectivity_tags,
                default="Neutral Objectivity")


    filtered_poems_s = clean_df_v2 #display unfiltered dataframe

    #filtering by polarity
    if polarity_selection == "Negative emotion":
        polarity_filter = clean_df_v2["sentiment_polarity"] < 0
    elif polarity_selection == "Positive emotion":
        polarity_filter = clean_df_v2["sentiment_polarity"] > 0
    elif polarity_selection == "Neutral emotion":
        polarity_filter = clean_df_v2["sentiment_polarity"] == 0 
    if not polarity_selection:
        polarity_filter = False

        
    #filter poems, only show poems with selected polarity
    if subjectivity_selection == "Objective":
        subjectivity_filter = clean_df_v2["sentiment_subjectivity"] < 0
    elif subjectivity_selection == "Subjective":
        subjectivity_filter = clean_df_v2["sentiment_subjectivity"] > 0
    elif subjectivity_selection == "Neutral Objectivity":
        subjectivity_filter = clean_df_v2["sentiment_subjectivity"] == 0
    if not subjectivity_selection:
        subjectivity_filter = False

    #combining & applying filter

### !!!!!!!!!!!!!!!! BUG IS HERE !!!!!!!!!!!!!!!!! ### 
    if polarity_filter is False:
        combined_filter = subjectivity_filter
    else:
        combined_filter = polarity_filter & subjectivity_filter

    filtered_poems_s = clean_df_v2[combined_filter]

### !!!!!!!!!!!!!!!! BUG IS HERE !!!!!!!!!!!!!!!!! ### 

    #display poems
    st.write(f"Poems with: **{polarity_selection}** and **{subjectivity_selection}**")
    "There are ", len(filtered_poems_s), " poems to display."
    st.write(filtered_poems_s[["poem", "sentiment_polarity", "sentiment_subjectivity"]])
    

### VERSION HISTORY PAGE
if page == "See all versions of dataset":

    expand = st.expander("Cleaned Dataset with POS Tags & Sentiment scores", icon=":material/info:")
    expand.dataframe(clean_df_v2, use_container_width=True)    
 
    expand = st.expander("The cleaned dataset", icon=":material/info:")
    expand.dataframe(clean_df, use_container_width=True)

    expand = st.expander("The original Blackout dataset", icon=":material/info:")
    expand.dataframe(blackout_df, use_container_width=True)




