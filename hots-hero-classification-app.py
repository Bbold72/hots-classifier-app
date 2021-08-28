import streamlit as st
import pandas as pd
import pickle
import os

dir_data = 'data'
dir_output = 'output'

df = pd.read_csv(os.path.join(dir_data, 'herodata.csv'))
df = df.drop(['speed', 'sight', 'life_scale', 'life_regenScale', 'weapon_damageScale'], axis=1)
df = df.drop(['hero', 'role'], axis=1)


agg_df = df.agg(['min', 'max', 'median'])
print(agg_df)
print(agg_df.loc['min', 'rating_damage'])

st.write("""
# Simple Heros of the Storm Prediction App
This app predicts the **role** of a hero given specified attributes!
""")

# slider for user to adjust inputs to model
st.sidebar.header('User Input')
def make_slider(var_name, slider_name):
    return st.sidebar.slider(slider_name, float(agg_df.loc['min', var_name]), float(agg_df.loc['max', var_name]), float(agg_df.loc['median', var_name]))


def user_input_features():
    # min, max, default
    rating_damage = make_slider('rating_damage', 'Rating Damage')
    rating_survivability = make_slider('rating_damage', 'Rating Survivability')
    rating_utility = make_slider('rating_damage', 'Rating Utility')
    life_amount = make_slider('rating_damage', 'Life Amount')
    life_regenRate = make_slider('life_regenRate', 'Life Regeneration Rate')
    weapon_damage = make_slider('weapon_damage', 'Weapon Damage')
    weapon_period = make_slider('weapon_period', 'Weapon Period')
    weapon_range = make_slider('weapon_damage', 'Weapon Range')
    data = {'Rating Damage': rating_damage,
            'Rating Survivability': rating_survivability,
            'Rating Utility': rating_utility,
            'Life Amount': life_amount,
            'Life Regeneration Rate': life_regenRate,
            'Weapon Damage': weapon_damage,
            'Weapon Period': weapon_period,
            'Weapon Range': weapon_range}
    features = pd.DataFrame(data, index=[0])
    return features

# return user input as a dataframe
user_df = user_input_features()


# format dataframe for output
user_df_display = user_df.T 
user_df_display.columns = ['Input']
user_df_display.index.names = ['Parameter']

# display user's input
st.subheader('User Input parameters')
st.write(user_df_display)


# load the model from disk
loaded_model = pickle.load(open('rf_model.sav', 'rb'))

# predict hero role based on user input
prediction = pd.DataFrame(loaded_model.predict(user_df), columns=['Role'])
prediction_proba = pd.DataFrame(loaded_model.predict_proba(user_df), columns=loaded_model.classes_)


# display model prediction
# st.subheader('Prediction')
st.write(prediction)

# Prediction Probabilities for each role
st.subheader('Prediction Probability')
st.write(prediction_proba)

