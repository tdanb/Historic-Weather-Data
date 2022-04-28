from getData import retrieve_hist_data
import os
import datetime

def time_range():
    s_date = input('Input the start date (ex. 01-JAN-2009): ')
    e_date = input('Input the end date (ex. 01-JAN-2009): ')

    if(int(e_date[7:]) > 2022):
        e_date = e_date[:7] + '2022'

    return s_date, e_date

def location():
    
    num_countries = int(input('How many countries? '))
    country_list = [' '] * num_countries
    i = 0

    while (i < num_countries):
        country_list[i] = input('Input the name of a country:')
        i += 1

    return country_list


def information():
    print ('| Option 1 | Option 2 | Option 3   | Option 4    |')
    print ('_________________________________________________')
    print ('| date/time| date/time| date/time  | date/time   |')
    print ('| maxtempC |  sunHour |totalSnow_cm| WindChillC  |')
    print ('| mintempC |  uvIndex |  DewPointC |WindGustKmph |')
    print ('|FeelsLikeC|  sunrise |  humidity  |winddirDegree|')
    print ('|   tempC  |  sunset  | visibility |  precipMM   |')
    print ('|HeatIndexC|  moonrise| cloudcover |windspeedKmph|')
    print ('| mintempC |  moonset |  pressure  |')

    options = int(input('How many options would you like to choose? '))
    cols = ['date_time']

    for i in range(options):
        choice = int(input('Input Option #: '))

        if (choice == 1):
            cols = cols.append(['maxtempC','mintempC','FeelsLikeC','tempC','HeatIndexC','mintempC'])
        elif (choice == 2):
            cols = cols.append(['sunHour','uvIndex','sunrise','sunset','moonrise','moonset'])
        elif (choice == 3):
            cols = cols.append(['totalSnow_cm','DewPointC','humidity','visibility','cloudcover','pressure'])
        elif (choice == 4):
            cols = cols.append(['WindChillC','WindGustKmph','winddirDegree','precipMM','windspeedKmph'])
        else:
            print('Please only input 1,2,3,4. Thanks!')
    
    return cols





# setting working directory for the outputted csv
os.chdir("./Output Data")

# constants
api_key = 'bffc83d8ee6f424f85335044221703'
frequency = 24

# input values 
start_date, end_date = time_range()
location_list = location()
data_specifics = information()

hist_weather_data = retrieve_hist_data(api_key,
                                        location_list,
                                        start_date,
                                        end_date,
                                        frequency,
                                        data_specifics
                                        )

