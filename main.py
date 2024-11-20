import pandas as pd
import streamlit as st

st.markdown("<h1 style='text-align: center'>Food Feud</h1>", unsafe_allow_html=True)

RESTAURANT_SURVEY_STAGE = 1
RECIPE_GENERATION_STAGE = 2

PREFER_NUMBER = 20

if 'stage' not in st.session_state:
    st.session_state.stage = RESTAURANT_SURVEY_STAGE # Start stage

if "prefer" not in st.session_state:
    st.session_state.prefer = []

if "not_prefer" not in st.session_state:
    st.session_state.not_prefer = []

if "prefer_count" not in st.session_state:
    st.session_state.prefer_count = PREFER_NUMBER

if "survey_progress" not in st.session_state:
    st.session_state.survey_progress = 0

data_path = "data/"
data_file = "top_restaurants.csv"

@st.cache_data
def load_restaurant_data():
    return pd.read_csv(data_path+data_file)

def add_prefer(prefer): # Preference is a row in a DataFrame
    st.session_state.prefer.append(prefer) # Build up preferences!
    if st.session_state.survey_progress < 100:
        st.session_state.survey_progress += 100//PREFER_NUMBER
        st.session_state.prefer_count -= 1
        survey_progress_bar.progress(st.session_state.survey_progress, text=f"Select {st.session_state.prefer_count} more.")
    
df_restaurants = load_restaurant_data()

placeholder = st.empty()

if st.session_state.stage == RESTAURANT_SURVEY_STAGE:
    with placeholder.container():
        st.markdown("<h4 style='text-align: center'>Start by taking our survey of eating establishments whose food you enjoy.</h4>", unsafe_allow_html=True)
        survey_progress_bar = st.progress(st.session_state.survey_progress, text=f"Select {st.session_state.prefer_count} more.")
        restaurant = df_restaurants.sample()
        st.markdown("<h3 style='text-align: center'>"+restaurant.iloc[0]['name']+"</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        if col1.button('Yes 👍', type="secondary", use_container_width=True):
            add_prefer(restaurant)
        col2.button('No 👎', type="secondary", use_container_width=True)

if st.session_state.prefer_count == 0:
    placeholder.empty()
    st.balloons()
    st.session_state.stage = RECIPE_GENERATION_STAGE

if st.session_state.stage == RECIPE_GENERATION_STAGE:
    df_restaurant_preferences = pd.concat(st.session_state.prefer)
    st.dataframe(df_restaurant_preferences)