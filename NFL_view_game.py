# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 11:19:18 2016

@author: stubberf
Run this program to view output of cloud trained logistic regression alogrithim

Using Spyder 2.3.8

"""
import os, json, urllib2, random
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot') # Look Pretty





###############################################################################
#   Set Variables
###############################################################################
GAME_ID = 2015091312
API_KEY = 'ENTER YOUR AZURE API KEY'
URL = 'ENTER AZURE URL TO CLASSIC WEBSERVICE'
WORKING_DIR = "ENTER YOUR WORKING DIRECTORY"
PBP_FILE = "Datasets\\pbp-final_V2.csv"
DEV_ON = False





###############################################################################
#   Functions
###############################################################################
def predict (dataInput):
    data = {
        "Inputs": { "input1":{ 
                    "ColumnNames": ["Column 0", "GameId", "GameDate", "Quarter", "Minute", "Second", "OffenseTeam", "DefenseTeam", "Down", "ToGo", "YardLine", "Unnamed: 10", "SeriesFirstDown", "Unnamed: 12", "NextScore", "Description", "TeamWin", "Unnamed: 16", "Unnamed: 17", "SeasonYear", "Yards", "Formation", "PlayType", "IsRush", "IsPass", "IsIncomplete", "IsTouchdown", "PassType", "IsSack", "IsChallenge", "IsChallengeReversed", "Challenger", "IsMeasurement", "IsInterception", "IsFumble", "IsPenalty", "IsTwoPointConversion", "IsTwoPointConversionSuccessful", "RushDirection", "YardLineFixed", "YardLineDirection", "IsPenaltyAccepted", "PenaltyTeam", "IsNoPlay", "PenaltyType", "PenaltyYards", "Time", "Team1", "Team2", "Team1Score", "Team2Score", "PointDiff", "Team1Yards", "Team2Yards", "YardDiff", "Team1NumPlays", "Team2NumPlays", "NumPlaysDiff", "Team1Win", "PPPT1", "PPPT2", "PPPDiff"],
                    "Values": [ dataInput ]
        } },
        "GlobalParameters":  {}
    }
    body = str.encode(json.dumps(data))
    url = URL
    # Replace this with the API key for the web service    
    api_key = API_KEY 
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib2.Request(url, body, headers)
    try:
        if DEV_ON == True:
            return unicode(random.random())
        response = urllib2.urlopen(req)
        result = json.loads(response.read())
        #print(result)
        result = result['Results']['output1']['value']['Values'][0][1]

    except urllib2.HTTPError, error:
        print("The request failed with status code: " + str(error.code))
    return result
        
        
def setup_plot (row, prob=0):
    axes = plt.gca()
    axes.set_ylim([0,1])
    plt.title( 'NFL {0} vs. {1} Probability Of Winning'.format(row['Team1'],row['Team2']) )
    plt.ylabel('Probability', size='x-large')
    plt.text(0, .95, row['Team1'], weight='bold', size='x-large' )
    plt.text(0, .025, row['Team2'], weight='bold', size='x-large' )
    return


def process_game (gId, df):
    g = df[ df['GameId']==gId ]
    g = g.sort_values(['GameId','Time'], ascending=True)
    x, y = [], []
    
    #Setup Plot
    l = len(g)
    plt.ion()   #make the plot interactive
      
    for i in range(l):
        row = g.iloc[i,:]
        plt.clf()   #clear the plot
        prob = float( predict(row.tolist()) ) #case as float
        setup_plot (row, prob)
        pbp = "{0} prob({1:.2f}%)".format(row['Description'], prob*100)
        #print info about the current play
        print pbp
        plt.xlabel(pbp, size='small')
        #update the plot
        x.append(i)
        y.append(prob)                
        #plt.plot( i, prob, 'ro')        
        plt.plot( x, y, color='r', linewidth=2.0)
        plt.pause(1)
    return 'Done'





###############################################################################
#   Start of Main Portion of Script
###############################################################################
os.chdir(WORKING_DIR)


#set column names
names = [u'Column 0', u'GameId', u'GameDate', u'Quarter', u'Minute', u'Second',
    u'OffenseTeam', u'DefenseTeam', u'Down', u'ToGo', u'YardLine',
    u'Unnamed: 10', u'SeriesFirstDown', u'Unnamed: 12', u'NextScore',
    u'Description', u'TeamWin', u'Unnamed: 16', u'Unnamed: 17',
    u'SeasonYear', u'Yards', u'Formation', u'PlayType', u'IsRush',
    u'IsPass', u'IsIncomplete', u'IsTouchdown', u'PassType', u'IsSack',
    u'IsChallenge', u'IsChallengeReversed', u'Challenger', u'IsMeasurement',
    u'IsInterception', u'IsFumble', u'IsPenalty', u'IsTwoPointConversion',
    u'IsTwoPointConversionSuccessful', u'RushDirection', u'YardLineFixed',
    u'YardLineDirection', u'IsPenaltyAccepted', u'PenaltyTeam', u'IsNoPlay',
    u'PenaltyType', u'PenaltyYards', u'Time', u'Team1', u'Team2',
    u'Team1Score', u'Team2Score', u'PointDiff', u'Team1Yards',
    u'Team2Yards', u'YardDiff', u'Team1NumPlays', u'Team2NumPlays',
    u'NumPlaysDiff', u'Team1Win', u'PPPT1', u'PPPT2', u'PPPDiff']
#set column dtypes
dataType = {u'IsTwoPointConversion': np.int32, u'YardLineDirection': np.object, 
    u'IsPenalty': np.int32, u'SeasonYear': np.int32, u'PenaltyType': np.object, 
    u'NextScore': np.int32, u'Team1': np.object, u'Team2': np.object, 
    u'PenaltyTeam': np.object, u'YardLineFixed': np.int32, u'RushDirection': np.object, 
    u'IsInterception': np.int32, u'Team2Yards': np.int32, u'IsRush': np.int32, 
    u'SeriesFirstDown': np.int32, u'PlayType': np.object, u'Down': np.int32, 
    u'OffenseTeam': np.object, u'Description': np.object, u'Challenger': np.object, 
    u'Team1Win': np.int32, u'Team1Yards': np.int32, u'IsFumble': np.int32, 
    u'Formation': np.object, u'YardDiff': np.int32, u'Yards': np.int32, 
    u'Team2Score': np.int32, u'Team1Score': np.int32, u'Minute': np.int32, 
    u'TeamWin': np.int32, u'IsTwoPointConversionSuccessful': np.int32, 
    u'IsTouchdown': np.int32, u'YardLine': np.int32, u'GameDate': np.object, 
    u'NumPlaysDiff': np.int32, u'PenaltyYards': np.int32, u'IsChallenge': np.int32, 
    u'ToGo': np.int32, u'PassType': np.object, u'Team1NumPlays': np.int32, 
    u'PointDiff': np.int32, u'Time': np.int32, u'IsSack': np.int32, 
    u'Quarter': np.int32, u'IsPass': np.int32, u'IsNoPlay': np.int32, 
    u'IsIncomplete': np.int32, u'GameId': np.int32, u'DefenseTeam': np.object, 
    u'Column 0': np.int32, u'IsMeasurement': np.int32, u'PPPDiff': np.float64, 
    u'IsChallengeReversed': np.int32, u'Unnamed: 16': np.object, 
    u'Unnamed: 17': np.object, u'Second': np.int32, u'Team2NumPlays': np.int32, 
    u'Unnamed: 12': np.object, u'Unnamed: 10': np.object, u'PPPT1': np.float64, 
    u'IsPenaltyAccepted': np.int32, u'PPPT2': np.float64}

#read in data file
df = pd.read_csv(PBP_FILE, sep=',', escapechar="\\", 
                 names=names, header=0, dtype=dataType)
df.fillna('', inplace=True)
process_game(GAME_ID, df)
