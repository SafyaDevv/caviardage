import streamlit as st
import data_exploration as data_exp

st.title("Caviardage 📜🐙")

data = data_exp.dataFrame

st.write(
    "Woop woop",
)

#TRYING OUT TOGGLES
#displayDataFrame = st.toggle("Display full original dataset")

# if displayDataFrame:
#     st.subheader("The original Blackout dataset")
#     st.dataframe(data, use_container_width=True)


expand = st.expander("The original Blackout dataset", icon=":material/info:")
expand.dataframe(data, use_container_width=True)

