import streamlit as st
import data_pipeline as dp
import matplotlib.pyplot as plot
import pandas
import plotly.io as pio

clean_df_v2 = dp.clean_df_v2

st.title("Caviardage 📜🐙")

### SETTING UP SIDEBAR
page = st.sidebar.selectbox(
    "Select a page:",
    ["Overview", "Visualisation", "Syntax & Sentiment Analysis", 
     "Themes exploration",
     "Poem recommender",
     "See all versions of dataset",
     ]
    )
st.sidebar.write("More stuff here?!")

### OVERVIEW PAGE
  
st.set_page_config(layout="wide") #make page full width

if page == "Overview":
    st.write(
        "Woop woop here comes the data.",
    )

    #Descriptive analysis of dataset

    col1, col2 = st.columns(2)

    with col1:
        st.write(clean_df_v2.describe())  # ? add description for each column

    with col2:
        st.write(clean_df_v2.columns.values)


### VISUALISATION HERE
if page == "Visualisation":

    st.subheader("Correlation heatmap of numeric features in dataset, before encoding categorical features")
    col1, col2 = st.columns(2)

    with col1:
        fig = dp.get_correlation_heatmap()
        st.pyplot(fig, use_container_width=False)

    st.subheader("Scatter plots of sentiment analysis in dataset")
    
    col1, col2 = st.columns(2)

    with col1:
        #polarity vs subjectivity scatter plots
        scatter_plot_1 = dp.get_scatterplot("passage-subjectivity", "passage-polarity", "Passage: Polarity compared to subjectivity", "pink")
        st.pyplot(scatter_plot_1)

    with col2:
        scatter_plot_2 = dp.get_scatterplot("poem-subjectivity", "poem-polarity", "Poem: Polarity compared to subjectivity", "purple")
        st.pyplot(scatter_plot_2)

    st.subheader("Relationship between sentiment of a **poem** compared to the **passage** it is derived from")
    col1, col2 = st.columns(2)

    with col1:
        #sentiment of passage vs poem scatter plot
        scatter_plot_3 = dp.get_scatterplot("poem-polarity", "passage-polarity", "Polarity: Poem compared to Passage", "cyan")
        st.pyplot(scatter_plot_3)

    with col2:
        scatter_plot4 = dp.get_scatterplot("poem-subjectivity", "passage-subjectivity", "Subjectivity: Poem compared to Passage", "blue")
        st.pyplot(scatter_plot4)

    #scatter plot poem word count vs perplexity scores
    st.subheader("Weak negative correlation between poems word count and their perplexity scores")
    fig = dp.get_scatterplot("ppl-gpt2", "poem-word-count", "Poem word count compared to perplexity scores", "grey")
    st.pyplot(fig)

    #data cleaning pie chart
    st.subheader("Pie chart of data that was cleaned from original dataset")
    fig = plot.figure(dp.plot_cleaning_pie_chart())
    st.pyplot(fig)

    #WORDCLOUDS and word frequencies
    st.subheader("Word frequencies for passages (input) vs poems (output):", divider="rainbow")
    st.write("_Note: Without stopwords_")
    
    col1, col2 = st.columns(2)

    st.write("Frequency of most common words in both 'passage' and 'poem'")

    show_tables = st.toggle("_Show frequency tables._")

#!!!!!!! BUG WHERE MORE WORDS ARE DISPLAYED THAN ASKED FOR!!!!!!!!!!!!!!!
    how_many = 3 #default
    options = ["3", "5", "10", "20"]
    input = st.pills("How many top words in common to display", options)
    if(input is not None):
        how_many = int(input)                    

    with col1:
    #wordcloud
        st.write("**_Poems_**")
        wc_fig_1 = dp.generate_wordcloud("poems", "BuPu")
        st.pyplot(wc_fig_1)
        #tables of frequencies
        most_common_df_1 = pandas.DataFrame(
            dp.get_most_common_words("poems",how_many),
            columns = ["word", "frequency"])

        if show_tables:
            st.dataframe(most_common_df_1, use_container_width=True, hide_index= True)

    with col2:
    #wordcloud
        st.write("**_Passages_**")
        wc_fig_2 = dp.generate_wordcloud("passages", "RdPu")
        st.pyplot(wc_fig_2)

    #tables of frequencies
        most_common_df_2 = pandas.DataFrame(
            dp.get_most_common_words("passages",how_many),
            columns = ["word", "frequency"])

        if show_tables:
            st.dataframe(most_common_df_2, use_container_width=True, hide_index= True)
    
    #stacked bar chart
    st.bar_chart(dp.overall_word_freq(how_many), x="word", y="frequency", color="source", horizontal=True)


### DATA EXPLORATION PAGE
if page == "Syntax & Sentiment Analysis":

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
    filter = clean_df_v2["poem-pos"].apply(
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
    st.write(filtered_poems[["poem", "poem-pos"]])

    "✦•····················•✦•····················•✦"*4

    "🔎 Find poems with specific sentiment expressed"

    col1, col2 = st.columns(2)

    sentiment_tags = ["Negative emotion", "Positive emotion", "Neutral emotion"]
    subjectivity_tags = ["Objective", "Subjective"]

    ###choose how to filter poems
    #left column, sentiment polarity selection
    with col1:
        polarity_selection = st.segmented_control(
                "Type of emotion",
                sentiment_tags)

    #left column, sentiment subjectivity selection
    with col2:
        subjectivity_selection = st.segmented_control(
                "Subjectivity of text",
                subjectivity_tags)

    #no filtering masks done by creating new series with all values = true, same indices as clean_df_v2
    polarity_filter = pandas.Series(True, index=clean_df_v2.index)
    subjectivity_filter = pandas.Series(True, index=clean_df_v2.index)

    #filtering by polarity
    if polarity_selection == "Negative emotion":
        polarity_filter = clean_df_v2["poem-polarity"] < 0
    elif polarity_selection == "Positive emotion":
        polarity_filter = clean_df_v2["poem-polarity"] > 0
    elif polarity_selection == "Neutral emotion":
        polarity_filter = clean_df_v2["poem-polarity"] == 0 
    #filtering by subjectivity
    if subjectivity_selection == "Objective":
        subjectivity_filter = clean_df_v2["poem-subjectivity"] <= 0.5
    elif subjectivity_selection == "Subjective":
        subjectivity_filter = clean_df_v2["poem-subjectivity"] > 0.5

    #combining and applying filters
    combined_filter = polarity_filter & subjectivity_filter
    filtered_poems_s = clean_df_v2[combined_filter]

    #display poems
    st.write(f"Poems with following filters applied: **{polarity_selection}** and **{subjectivity_selection}**")
    "There are ", len(filtered_poems_s), " poems to display."
    st.write(filtered_poems_s[["poem", "poem-polarity", "poem-subjectivity"]])
    
if page == "Themes exploration":

    st.subheader(
        "Explore poem themes through clustering analysis")
    
    themes_fig = pio.read_json("files/poem_clusters.json")
    st.plotly_chart(themes_fig)

    st.write("_Please activate your browswer's light mode for better visibility of the hover labels._\n")

    "🔎 Find poems with specific a specific theme"

    #choose theme to use
    themes = clean_df_v2["poem-theme"].unique().tolist()

    user_selection = st.selectbox(
            "Select a theme:",
            themes,
            placeholder="Choose a theme to filter poems"
        )
    

    #filter poems, only show poems with selected theme
    filtered_poems = clean_df_v2[clean_df_v2["poem-theme"] == user_selection]
        
    #display poems
    st.write(f"Poems with following theme: **{user_selection}**")
    "There are ", len(filtered_poems), " poems to display."
    st.write(filtered_poems[["poem", "poem-theme"]])

   #get random poem from selected theme
    if st.button("Get a random poem from this theme"):
        random_poem = filtered_poems.sample(n=1)
        st.write(random_poem[["poem", "poem-theme", "poem-polarity", "poem-subjectivity"]])        
        #describe its sentiment
        if random_poem["poem-polarity"].values[0] < 0:
            polarity_desc = "negative emotion"
        elif random_poem["poem-polarity"].values[0] > 0:
            polarity_desc = "positive emotion"
        else:
            polarity_desc = "neutral emotion"
        if random_poem["poem-subjectivity"].values[0] <= 0.5:
            subjectivity_desc = "objective"
        else:
            subjectivity_desc = "subjective"
        st.write(f"This poem expresses **{polarity_desc}** and its tone is **{subjectivity_desc}**.")

if page == "Poem recommender":
    st.subheader("Select 5 poems you like, and get recommendations for similar poems!")

### VERSION HISTORY PAGE
if page == "See all versions of dataset":

    expand = st.expander("Cleaned Dataset with POS Tags & Sentiment scores", icon=":material/info:")
    expand.dataframe(clean_df_v2, use_container_width=True)    
 
    expand = st.expander("The cleaned dataset", icon=":material/info:")
    expand.dataframe(dp.clean_df, use_container_width=True)

    expand = st.expander("The original Blackout dataset", icon=":material/info:")
    expand.dataframe(dp.blackout_df, use_container_width=True)




