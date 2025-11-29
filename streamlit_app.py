import streamlit as st
from data_pipeline import clean_df, blackout_df, clean_df_v2, plot_cleaning_pie_chart
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

    "✦•······················•✦•······················•✦"*3

    "🔎 Find poems with specific sentiment expressed"

    #WILL USE SEGMENTED CONTROL :o

    #choose how to filter poems
    sentiment_tags = ["Negative emotion", "Positive emotion", "Neutral emotion"]
 #"Objective", "Subjective", "Neutral Objectivity

    selection = st.segmented_control(
            "Select type of emotion",
            sentiment_tags,
            default="Negative emotion"
        )
    

    #filter poems, only show poems with selected polarity
    if selection == None:
        filtered_poems_s = clean_df_v2

    if selection == "Negative emotion":
        filtered_poems_s = clean_df_v2[clean_df_v2["sentiment_polarity"] < 0]

    if selection == "Positive emotion":
        filtered_poems_s = clean_df_v2[clean_df_v2["sentiment_polarity"] > 0]

    if selection == "Neutral emotion":
        filtered_poems_s = clean_df_v2[clean_df_v2["sentiment_polarity"] == 0]

    #display poems
    st.write(f"Poems with: **{selection}**")
    "There are ", len(filtered_poems_s), " poems to display."
    st.write(filtered_poems_s[["poem", "sentiment_polarity"]])
    

### VERSION HISTORY PAGE
if page == "See all versions of dataset":

    expand = st.expander("Cleaned Dataset with POS Tags & Sentiment scores", icon=":material/info:")
    expand.dataframe(clean_df_v2, use_container_width=True)    
 
    expand = st.expander("The cleaned dataset", icon=":material/info:")
    expand.dataframe(clean_df, use_container_width=True)

    expand = st.expander("The original Blackout dataset", icon=":material/info:")
    expand.dataframe(blackout_df, use_container_width=True)




