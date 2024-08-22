import streamlit as st
import time
import pickle
import numpy as np
import pandas as pd
import os

# Miami Heat Color Scheme
PRIMARY_COLOR = "#98002E"  # Red
FONT_COLOR = "#FFFFFF"  # White

# Function to add custom CSS for Miami Heat theme, background gradients, animations, and fonts
def add_custom_css():
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap');
            body {{
                background-color: #ffffff;
                color: {PRIMARY_COLOR};
                font-family: 'Roboto', sans-serif;
            }}
            .stButton>button {{
                background-color: {PRIMARY_COLOR};
                color: {FONT_COLOR};
                border-radius: 8px;
                font-weight: bold;
                transition: transform 0.3s;
            }}
            .stButton>button:hover {{
                transform: scale(1.05);
            }}
            .stTextInput>div>input {{
                background-color: #f0f0f0;
                color: #000000;
            }}
            .stNumberInput>div>input {{
                background-color: #f0f0f0;
                color: #000000;
            }}
            .stMarkdown h1 {{
                color: {PRIMARY_COLOR};
                font-family: 'Oswald', sans-serif;
                font-size: 40px;
                font-weight: 900;
            }}
            .stMarkdown h2 {{
                color: {PRIMARY_COLOR};
            }}
            .stMarkdown p {{
                font-weight: bold;
                color: #4b4b4b;
            }}
            .css-18e3th9 {{
                font-family: 'Roboto', sans-serif;
            }}
            .prediction-text {{
                font-size: 20px;
                color: #333333;
            }}
            .trademark {{
                font-size: 12px;
                color: #4b4b4b;
                text-align: center;
                margin-top: 50px;
                font-family: 'Roboto', sans-serif;
                font-style: italic;
            }}
        </style>
    """, unsafe_allow_html=True)

# Add custom CSS
add_custom_css()

# Display the title and Heat logo
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("# MIAMI HEAT PLAYER PERFORMANCE TOOL")
with col2:
    st.image('heat-logo.png', width=70)

# Tool Explanation
st.markdown("""
Welcome to the Miami Heat Player Performance Tool! This tool analyzes player data, including 10-game rolling averages and last game stats, to provide predictions on a player's future performance. 
It factors in historical game logs, opponent-specific data, and rest days to deliver personalized predictions for each player. Select a player, their opponent team, and specify rest days to generate predictions.
""")

# Load player CSV data
csv_folder_path = 'Miami Heat 2023-2024 Roster Game Logs'  # Adjusted for relative path

# Get list of players from CSV files
player_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
players = [os.path.splitext(f)[0] for f in player_files]

# Player Selection from Dropdown
player = st.selectbox("Select a player", ['-'] + players)

# Team selection
team = st.selectbox("Select a team", ["-", "BOS", "CHI", "CLE", "DET", "IND", "MIL", "PHI", "ATL", "ORL", "MIA", "WAS", "NYK", "BKN", "TOR", "CHA"])

# Rest days input
rest_days = st.number_input("Rest Days", min_value=0, value=0)

# Proceed only if a player is selected
if player != '-':
    # Load selected player's data
    player_data = pd.read_csv(os.path.join(csv_folder_path, f"{player}.csv"))

    # Ensure 'PTS', 'AST', 'TRB' columns are numeric, coerce errors to NaN
    player_data['PTS'] = pd.to_numeric(player_data['PTS'], errors='coerce')
    player_data['AST'] = pd.to_numeric(player_data['AST'], errors='coerce')
    player_data['TRB'] = pd.to_numeric(player_data['TRB'], errors='coerce')

    # Drop rows with NaN values in important columns
    player_data = player_data.dropna(subset=['PTS', 'AST', 'TRB'])

    # Calculate the 10-game rolling averages and last game stats
    rolling_avg_points = player_data['PTS'].tail(10).mean()
    rolling_avg_assists = player_data['AST'].tail(10).mean()
    rolling_avg_rebounds = player_data['TRB'].tail(10).mean()

    last_game_points = player_data['PTS'].iloc[-1]
    last_game_assists = player_data['AST'].iloc[-1]
    last_game_rebounds = player_data['TRB'].iloc[-1]

    # Display the calculated stats
    st.write(f"**10-Game Rolling Average Points:** {rolling_avg_points:.2f} | **Points Last Game:** {last_game_points}")
    st.write(f"**10-Game Rolling Average Assists:** {rolling_avg_assists:.2f} | **Assists Last Game:** {last_game_assists}")
    st.write(f"**10-Game Rolling Average Rebounds:** {rolling_avg_rebounds:.2f} | **Rebounds Last Game:** {last_game_rebounds}")

    # Load the trained model
    with open('player_performance_model_multi.pkl', 'rb') as file:
        model = pickle.load(file)

    # Predict button functionality
    if st.button("Predict"):
        with st.spinner("Calculating predictions..."):
            time.sleep(1)  # Simulate a small delay for effect

            # Prepare input data for prediction
            input_data = np.array([
                rolling_avg_points,
                rolling_avg_assists,
                rolling_avg_rebounds,
                last_game_points,
                last_game_assists,
                last_game_rebounds,
                rest_days
            ]).reshape(1, -1)

            # Make predictions using the model
            predicted_performance = model.predict(input_data)

            predicted_points = predicted_performance[0][0]
            predicted_assists = predicted_performance[0][1]
            predicted_rebounds = predicted_performance[0][2]

            # Apply "vs Team" adjustment
            if team != '-':
                team_data = player_data[player_data['Opp'] == team]
                if team_data.empty:
                    st.write(f"Didn't play against {team} last season")
                else:
                    # Apply adjustments based on historical performance vs team
                    team_avg_points = team_data['PTS'].mean()
                    team_avg_assists = team_data['AST'].mean()
                    team_avg_rebounds = team_data['TRB'].mean()

                    # Adjust the prediction
                    predicted_points += (team_avg_points - rolling_avg_points) * 0.1  # Small adjustment weight
                    predicted_assists += (team_avg_assists - rolling_avg_assists) * 0.1
                    predicted_rebounds += (team_avg_rebounds - rolling_avg_rebounds) * 0.1

            # Display the predicted performance
            st.subheader("Predicted Performance:")
            st.write(f"🏀 **Predicted Points**: {predicted_points:.2f}")
            st.write(f"🎯 **Predicted Assists**: {predicted_assists:.2f}")
            st.write(f"🔄 **Predicted Rebounds**: {predicted_rebounds:.2f}")

# Trademark Section at the bottom with a more professional tone
st.markdown("<p class='trademark'>© 2024 Jacob Zonis - Developer & Data Analyst. All Rights Reserved.</p>", unsafe_allow_html=True)

