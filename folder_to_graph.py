import pandas as pd
from bokeh.plotting import figure
from bokeh.io import save, output_file, show
from bokeh.models import FixedTicker, ColorBar, LinearColorMapper, BasicTicker, HoverTool
from bokeh.palettes import Viridis256
import numpy as np
import datetime
import sys
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
    date_df['Week_Num'] = date_df['Timestamp'].dt.strftime('%U').astype(int)
    return date_df


def make_cal_heatmap(date_df):
    unique_days = date_df[['Year', 'Month', 'Day', 'Weekday', 'Week_Num']]
    unique_days = unique_days.value_counts().to_frame('Num_Pomos').reset_index()
    colors = Viridis256
    c_map = LinearColorMapper(palette = colors, low = 0, high = max(unique_days.Num_Pomos))
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cal_file_names = []
    for y in unique_days.Year.unique():
        this_year_df = unique_days[:][unique_days['Year'] == y]
        max_num_weeks = datetime.date(int(y), 12, 31).isocalendar()[1]
        month_locs = []
        tick_dict = dict()
        tooltips = [
            ('Number of Pomos', '@Num_Pomos')
           ]
        for ind, i in enumerate(list(range(1,13))):
            mid_month = datetime.date(int(y), i, 15)
            month_locs.append(int(mid_month.isocalendar()[1]))
            tick_dict[month_locs[-1]] = months[ind]
        p = figure(title = f'Number of Pomodoros per Day in {y}',
                x_range = (0,max_num_weeks),
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

        output_file(f'{y}_pomo_cal.html', title = 'Num Pomos Calendar')
        cal_file_names.append(f'{y}_pomo_cal.html')
        save(p)


def make_figs(folder):

    date_df = make_date_df(folder)
    cal_fig_files = make_cal_heatmap(date_df)

    return cal_fig_files,2,3


if __name__ == '__main__':
    folder = sys.argv[1]
    cal_fig, hour_fig, sig_fig = make_figs(folder)
