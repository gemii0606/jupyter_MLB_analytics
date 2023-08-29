import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output
import requests
from bs4 import BeautifulSoup
import re
import requests
import matplotlib.pyplot as plt
import random

# getting the data from MLB database
# getting the batters' data
url = 'https://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2022/start/0'
page = requests.get(url)
content = page.text
soup = BeautifulSoup(content, 'html.parser')
header = soup.find('tr', attrs={'class':'colhead'})
columns = [col.get_text() for col in header.find_all('td')]
final_df_1 = pd.DataFrame(columns = columns)
# iterate the online pages
for i in range(0, 347, 50):
    url = 'https://www.espn.com/mlb/history/leaders/_/breakdown/season/year/2022/start/{}'.format(i)
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, 'html.parser')
    players = soup.find_all('tr', attrs={'class':re.compile('row player-10-')})
# forming the dataframe of batters
    for player in players:
        stats = [stat.get_text() for stat in player.find_all('td')]
        temp_df = pd.DataFrame(stats).transpose()
        temp_df.columns = columns
        final_df_1 = pd.concat([final_df_1, temp_df], ignore_index=True)
final_df_1['Role'] = 'batting'

# getting the pitchers' data
url = 'https://www.espn.com/mlb/history/leaders/_/type/pitching/breakdown/season/year/2022/sort/ERA/start/0'
page = requests.get(url)
content = page.text
soup = BeautifulSoup(content, 'html.parser')
header = soup.find('tr', attrs={'class':'colhead'})
columns = [col.get_text() for col in header.find_all('td')]
final_df_2 = pd.DataFrame(columns = columns)
# iterate the online pages
for i in range(0, 347, 50):
    url = 'https://www.espn.com/mlb/history/leaders/_/type/pitching/breakdown/season/year/2022/sort/ERA/start/{}'.format(i)
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, 'html.parser')
    players = soup.find_all('tr', attrs={'class':re.compile('row player-10-')})
# forming the dataframe of pitchers
    for player in players:
        stats = [stat.get_text() for stat in player.find_all('td')]
        temp_df = pd.DataFrame(stats).transpose()
        temp_df.columns = columns
        final_df_2 = pd.concat([final_df_2, temp_df], ignore_index=True)
final_df_2['Role'] = 'pitching'

# function to draw the radar chart
def Radar_chart(categories, valueDict, title, playerName = None, otherPlayerName = None):
    if playerName is None:
        print("No given player name!!")
        return 
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    # get the values for radar
    values = valueDict[playerName]
    
    
    values=np.concatenate((values,[values[0]]))
    angles=np.concatenate((angles,[angles[0]]))
    categories = np.concatenate((categories, [categories[0]]))
    # close radar chart
    
    # subplot the polar plot
    ax = plt.subplot(1, 1, 1, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2, label = playerName) # x:angles, y:values
    ax.fill(angles, values, alpha=0.25) # fill the polygon
    if not otherPlayerName is None:
        otherValues = valueDict[otherPlayerName]
        otherValues=np.concatenate((otherValues,[otherValues[0]]))
        ax.plot(angles, otherValues, 'o-', linewidth=2, label = otherPlayerName)
        ax.fill(angles, otherValues, alpha=0.25)
        title = title + playerName + ' V.S. ' + otherPlayerName
    else:
        title = title + playerName
    ax.set_thetagrids(np.degrees(angles), categories)
    # set the labels by the angles
    ax.set_title(title, size=14, weight='bold')
    ax.grid(True)
    plt.legend()
    plt.show()

# print batters' radar chart, and it provides the personal and comparisons within the same function
# it also standardize the data
def do_batting_chart(x, y = None):
    categories = np.array(['HR', 'RBI', 'BB', 'SB', 'H'])
    batting_PLAYER = data['PLAYER']
    batting_values = dict()
    ER_mean = np.array(data['HR'], dtype=float).mean()
    BB_mean = np.array(data['RBI'], dtype=float).mean()
    IP_mean = np.array(data['BB'], dtype=float).mean()
    SO_mean = np.array(data['SB'], dtype=float).mean()
    W_mean = np.array(data['H'], dtype=float).mean()
    ER_std = np.array(data['HR'], dtype=float).std()
    BB_std = np.array(data['RBI'], dtype=float).std()
    IP_std = np.array(data['BB'], dtype=float).std()
    SO_std = np.array(data['SB'], dtype=float).std()
    W_std = np.array(data['H'], dtype=float).std()
    for i in range(0, batting_PLAYER.size):
        batting_values[data['PLAYER'][i]] = [10*(float(data['HR'][i])-ER_mean)/ER_std+50, 
                                             10*(float(data['RBI'][i])-BB_mean)/BB_std+50,
                                             10*(float(data['BB'][i])-IP_mean)/IP_std+50,
                                             10*(float(data['SB'][i])/SO_mean)/SO_std+50,
                                             10*(float(data['H'][i])/W_mean)/W_std+50]

    if y is None:
        title = 'Individual Player Radar Chart: '
    else:
        title = 'Two Players Radar Chart: '
    # plot radar chart
    Radar_chart(categories, batting_values, title, playerName = x, otherPlayerName = y)

# print pitchers' radar chart, and it provides the personal and comparisons within the same function
# it also standardize the data
def do_pitching_chart(x, y = None):
    categories = np.array(['ER', 'BB', 'IP', 'SO', 'W'])
    batting_PLAYER = data['PLAYER']
    batting_values = dict()
    ER_mean = np.array(data['ER'], dtype=float).mean()
    BB_mean = np.array(data['BB'], dtype=float).mean()
    IP_mean = np.array(data['IP'], dtype=float).mean()
    SO_mean = np.array(data['SO'], dtype=float).mean()
    W_mean = np.array(data['W'], dtype=float).mean()
    ER_std = np.array(data['ER'], dtype=float).std()
    BB_std = np.array(data['BB'], dtype=float).std()
    IP_std = np.array(data['IP'], dtype=float).std()
    SO_std = np.array(data['SO'], dtype=float).std()
    W_std = np.array(data['W'], dtype=float).std()
    for i in range(0, batting_PLAYER.size):
        batting_values[data['PLAYER'][i]] = [10*(float(data['ER'][i])-ER_mean)/ER_std+50, 
                                             10*(float(data['BB'][i])-BB_mean)/BB_std+50,
                                             10*(float(data['IP'][i])-IP_mean)/IP_std+50,
                                             10*(float(data['SO'][i])/SO_mean)/SO_std+50,
                                             10*(float(data['W'][i])/W_mean)/W_std+50]

    if y is None:
        title = 'Individual Player Radar Chart: '
    else:
        title = 'Two Players Radar Chart: '
    # plot radar chart
    Radar_chart(categories, batting_values, title, playerName = x, otherPlayerName = y)
    
# Function: print the personal batters' performance - table and bar chart 
def one_batter_chart(p1):
    global data
    data = data.reset_index(drop = True).set_index('PLAYER')
    indicators = ['HR', 'RBI', 'BB', 'SB', 'H']
    players = data.loc[[p1]]
    player_1 = players.loc[p1][[8, 9, 10, 12, 5]].tolist()                        # pick the values
    player_1 = list(map(float, player_1))
    average_scores = [sum(np.array(data['HR'], dtype=float))/ len(data['HR']),    # calculate the average scores
                 sum(np.array(data['RBI'], dtype=float))/ len(data['RBI']), 
                 sum(np.array(data['BB'], dtype=float))/ len(data['BB']), 
                 sum(np.array(data['SB'], dtype=float))/ len(data['SB']),
                 sum(np.array(data['H'], dtype=float))/ len(data['H'])]
    x = np.arange(5)
    width = 0.3
    plt.bar(x, player_1, width, color='darkseagreen', label=p1)
    plt.plot(x, average_scores, color='chocolate', linewidth = 3, label='Average units')
    plt.xticks(x + width / 2, indicators)
    plt.ylabel('unit')
    plt.title("Batter's Data", 
          fontsize=32.5, 
          fontstyle='italic', 
          color='white',
          backgroundcolor='gray')
    plt.legend(loc='upper left')
    
    players = players.drop('Role',axis=1)
    display(players)
    plt.show()

# Function: print the personal pitchers performance - table and bar chart
def one_pitcher_chart(p1):
    global data
    data = data.reset_index(drop = True).set_index('PLAYER')
    indicators = ['ER', 'BB', 'IP', 'SO', 'W']
    players = data.loc[[p1]]
    player_1 = players.loc[p1][[8, 9, 6, 10, 11]].tolist()                        # pick the values
    player_1 = list(map(float, player_1))
    average_scores = [sum(np.array(data['ER'], dtype=float))/ len(data['ER']),    # calculate the average scores
             sum(np.array(data['BB'], dtype=float))/ len(data['BB']), 
             sum(np.array(data['IP'], dtype=float))/ len(data['IP']), 
             sum(np.array(data['SO'], dtype=float))/ len(data['SO']),
             sum(np.array(data['W'], dtype=float))/ len(data['W'])]
    x = np.arange(5)
    width = 0.3
    plt.bar(x, player_1, width, color='darkseagreen', label=p1)
    plt.plot(x, average_scores, color='chocolate', linewidth = 3, label='Average units')
    plt.xticks(x + width / 2, indicators)
    plt.ylabel('unit')
    plt.title("Pitcher's Data", 
          fontsize=32.5, 
          fontstyle='italic', 
          color='white',
          backgroundcolor='gray')
    plt.legend(loc='upper left')
    
    players = players.drop('Role',axis=1)
    display(players)
    plt.show()
    
# Function: comparing two batters' performance - table and bar chart
def two_batters_comparison(p1, p2):
    global data
    data = data.reset_index(drop = True).set_index('PLAYER')
    indicators = ['HR', 'RBI', 'BB', 'SB', 'H']
    players = data.loc[[p1, p2]]
    player_1 = players.loc[p1][[8, 9, 10, 12, 5]].tolist()                        # pick the values
    player_1 = list(map(float, player_1))
    player_2 = players.loc[p2][[8, 9, 10, 12, 5]].tolist()
    player_2 = list(map(float, player_2))
    average_scores = [sum(np.array(data['HR'], dtype=float))/ len(data['HR']),    # calculate the average scores
                 sum(np.array(data['RBI'], dtype=float))/ len(data['RBI']), 
                 sum(np.array(data['BB'], dtype=float))/ len(data['BB']), 
                 sum(np.array(data['SB'], dtype=float))/ len(data['SB']),
                 sum(np.array(data['H'], dtype=float))/ len(data['H'])]
    x = np.arange(5)
    width = 0.3
    plt.bar(x, player_1, width, color='darkseagreen', label=p1)
    plt.bar(x + width, player_2, width, color='lightsteelblue', label=p2)
    plt.plot(x, average_scores, color='chocolate', linewidth = 3, label='Average units')
    plt.xticks(x + width / 2, indicators)
    plt.ylabel('unit')
    plt.title('2 Batters Comparison', 
          fontsize=32.5, 
          fontstyle='italic', 
          color='white',
          backgroundcolor='gray')
    plt.legend(loc='upper left')
    
    players = players.drop('Role',axis=1)
    display(players)
    plt.show()

# Function: comparing two pitchers performance - table and bar chart
def two_pitchers_comparison(p1, p2):
    global data
    data = data.reset_index(drop = True).set_index('PLAYER')
    indicators = ['ER', 'BB', 'IP', 'SO', 'W']
    players = data.loc[[p1, p2]]
    player_1 = players.loc[p1][[8, 9, 6, 10, 11]].tolist()                        # pick the values
    player_1 = list(map(float, player_1))
    player_2 = players.loc[p2][[8, 9, 6, 10, 11]].tolist()
    player_2 = list(map(float, player_2))
    average_scores = [sum(np.array(data['ER'], dtype=float))/ len(data['ER']),    # calculate the average scores
             sum(np.array(data['BB'], dtype=float))/ len(data['BB']), 
             sum(np.array(data['IP'], dtype=float))/ len(data['IP']), 
             sum(np.array(data['SO'], dtype=float))/ len(data['SO']),
             sum(np.array(data['W'], dtype=float))/ len(data['W'])]
    x = np.arange(5)
    width = 0.3
    plt.bar(x, player_1, width, color='darkseagreen', label=p1)
    plt.bar(x + width, player_2, width, color='lightsteelblue', label=p2)
    plt.plot(x, average_scores, color='chocolate', linewidth = 3, label='Average units')
    plt.xticks(x + width / 2, indicators)
    plt.ylabel('unit')
    plt.title('2 Pitchers Comparison', 
          fontsize=32.5, 
          fontstyle='italic', 
          color='white',
          backgroundcolor='gray')
    plt.legend(loc='upper left')
    
    players = players.drop('Role',axis=1)
    display(players)
    plt.show()

input_1 = widgets.Dropdown(        # the Dropdowns for choosing the role
    options=['batting', 'pitching'],
    value='batting',
    description='Role',
    disabled=False,
)

input_2 = widgets.Dropdown(        # the Dropdowns for choosing personal data or comparing data
    options=['comparison data', 'personal data'],
    value='comparison data',
    description='Which?',
    disabled=False,
)

input_3 = widgets.Dropdown(        # the Dropdowns for choosing description data or charts
    options=['description', 'charts'],
    value='description',
    description='Data type',
    disabled=False,
)

# ste_1 to step_6 use for the flow control, it will be True after the particular step is done
step_1 = False
step_2 = False
step_3 = False
step_4 = False
step_5 = False
step_6 = False

# function for making choosed player's Dropdowns
def find_players(x):                   
    players_data = data[data['Role'] == x]['PLAYER']
    players = list(players_data)
    input_players = widgets.Dropdown(
    options= players,
    value= players[0],
    description='Player',
    disabled=False,
    )
    return input_players

# function for making compared player's Dropdowns
def compare_player(x):              
    global y
    y = list(data[data['PLAYER'] != x]['PLAYER'])
    input_other_players = widgets.Dropdown(
    options= y,
    value= y[0],
    description='With whom?',
    disabled=False,
    )
    return input_other_players

# determine the desired role of user, batters or pitchers
def which_role():    
    with out:
        display(input_1, button)
    global step_1
    step_1 = True

# global the batters' or pitchers' dataframe, it's based on the user's choice
def data_out():
    global data
    x = input_1.value
    if x == input_1.options[0]:
        data = final_df_1
    else:
        data = final_df_2

# making the players' Dropdowns based on the choice of user
def player_list():
    data_out()
    global input_players
    players_data = data['PLAYER']
    players = list(players_data)
    input_players = widgets.Dropdown(
    options= players,
    value= players[0],
    description='Player',
    disabled=False,
    )
    global step_2
    step_2 = True
        
    with out:
        display(input_players, button)

# determine whether the personal or comparing
def which_type():
    global step_3
    step_3 = True
    with out:
        display(input_2, button)

# determine which data type is the user wanted, personal or comparing
# based on the user's choice, the function will go into different step
def which_compare():    
    if input_2.value == input_2.options[0]:
        global step_4
        step_4 = True
        global input_other_players
        input_other_players = compare_player(input_players.value)
        with out:
            display(input_other_players, button)
    else:
        global step_6
        step_6 = True
        with out:
            display(input_3, button)

# ask the desired draw type
def compare_draw_type():
    global step_5
    step_5 = True
    with out:
            display(input_3, button)

# function to draw the comparing data with the particular event
def compare_draw():
    x, y = input_players.value, input_other_players.value
    if (data['Role'][0] == 'batting') and (input_3.value == input_3.options[0]):
        with out:
            two_batters_comparison(x, y)
    elif (data['Role'][0] == 'batting') and (input_3.value == input_3.options[1]):
        with out:
            do_batting_chart(x, y)
    elif (data['Role'][0] == 'pitching') and (input_3.value == input_3.options[0]):
        with out:
            two_pitchers_comparison(x, y)
    else:
        with out:
            do_pitching_chart(x, y)

# function to draw the personal data with the particular event
def draw_personal():
    x = input_players.value
    if (data['Role'][0] == 'batting') and (input_3.value == input_3.options[0]):
        with out:
            one_batter_chart(x)
    elif (data['Role'][0] == 'batting') and (input_3.value == input_3.options[1]):
        with out:
            do_batting_chart(x)
    elif (data['Role'][0] == 'pitching') and (input_3.value == input_3.options[0]):
        with out:
            one_pitcher_chart(x)
    else:
        with out:
            do_pitching_chart(x)

# the occurrence of event when click the button
# it contains the different actions when the particular event has been triggered
def on_button_clicked(b):
    out.clear_output()
    if step_6 == True:
        draw_personal()
        
    elif step_5 == True:
        compare_draw()
        
    elif step_4 == True:
        compare_draw_type()
        
    elif step_3 == True:
        which_compare()
        
    elif step_2 == True:
        which_type()
        
    elif step_1 == True:
        player_list()

# making the object for jupyter notebook
out = widgets.Output()
button = widgets.Button(description='Comfirm',)
button.on_click(on_button_clicked)

# main executing function
def main():
    which_role()
    
    return out

main()
#
