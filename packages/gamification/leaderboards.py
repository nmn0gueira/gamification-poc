import pandas as pd
from pandas.api.types import CategoricalDtype

# Ordinal suffixes
ORDINAL_SUFFIXES = ['st', 'nd', 'rd'] + ['th'] * 17 + ['st', 'nd', 'rd'] + ['th'] * 7 + ['st']

def create_unordered_empty_leaderboard(number_of_players, columns):
    placements = [i for i in range(number_of_players)]
    df = pd.DataFrame(index=placements, columns=["Player"] + columns + ["Total Points"])
    df["Total Points"] = 0

    return df


def finalize_leaderboard(df):
    """
    Finalizes the leaderboard by sorting the dataframe by the total points column,
    resetting the index and converting the index to Ordinal type with the defined suffixes
    :param df: The leaderboard dataframe"""

    df["Player"] = df.index.copy() + 1  # Set the player column to the placement + 1

    # Sort the dataframe by the total points column
    df.sort_values(by=["Total Points", "Player"], ascending=[False, True], inplace=True)

    df.reset_index(drop=True, inplace=True)  # Reset the index

    # Convert the index to Ordinal type with the defined suffixes
    df.index = (df.index + 1).to_series().astype(CategoricalDtype(ordered=True)).map(
        lambda x: f"{x}{ORDINAL_SUFFIXES[x - 1]}")
    
    # Rename the index to Placement
    df.index.name = "Placement"
    
    return df
