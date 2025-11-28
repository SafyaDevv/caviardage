import streamlit as st
import data_cleaning as data
import matplotlib.pyplot as plot
import numpy

st.title("Caviardage 📜🐙")

df = data.blackout_df
clean_data = data.clean_df

#st.set_page_config(layout="wide") #make page full width

st.write(
    "Woop woop here comes the data.",
)

fig = plot.figure(data.plot_data_cleaning_chart())
st.pyplot(fig)

expand = st.expander("The original Blackout dataset", icon=":material/info:")
expand.dataframe(df, use_container_width=True)

expand = st.expander("The cleaned dataset", icon=":material/info:")
expand.dataframe(clean_data, use_container_width=True)

#TRYING OUT TOGGLES
#displayDataFrame = st.toggle("Display full original dataset")

# if displayDataFrame:
#     st.subheader("The original Blackout dataset")
#     st.dataframe(data, use_container_width=True)

