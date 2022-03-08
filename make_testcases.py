from os import mkdir, path
import datetime

numdays = 1000
today = datetime.datetime.today()
date_list = [today - datetime.timedelta(days = i) for i in range(numdays)]

dir_name = f'./last_{numdays}_days/'
if not path.exists(dir_name):
    mkdir(dir_name)
file_name = dir_name + today.strftime("%Y_%m_%d") + '.txt'
with open(file_name, 'w+') as f:
    for d in date_list:
        f.write(''.join([str(d), '\n']))
