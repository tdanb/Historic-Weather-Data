import urllib.request
import urllib.parse
import panadas as pd
from datetime import datetime
import json
import os


# unnesting json for each month
def extract_monthly_data(data, data_specifics):

    # store return data
    df_month = pd.DataFrame()

    for i in range(len(data)):

        # extract this day
        d = data[i]
        # astronomy data is the same for the whole day
        astr_df = pd.DataFrame(d['astronomy'])
        # hourly data; temperature for each hour of the day
        hourly_df = pd.DataFrame(d['hourly'])
        # this wanted_key will be duplicated and use 'ffill' to fill up the NAs
        wanted_keys = ['date', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour', 'uvIndex']  # The keys you want
        subset_d = dict((k, d[k]) for k in wanted_keys if k in d)
        this_df = pd.DataFrame(subset_d, index=[0])
        df = pd.concat([this_df.reset_index(drop=True), astr_df], axis=1)
        # concat selected astonomy columns with hourly data
        df = pd.concat([df, hourly_df], axis=1)
        df = df.fillna(method='ffill')
        # make date_time columm to proper format
        # fill leading zero for hours to 4 digits (0000-2400 hr)
        df['time'] = df['time'].apply(lambda x: x.zfill(4))
        # keep only first 2 digit (00-24 hr) 
        df['time'] = df['time'].str[:2]
        # convert to pandas datetime
        df['date_time'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        
        # keep only interested columns
        df = df[data_specifics]
        df = df.loc[:,~df.columns.duplicated()]
        df_month = pd.concat([df_month, df])
    return (df_month)



# Retrieving the historic weather data per month for each location
def historic_weather_data(begin_month_dates, ending_month_dates, api_key, location, frequency, data_specifics, response_cache_path = None):
    start_d = str(begin_month_dates[i])[:10]
    end_d = str(ending_month_dates[i])[:10]
    file_path = f'{response_cache_path}/{location}_{start_d}_{end_d}'
    if (response_cache_path and os.path.exists(file_path)):
        print('\n\nReading cached data for ' + location + ': from ' + start_d + ' to ' + end_d)
        with open(f'{response_cache_path}/{location}_{start_d}_{end_d}', 'r') as f:
            json_data = json.load(f)
    else:
        print('\n\nCurrently retrieving data for ' + location + ': from ' + start_d + ' to ' + end_d)
        url_page = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=' + api_key + '&q=' + location + '&format=json&date=' + start_d + '&enddate=' + end_d + '&tp=' + str(
            frequency)
        json_page = urllib.request.urlopen(url_page, timeout=10)
        json_data = json.loads(json_page.read().decode())

    if response_cache_path:
        with open(f'{response_cache_path}/{location}_{start_d}_{end_d}', 'w') as f:
            json.dump(json_data, f)


    data = json_data['data']['weather']

    # call function to extract json object
    df_this_month = extract_monthly_data(data, data_specifics)
    df_this_month['location'] = location

    return df_this_month




# Retreive data by range and location
def retrieve_this_location(api_key, location_list, start_date, end_date, frequency, data_specifics, response_cache_path = None):
    
    start_time = datetime.now()
    print('\n\n{} Beginning ' + location + ' data retrieval'.format(start_time))

    # create list of first day of month for range between start date and converting to series
    begin_month_dates = pd.date_range(start_date, end_date, freq='MS', closed='right').concat([pd.Series(pd.to_datetime(start_date)), pd.Series(list_mon_begin)], ignore_index=True)

    # create list of month end dates for range between end dates and converting to series
    ending_month_dates = pd.date_range(start_date, end_date, freq='M', closed='left').concat([pd.Series(list_mon_end), pd.Series(pd.to_datetime(end_date))], ignore_index=True)

    # Storing return data
    df_weather = pd.DataFrame()

    # Retrieving historic weather data
    for i in range(len(begin_month_dates)):
        df_weather = pd.concat([df_weather, historic_weather_data(begin_month_dates, ending_month_dates, api_key, location, frequency,data_specifics, response_cache_path)])

        time_elapsed = datetime.now() - start_time
        print('\n\nFinished Data Retrival for a month Time elap (hh:mm:ss.ms) {}'.format(time_elapsed))
        
    return (df_weather)



# Retrieving the data for each inputted location
def retrieve_hist_data(api_key, location_list, start_date, end_date, frequency, data_specifics, response_cache_path = None):

    # Retrieving history data for each location
    for location in location_list:

        print('\n\nRetrieving weather data for ' + location + '\n\n')
        df_country = retrieve_this_location(api_key, location_list, start_date, end_date, frequency,data_specifics)

        print('\n\n' + location + ' weather data retrieved\n\n')
        df_country.to_csv('./' + location + '.csv', header=True, index=False)
        print('\n\nExporting ' + location + ' csv completed!\n\n')

