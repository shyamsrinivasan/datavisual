import os.path
import pandas as pd


def df_from_file(file_name, sep='\t'):
    """get data in file as dataframe"""
    data = pd.read_csv(file_name, sep=sep, header=0)
    # parse df (remove NaN and drop repeated rows
    column_names = data.columns.values.tolist()
    fltr_data = data[data[column_names[0]] != column_names[0]]  # remove rows with data similar to column headers
    fltr_data = fltr_data.dropna()  # get only valid data (NaN and other strings removed)
    return fltr_data


def combine_time(full_time):
    """combine time columns to get full time"""
    full_time = pd.to_datetime(full_time, errors='coerce')
    time_only = pd.Series([val.time() if not pd.isnull(val) else pd.NaT for val in full_time])
    return time_only


def get_time_stamp(data):
    """combine Hour Minute & Second columns to form single time column"""
    column_names = data.columns.values.tolist()
    if 'Hour ' in column_names and 'Minute ' in column_names and 'Second ' in column_names:
        time_meas = data['Hour '] + ':' + data['Minute '] + ':' + data['Second ']
    elif 'Hour' in column_names and 'Minute' in column_names and 'Second' in column_names:
        time_meas = data['Hour'] + ':' + data['Minute'] + ':' + data['Second']
    else:
        print('Time column names error')

    time_only = combine_time(time_meas)

    if 'Year ' in column_names and 'Month ' in column_names and 'Date ' in column_names:
        date = pd.concat({'Year': data['Year '],
                          'Month': data['Month '],
                          'Day': data['Date ']}, axis=1)
    elif 'Year' in column_names and 'Month' in column_names and 'Date' in column_names:
        date = pd.concat({'Year': data['Year'],
                          'Month': data['Month'],
                          'Day': data['Date']}, axis=1)
    else:
        print('Time column names error')

    date = pd.to_datetime(date)
    date = date.reset_index()
    date = date.rename(columns={0: 'Date'})
    time_stamp = pd.concat({'time index': date['index'],
                            'Date': date['Date'],
                            'Time': time_only}, axis=1)
    return time_stamp


def get_temp_humid(data,time_stamp):
    """get temperature humidity data with time stamps"""
    reid_df = data.reset_index()
    reid_df = reid_df[['index', 'Temperature ', 'Humidity ', 'Heat Index']]
    reid_df = reid_df.rename(columns={'Temperature ': 'Temperature', 'Humidity ': 'Humidity'})
    reid_df[['Temperature', 'Humidity', 'Heat Index']].astype('float64')
    df = pd.concat([time_stamp, reid_df], axis=1)
    df = df[df['time index'] == df['index']][['Date', 'Time', 'Temperature', 'Humidity', 'Heat Index']]
    return df


if __name__ == '__main__':
    # os.chdir("C:\\Users\\Shyam\\Documents\\datavisual")
    data_file = os.path.join(os.getcwd(), 'data\\temperature.txt')
    dframe = df_from_file(data_file)  # get data in file as dataframe
    time_data = get_time_stamp(dframe)

    full_data = get_temp_humid(dframe, time_data)  # get temperature humidity data with time stamps

    # get time series visuals
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


