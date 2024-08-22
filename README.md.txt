Miami Heat Player Performance Tool

Overview

The **Miami Heat Player Performance Tool** is designed to predict the performance of Miami Heat players by analyzing their recent game data. The tool uses historical game logs to calculate 10-game rolling averages, last game statistics, and takes into account team-specific performance and rest days to generate personalized predictions for points, assists, and rebounds.

Features

- **Player Selection**: Choose a Miami Heat player from the 2023-2024 roster.
- **Team Selection**: Select the opposing team to factor in team-specific performance.
- **Rest Days Input**: Specify the number of rest days since the player's last game.
- **Predictions**: The tool uses historical data to predict points, assists, and rebounds based on rolling averages and recent performance.

How It Works

1. **Select a Player**: Choose a player from the dropdown list.
2. **Select a Team**: Pick the opposing team.
3. **Input Rest Days**: Enter the number of days since the player’s last game.
4. **Click "Predict"**: The tool will analyze the data and provide a prediction based on the player's recent form and performance against the selected team.

The tool pulls the data from past game logs and calculates the rolling averages over the last 10 games. It also factors in rest days and past performances against specific teams to generate more accurate predictions.

Requirements

To run the project, you will need the following Python packages installed:

```
streamlit
pandas
numpy
scikit-learn
```

Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/YourUsername/Miami-Heat-PPP-Tool.git
    ```
2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

Files Included

- **app.py**: The main script that runs the Streamlit app.
- **player_performance_model_multi.pkl**: The trained machine learning model used for predictions.
- **heat-logo.png**: The Miami Heat logo image used in the UI.
- **Miami Heat 2023-2024 Roster Game Logs**: A folder containing CSV files with the game logs for each player.

License

This project is licensed under the MIT License.

---

Contact

For inquiries, feel free to reach out to **Jacob Zonis**.

