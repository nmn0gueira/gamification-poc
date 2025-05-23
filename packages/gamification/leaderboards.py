import pandas as pd
from pandas.api.types import CategoricalDtype

def create_unordered_empty_leaderboard(number_of_players, columns):
    """
    Creates an unordered empty leaderboard dataframe with the specified number of players and columns
    :param number_of_players: The number of players
    :param columns: The columns of the leaderboard
    :return: The leaderboard dataframe
    """
    placements = [i for i in range(number_of_players)]
    df = pd.DataFrame(index=placements, columns=["Player"] + columns + ["Total Points"])
    df["Total Points"] = 0

    return df


def finalize_leaderboard(df):
    """
    Finalizes the leaderboard by sorting the dataframe by the total points column,
    resetting the index and converting the index to Ordinal type with the defined suffixes
    :param df: The leaderboard dataframe
    :return: The finalized leaderboard dataframe
    """
    df["Player"] = df.index.copy() # Set the player column to the placement + 1

    # Sort the dataframe by the total points column
    df.sort_values(by=["Total Points", "Player"], ascending=[False, True], inplace=True)

    df.reset_index(drop=True, inplace=True)  # Reset the index

    ordinal_suffixes = generate_ordinal_suffixes(len(df.index))  # Generate the ordinal suffixes

    # Convert the index to Ordinal type with the defined suffixes
    df.index = (df.index + 1).to_series().astype(CategoricalDtype(ordered=True)).map(
        lambda x: f"{x}{ordinal_suffixes[x - 1]}")
    
    # Rename the index to Placement
    df.index.name = "Placement"
    
    return df


def get_ordinal_suffix(number):
    """
    Returns the ordinal suffix of a number
    :param number: The number
    :return: The ordinal suffix
    """
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return suffix

def generate_ordinal_suffixes(count):
    """
    Generates a list of ordinal suffixes
    :param count: The number of suffixes to generate
    :return: The list of ordinal suffixes
    """
    ordinal_suffixes = [get_ordinal_suffix(i) for i in range(1, count + 1)]
    return ordinal_suffixes
