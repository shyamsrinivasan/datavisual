import os.path
import pandas as pd
import datetime
from frameromdata import df_from_file, get_time_stamp, get_temp_humid
from plotdata import scatterplot


def time_dependent_data(data, timeofday=''):
    """get day time data only: day time 0601 - 1800, night time 1801 - 0600"""

    t1 = datetime.time(6, 0, 0)
    t2 = datetime.time(18, 0, 0)
    # t3 = datetime.time(18, 0, 1)
    # t4 = datetime.time(6, 0, 0)
    if timeofday == 'day':
        time_points = [True if t1 < stamp.time() < t2 else False for stamp in data['Time']]
    elif timeofday == 'night':
        time_points = [True if stamp.time() > t2 or stamp.time() < t1 else False for stamp in data['Time']]
    else:
        time_points = [True for _ in data['Time']]

    dn_data = [full_data[['Time', 'Temperature', 'Humidity', 'Heat Index']].iloc[indx]
               for indx, bl_ind in enumerate(time_points) if bl_ind]
    dn_data = pd.DataFrame(dn_data)
    dn_data = dn_data.reset_index(drop=True)
    return dn_data


if __name__ == '__main__':
    """collect data from file"""
    # os.chdir("C:\\Users\\Shyam\\Documents\\datavisual")
    data_file = os.path.join(os.getcwd(), 'data\\temperature.txt')
    dframe = df_from_file(data_file)  # get data in file as dataframe
    time_data = get_time_stamp(dframe)
    full_data = get_temp_humid(dframe, time_data)  # get temperature humidity data with time stamps

    day_data = time_dependent_data(full_data, timeofday='day')  # day time data (after sunrise and before sunset)
    night_data = time_dependent_data(full_data, timeofday='night')  # night time data (after sunset or before sunrise)

    # get monthly data for each year (mean with min and max) box plots

    # get time series visuals
    scatterplot(day_data, 'Temperature')

    # function to plot complete time visuals
    # function to plot day time only data
    # function to plot night time only data (for both temp and humidity)

    print('Complete')


# separate day and night time data
# separate seasonal data
# get box plot visuals (distribution of temperature w/ mean)

# visualize temperature
# visualize humidity
# visualize heat index


