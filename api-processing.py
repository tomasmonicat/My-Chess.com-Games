# -*- coding: utf-8 -*-
"""
Script that extract monthly games from a user of chess.com
"""

import pandas as pd
import requests
import re
import sys
import os

def moves_and_clocks(pgn):
    """
    Helper function that returns total amount of moves and the ending
    clocks for both black and white.
    """
    temp = re.findall("(\d+)\.{1,3} \w+\d \{\[%clk (\d:\d{2}:\d{2}\.?\d?)\]\}", pgn)
    if temp[-1][0] == temp[-2][0]:
        white_clock = temp[-2][1]
        black_clock = temp[-1][1]
    else:
        white_clock = temp[-1][1]
        black_clock = temp[-2][1]
    
    return [temp[-1][0], white_clock, black_clock]

def result(df):
    """
    Helper function that returns the result of the game (win, loss, draw) for
    the player and how it happened.
    """
    draw_conditions = ["agreed", "repetition", "stalemate", "insufficient", "timevsinsufficient"]
    loose_conditions = ["checkmated", "timeout", "resigned", "abandoned"]
    
    if df["white_result"] in draw_conditions:
        result = "draw"
        game_ending = df["white_result"]
        
    elif df["white_result"] in loose_conditions:
        game_ending = df["white_result"]
        if df["white_username"] == "DelTomaTe":
            result = "loss"
        else:
            result = "win"
            
    else:
        game_ending = df["black_result"]
        if df["white_username"] == "DelTomaTe":
            result = "win"
        else:
            result = "loss"
            
    return result, game_ending

def to_seconds(time):
    """
    Takes a string AA:BB:CC.D with AA=hours, BB=minutes, CC=seconds, 
    D=tenths of second and returns the amount of seconds as float.
    """
    hours, minutes, seconds = re.split(":", time)
    return int(hours)*3600 + int(minutes)*60 + float(seconds)

def monthly_games(username, year, month):
    """
    You will need pandas package installed to run this script.
    The function takes three parameters:
        1. username: chess.com username id as string,
        2. year: four digits,
        3. month: two digits,
        
    writes a csv named MMYYYY.csv with all your games of the month selected,
    with the following headers:
        1. pieces with which you played,
        2. result of the game (win/loss/draw),
        3. how the game ended (checkmated, timeout, etc),
        4. timestamp when the game ended,
        5. amount of moves,
        6. rating of white player,
        7. accuracy of white player,
        8. rating of black player,
        9. accuracy of black player,
        10. seconds remaining for white,
        11. seconds remaining for black,
        12. time control (600, 150, etc),
        13. time class (rapid/blitz/bullet).
    """
    url =  "https://api.chess.com/pub/player/{}/games/{}/{}".format(username, year, month)
    response = requests.get(url).json()
    
    df = pd.DataFrame(response["games"])
    
    df[["white_accuracy", "black_accuracy"]] = df["accuracies"].apply(pd.Series)[["white", "black"]]

    df[["white_rating", "white_result", "white_id", "white_username"]] = df["white"].apply(pd.Series)[["rating", "result", "@id", "username"]]
    df[["black_rating", "black_result", "black_id", "black_username"]] = df["black"].apply(pd.Series)[["rating", "result", "@id", "username"]]

    
    df[["moves", "white_clock", "black_clock"]] = df["pgn"].apply(moves_and_clocks).apply(pd.Series)    
    
    df[["result", "game_ending"]] = df.apply(result, axis=1).apply(pd.Series)
    
    df["pieces"] = df["white_username"].apply(lambda x: "white" if x == username else "black")    
    
    df["white_seconds"] = df["white_clock"].apply(to_seconds)
    df["black_seconds"] = df["black_clock"].apply(to_seconds)
    
    games_df = df[["pieces", "result", "game_ending", "end_time", "moves", "white_rating", "white_accuracy", "black_rating", "black_accuracy", "white_seconds", "black_seconds", "time_control", "time_class"]]
    
    if not os.path.isdir("games"):
        os.mkdir("games")
        
    save_file = os.path.join("games/", "{}{}.csv".format(month, year))
    games_df.to_csv(save_file, index=False, header=True)

if __name__ == "__main__":
    monthly_games(sys.argv[1], sys.argv[2], sys.argv[3])