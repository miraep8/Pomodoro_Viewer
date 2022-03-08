import pandas as pd
from bokeh.plotting import figure
from bokeh.io import save, output_file, show
from bokeh.models import FixedTicker, ColorBar, LinearColorMapper, BasicTicker, HoverTool
from bokeh.palettes import Viridis256
import numpy as np
import datetime
import sys
from make_dataframes import *


def make_cal_heatmap(date_df):
    '''
    make_cal_heatmap will take a date_df which is a dataframe containing the
    processed time stamps of all your pomodoros. It will return the filenames
    of all the html heatmap calendar files created.  (will create a seperate
    html file for each year of data.)
    '''
    unique_days = date_df[['Year', 'Month', 'Day', 'Day_Date_Rep', 'Weekday', 'Week_Num']]
    unique_days = unique_days.value_counts().to_frame('Num_Pomos').reset_index()
    colors = Viridis256
    weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    month_nums = ['1','2','3','4','5','6','7','8','9','10','11','12']
    months = []
    for m_num in month_nums:
        datetime_object = datetime.datetime.strptime(m_num, "%m")
        months.append(datetime_object.strftime("%b"))
    cal_file_names = []
    for uniq_year in unique_days.Year.unique():
        this_year_df = unique_days[:][unique_days['Year'] == uniq_year]
        c_map = LinearColorMapper(palette = colors, low = 0, high = max(this_year_df.Num_Pomos))
        max_num_weeks = max(datetime.date(int(uniq_year), 12, 31).isocalendar()[1], 52)
        month_locs = []
        tick_dict = dict()
        tooltips = [
            ('Number of Pomos', '@Num_Pomos'),
            ('Date', '@Day_Date_Rep')
           ]
        for ind, i in enumerate(list(range(1,13))):
            mid_month = datetime.date(int(uniq_year), i, 15)
            month_locs.append(int(mid_month.isocalendar()[1]))
            tick_dict[month_locs[-1]] = months[ind]
        p = figure(title = f'Number of Pomodoros per Day in {uniq_year}',
                x_range = (-1,max_num_weeks+1),
                y_range = list(reversed(weekdays)),
                width = 2080,
                height = 315)
        p.add_tools(HoverTool(tooltips = tooltips))
        p.title.text_font_size = '20pt'
        p.title.align = 'center'
        p.xaxis.ticker = FixedTicker(ticks = list(month_locs))
        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.major_label_text_font_size = "15px"
        p.axis.major_label_standoff = 0
        p.xaxis.major_label_overrides = tick_dict
        p.rect(x = "Week_Num", y = "Weekday", width = .8, height = .8,
                source = this_year_df, fill_color = {'field': 'Num_Pomos', 'transform': c_map},
                line_color = None)

        color_bar = ColorBar(color_mapper = c_map, major_label_text_font_size="12px",
                     ticker = BasicTicker(desired_num_ticks = 8),
                     label_standoff=6, border_line_color=None)
        p.add_layout(color_bar, 'right')

        output_file(f'{uniq_year}_pomo_cal.html', title = f'Num Pomos Calendar for {uniq_year}')
        cal_file_names.append(f'{uniq_year}_pomo_cal.html')
        save(p)
    return cal_file_names

#def make_weekly_counter(date_df, goals_df):
#    '''
#    make_weekly_counter will takes both goal_df and date_df.  date_df is a
#    dataframe containing all the processed time stamps of all your pomodoros.
#    goal_df is a dataframe with all the weekly goals you have set for yourself
#    in terms of number of pomodoros per week (it can be configured to take into
#    account days off as well!).  It will then return a html file comparing how
#    many pomodoros you have done per week versus your goal.
#    '''
#    unique_weeks = date_df[['Year', 'Week_Num']]
#    unique_weeks = unique_weeks.value_counts().to_frame('Num_Pomos').reset_index()
#    colors = Viridis256
#    for week in unique_weeks.iterrows
