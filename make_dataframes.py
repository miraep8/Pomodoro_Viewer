import pandas as pd
import numpy as np
import datetime
from pathlib import Path


def make_date_df(folder):

    date_dfs = []
    file_string_pattern = '[1-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9]*'
    for file in Path(folder).glob(file_string_pattern):
        new_df = pd.read_csv(str(file), names = ['Timestamp'], parse_dates = ['Timestamp'])
        date_dfs.append(new_df)
    date_df = pd.concat(date_dfs, ignore_index = True)
    #Now we will parse some of the specific datetime info into new columns:
    date_df['Weekday'] = date_df['Timestamp'].dt.strftime('%a')
    date_df['Month'] = date_df['Timestamp'].dt.strftime('%b')
    date_df['Day'] = date_df['Timestamp'].dt.strftime('%d')
    date_df['Year'] = date_df['Timestamp'].dt.strftime('%Y')
    date_df['Hour'] = date_df['Timestamp'].dt.strftime('%H')
    date_df['Day_Date_Rep'] = date_df['Timestamp'].dt.strftime('%x')
    date_df['Week_Num'] = date_df['Timestamp'].dt.strftime('%U').astype(int)

    return date_df


def get_days_off(folder, holiday_str = '*holiday*'):

    files = []
    days_off = []
    for file in Path(folder).glob(holiday_str):
        files.append(str(file))
    if len(files) > 1:
        print('There was an error in reading your holiday file. \n There should be \
              only be one holiday file in your pomodoro folder. \n The program will\
              default to assuming no time off. \n Please check out test_folder on \
              the github for proper formatting ')
    if len(files) == 1:
        with open(files[0]) as f:
            for l in f.readlines():
                days_off.append(datetime.strptime(l, '%d/%m/%y'))

    return days_off

def get_goals(folder, default, goals_str =  '*goals*'):

    files = []
    start = min(data_df['Timestamp']).dt.strftime('%x')
    for file in Path(folder).glob(goal_str):
        files.append(str(file))
    empty_data = {'Start_Date':[start], 'Pomos_per_Week':[default]}
    if len(files) > 1:
        goals_df = pd.DateFrame(data = empty_data)
        print(f'There was an error in reading your goals file. \n There should be \
              only be one goals file in your pomodoro folder. \n The program will\
              default to assuming a weekly goal of {default} Pomodoros. \n \
              Please check out test_folder on the github for proper formatting ')
    if len(files) < 1:
        goals_df = pd.DateFrame(data = empty_data)
        print(f'Since you have not specified a goals file, the program will assume \
              a weekly goal of {default} Pomodoros per week. \n  To change this or \
              add a goal check out the example goals file in test_folder ')
    if len(files) == 1:
        goals_df = pd.read_csv(files[0], header = None,
                                names = ['Start_Date', 'Pomos_per_Week'],
                                parse_date = ['Start_Date'])
        goals_df.sort_values(['Start_Date'])
        goals_df['Year'] = goals_df['Start_Date'].dt.strftime('%Y')
        goals_df['Week_Num'] = goals_df['Start_Date'].dt.strftime('%U').astype(int)
        goals_df['Day_Date_Rep'] = goals_df['Start_Date'].dt.strftime('%x')

    return goals_df


def make_goal_df(folder, date_df, default = 40):

    days_off = get_days_off(folder)
    ordered_goals = get_goals(folder, default)
    unique_weeks = date_df[['Year','Week_Num']]
    unique_weeks = unique_weeks.value_counts().to_frame('Num_Pomos').reset_index()
