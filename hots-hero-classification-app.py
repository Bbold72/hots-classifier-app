import streamlit as st
import pandas as pd
import os

dir_data = 'data'
dir_output = 'output'

df = pd.read_csv(os.path.join(dir_data, 'herodata.csv'))
df = df.drop(['speed', 'sight', 'life_scale', 'life_regenScale', 'weapon_damageScale'], axis=1)
df = df.drop(['hero', 'role'], axis=1)


agg_df = df.agg(['min', 'max', 'median'])
print(agg_df)
print(agg_df.loc['min', 'rating_damage'])

