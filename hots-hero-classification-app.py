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
    data = {'rating_survivability': rating_survivability,
            'rating_utility': rating_utility,
            'life_amount': life_amount,
            'life_regenRate': life_regenRate,
            'weapon_damage': weapon_damage,
            'weapon_period': weapon_period,
            'weapon_range': weapon_range}
    features = pd.DataFrame(data, index=[0])
    return features

user_df = user_input_features()

st.subheader('User Input parameters')
st.write(user_df.T)


# load the model from disk
loaded_model = pickle.load(open('rf_model.sav', 'rb'))



