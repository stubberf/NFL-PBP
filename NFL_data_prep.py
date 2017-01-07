# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 03:47:53 2016

@author: stubberf
This script does some additional data prep to the initial pbp datasets
"""

import pandas as pd
import numpy as np
import os


def add_team(df):
    #this function adds a column for team1 & team2
    tNames = df.groupby(['GameId'])['DefenseTeam'].unique()
    tNames = tNames[df['GameId']].tolist()  #convert to a list and back to df
    tNames = pd.DataFrame( tNames )         #to get rid of array in every row
    df['Team1'] = tNames.iloc[:,0]
    df['Team2'] = tNames.iloc[:,1]
    return df


def add_time(df):
    #this function adds a column for cumlative game time (sec.) for each play
    df['Time'] = (df['Quarter']-1)*900 + (15-df['Minute']-1)*60 + (60-df['Second'])
    return df
    
    
def add_scores(df):
    #this function add columns of game info for each game

    #add dummie columns to the df to be filled in later
    df['Team1Score'], df['Team2Score'] = 0, 0
    df['PointDiff'] = 0
    df['Team1Yards'], df['Team2Yards'] = 0, 0
    df['YardDiff'] = 0
    df['Team1NumPlays'], df['Team2NumPlays'] = 0, 0
    df['NumPlaysDiff'] = 0
    df['Team1Win'] =0
    gIds = df['GameId'].unique()
    for gId in gIds:
        dfSingleGame = score_game(df[df['GameId'] == gId])
        dfSingleGame = game_stats(dfSingleGame)
        df[df['GameId'] == gId] = dfSingleGame
    return df


def score_game(df):
    #this function add columns of game info for a game
    df = df.sort_values(['GameId','Time'], ascending=True)
    t1Score, t2Score = [], []
    runningScoreOpp = { df['Team1'].iloc[0]:0,  df['Team2'].iloc[0]:0 }
    for i in range(len(df)):
        row = df.iloc[i,:]
        desc = str(row['Description'])    #insure description in string format
        #fumble recovered by defense
        fumbleDR = desc.find('RECOVERED BY '+str(row['DefenseTeam']) ) 
        #fumble recovered by offense
        fumbleOR = desc.find('RECOVERED BY '+str(row['OffenseTeam']) ) 
        TD = desc.find(', TOUCHDOWN')

        #list of plays that score points
        #touchdown no turnover    
        if row['IsTouchdown'] == 1 and \
        (row['IsFumble'] == 0 or \
        (row['IsFumble'] == 1 and fumbleOR >0  and fumbleOR < TD)) and \
        row['IsInterception'] == 0 and \
        row['IsNoPlay'] == 0:
            #Normal call or a call that is reversed and now is a TD
            if (desc.find(' REVERSED') == -1) or \
            (desc.find(' REVERSED') > 0 and desc.find(' REVERSED') < TD):
                runningScoreOpp[ row['DefenseTeam'] ] += 6
        #touchdown off of turnover    
        if row['IsTouchdown'] == 1 and \
        (row['IsFumble'] == 1 and fumbleDR > 0 and fumbleDR < TD or \
        row['IsInterception'] == 1) and \
        row['IsNoPlay'] == 0:
            #Normal call or a call that is reversed and now is a TD
            if (desc.find(' REVERSED') == -1) or \
            (desc.find(' REVERSED') > 0 and desc.find(' REVERSED') < TD):
                runningScoreOpp[ row['OffenseTeam'] ] += 6
        #extra point
        if row['PlayType']=='EXTRA POINT' and \
        desc.find('IS GOOD') > 0 and \
        row['IsNoPlay'] == 0:
            runningScoreOpp[ row['DefenseTeam'] ] += 1
        #2 point attempt
        if row['PlayType']=='TWO-POINT CONVERSION' and \
        desc.find('ATTEMPT SUCCEEDS') > 0 and \
        row['IsNoPlay'] == 0:
            runningScoreOpp[ row['DefenseTeam'] ] += 2
        #field goal
        if row['PlayType']=='FIELD GOAL' and \
        desc.find('IS GOOD') > 0 and \
        row['IsNoPlay'] == 0:
            runningScoreOpp[ row['DefenseTeam'] ] += 3
        #safety
        if desc.find(', SAFETY') > 0 and row['IsNoPlay'] == 0:
            runningScoreOpp[ row['OffenseTeam'] ] += 2
        # Scores after this play
        #We use deffensive team name to track the offensive scores, because the
        # offensive team name is sometimes missing in dataset
        t1Score.append( runningScoreOpp[row['Team2']] ) 
        t2Score.append( runningScoreOpp[row['Team1']] )
        
        #print row['Description']
        #print runningScoreOpp
    #Add scores to DF
    df['Team1Score'] = t1Score
    df['Team2Score'] = t2Score
    df['PointDiff'] = np.array(t1Score) - np.array(t2Score)
    if t1Score[-1] > t2Score[-1]:
        df['Team1Win'] = np.ones( (len(df),), dtype=np.int64 )
    else:
        df['Team1Win'] = np.zeros( (len(df),), dtype=np.int64 )
    return df


def game_stats(df):
    #this function add columns of game info for a game
    df = df.sort_values(['GameId','Time'], ascending=True)
    t1Yards, t2Yards = [], []
    t1Plays, t2Plays = [], []
    runningTotalYardsOpp = { df['Team1'].iloc[0]:0,  df['Team2'].iloc[0]:0 }
    runningTotalPlaysOpp = { df['Team1'].iloc[0]:0,  df['Team2'].iloc[0]:0 }
    for i in range(len(df)):
        row = df.iloc[i,:]
        runningTotalYardsOpp[ row['DefenseTeam'] ] += row['Yards']
        runningTotalPlaysOpp[ row['DefenseTeam'] ] += 1
    
        # Total Yards after this play
        #We use deffensive team name to track the offensive scores, because the
        # offensive team name is sometimes missing in dataset
        t1Yards.append( runningTotalYardsOpp[row['Team2']] ) 
        t2Yards.append( runningTotalYardsOpp[row['Team1']] )
        t1Plays.append( runningTotalPlaysOpp[row['Team2']] )
        t2Plays.append( runningTotalPlaysOpp[row['Team1']] )

    #Add Total Yards to DF
    df['Team1Yards'], df['Team2Yards'] = t1Yards, t2Yards
    df['YardDiff'] = np.array(t1Yards) - np.array(t2Yards)
    df['Team1NumPlays'], df['Team2NumPlays'] = t1Plays, t2Plays
    df['NumPlaysDiff'] = np.array(t1Plays) - np.array(t2Plays)
    return df


def add_ppp (df):
    df['PPPT1'] = df['Team1Score'] / ( df['Team1NumPlays'] + 1 )
    df['PPPT2'] = df['Team2Score'] / ( df['Team2NumPlays'] + 1 )
    df['PPPDiff'] = df['PPPT1'] - df['PPPT2']
    return df
    
    
def add_time_score_interaction (df):
    df['TimeScore'] = df['TimeLeft'] * df['Team1Score']
    return df








###############################################################################
#   Start of Main Portion of Script
###############################################################################

os.chdir("ENTER YOUR WORKING DIRECTORY")
fileList = ["Datasets\\pbp-2013.csv",
            "Datasets\\pbp-2014.csv",
            "Datasets\\pbp-2015.csv"]

results = []
for f in fileList:
    df = pd.read_csv(f, sep=',', escapechar="\\")

    df = add_time(df)
    df = add_team(df)
    df = add_scores(df)
    df = add_ppp(df)
    results.append(df)

#Merge results into 1 dataframe
result = pd.concat(results)
#Output the results to CSV file
result.to_csv("Datasets\\pbp-final_V2.csv", sep=',', escapechar="\\" )

#Uncomments of the lines below to view a summary of all of the scores
#scores = df.loc[:, ['GameId','GameDate','Team1','Team2','Team1Score','Team2Score','Team1Win']]
#print scores.groupby(['GameId','GameDate']).max()