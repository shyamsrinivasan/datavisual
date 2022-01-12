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


def get_monthly_data(data, nmonths=12):
    """get monthly data for each year (mean with min and max) box plots"""

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    ndata = len(full_data)
    parsed_data = [[data[['Time', 'Temperature', 'Humidity', 'Heat Index']].iloc[indx] for indx in range(0, ndata) if data['Time'].iloc[indx].month == imnth]
                   for imnth in range(1, 13)]
    parsed_df = [pd.DataFrame(idata) if idata else pd.DataFrame([]) for idata in parsed_data]
    if 0 <= nmonths <= 11:     # get only nth month data
        monthly_data = {months[imonth]: idata.reset_index(drop=True) for imonth, idata in enumerate(parsed_df)
                        if imonth == nmonths and not idata.empty}
    else:               # get monthly data for all months/years (for which data is available)
        monthly_data = {months[imonth]: idata.reset_index(drop=True)
                        for imonth, idata in enumerate(parsed_df) if not idata.empty}

    # get data stats for each month
    # stats = {imonth: [] for (imonth, idata) in monthly_data.items()}
    #     min_temp = idata
    return monthly_data


def combinedatafiles(datafiles, newfile=''):
    """Combine two or more data files into single file"""
    fin = False

    for file in datafiles:
        with open(file, 'r') as f:
            if newfile:
                with open(newfile, 'a') as nf:
                    for line in f:
                        nf.write(line)
                    nf.close()
            else:
                newfile = os.path.join(os.getcwd(), 'data\\combined_data.txt')
                with open(newfile, 'a') as nf:
                    for line in f:
                        nf.write(line)
                    nf.close()
            f.close()
            fin = True

    return fin


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
    monthly_data = get_monthly_data(full_data)

    # file operations test
    all_datafiles = [os.path.join(os.getcwd(), 'data\\Apr21_Jun10_2021.txt'),
                     os.path.join(os.getcwd(), 'data\\Jun10_Dec20_2021.txt')]
    flag = combinedatafiles(all_datafiles, os.path.join(os.getcwd(), 'data\\combined_data.txt'))

    # get time series visuals
    scatterplot(day_data, dtype='all', sep=True)

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


