import streamlit as st
import pickle
import pandas as pd
import numpy as np

pipe = pickle.load(open('ipl.pkl', 'rb'))

teams1 = ['Mumbai Indians','Royal Challengers Bangalore', 'Chennai Super Kings', 'Kolkata Knight Riders',
          'Kings XI Punjab', 'Rajasthan Royals',
          'Delhi Daredevils', 'Sunrisers Hyderabad']

teams2 = ['Chennai Super Kings','Mumbai Indians','Royal Challengers Bangalore','Kolkata Knight Riders',
          'Kings XI Punjab', 'Rajasthan Royals',
          'Delhi Daredevils', 'Sunrisers Hyderabad']

st.title('IPL Score Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select batting team', teams1)
with col2:
    bowling_team = st.selectbox('Select bowling team', teams2)

col3, col4, col5 = st.columns(3)

with col3:
    overs = st.number_input('Overs done (select > 5 overs)', format="%.1f", min_value=5.1)
with col4:
    current_score = st.number_input('Current Score', step=1)
with col5:
    wickets = st.number_input('Wickets out', step=1, min_value=0, max_value=10)

last_five_runs = st.number_input('Runs scored in previous 5 overs (e.g., 42)', step=1)
last_five_wickets = st.number_input('Wickets taken in previous 5 overs (e.g., 2)', step=1)

if st.button('Predict Score'):
    if overs > 0:
        crr = current_score / overs

        # Calculate balls left based on overs completed
        overs_int = int(overs)
        overs_dec = float('0.' + str(overs).split('.')[1])
        balls = (20 - overs_int - 1) * 6 + (6 - ((overs_dec * 10) % 10 + 1))
        balls_left = int(balls)

        wickets_left = 10 - wickets

        # Create input DataFrame for model
        input_df = pd.DataFrame(
            {'bat_team': [batting_team], 'bowl_team': [bowling_team], 'runs': [current_score],
             'wickets': [wickets], 'overs': [overs], 'balls_left': [balls_left], 
             'wickets_left': [wickets_left], 'crr': [crr], 'runs_last_5': [last_five_runs], 
             'wickets_last_5': [last_five_wickets]})

        try:
            # Predict using the loaded pipeline
            result = pipe.predict(input_df)
            st.header(f"Predicted Score - {int(result[0]-2)} TO {int(result[0]+8)}")
        except Exception as e:
            st.error(f"Prediction error: {e}")
    else:
        st.warning("Overs must be greater than 0 to calculate the score.")
