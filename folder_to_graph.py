import pandas as pd
from make_figures import *
from make_dataframes import *


def make_figs(folder):

    date_df = make_date_df(folder)
    cal_fig_files = make_cal_heatmap(date_df)

    return cal_fig_files,2,3


if __name__ == '__main__':
    folder = sys.argv[1]
    cal_fig, hour_fig, sig_fig = make_figs(folder)
