import os
from pandas import *
import datetime


# Find the file that begins with FCST, and return the location
def get_fcst_path(working_directory):
    fcst_locations = []
    tomorrow_files = []
    today_files = []
    today_date = datetime.datetime.today().date()
    tomorrow_date = (datetime.datetime.today() + datetime.timedelta(days=1)).date()
    # date_format = '%Y-%m-%d %H:%M:%S'

    # Loop through each file in directory, return list of lists: [[FCST_07July2021.xlsx, 07-07-2021, 07-07-2021 08:00]]
    for file in os.listdir(working_directory):
        if os.path.isfile(os.path.join(working_directory, file)) and 'FCST' in file:
            fcst_location = working_directory + "\\" + file
            fcst_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(fcst_location))
            fcst_date = get_fcst_date_from_filename(file)
            fcst_locations.append([fcst_location, fcst_date, fcst_timestamp])

    # Search for FCST file for the next day, and populate a list with these files
    for fcst_file in fcst_locations:
        if fcst_file[1] == tomorrow_date:
            # print("I found tomorrow's file! \n", fcst_file, '\n')
            tomorrow_files.append(fcst_file)

        if fcst_file[1] == today_date:
            # print('\nNow I found todays file!\n', fcst_file)
            today_files.append(fcst_file)

    latest_nextday_fcst = get_latest_file(tomorrow_files)
    latest_current_day_fcst = get_latest_file(today_files)
    latest_fcst_overall = get_latest_file(fcst_locations)

    # If there is at least one file for tomorrow, get the latest one, and then the latest file for today as well
    if len(tomorrow_files) > 0:
        return [latest_nextday_fcst, latest_current_day_fcst]

    # If there are no files for tomorrow, but at least one for today, return the latest for today
    elif len(today_files) > 0:
        return [latest_current_day_fcst]

    # If there are no FCST files for today nor tomorrow, print message, then use latest file
    else:
        print('Could not find FCST file for today nor tomorrow.  Proceeded to use latest FCST that I found: ',
              latest_fcst_overall)

        return latest_fcst_overall


# Get the most recent file from a list of lists: [FCST_12July2021.xlsx,, 07-12-2021, 07-11-2021 13:34:20 (timestamp)]
def get_latest_file(files):
    max_timestamp = datetime.datetime(1990, 1, 1)

    try:
        latest_file = files[0][0]
    except IndexError:
        return 0

    for file in files:
        if file[2] > max_timestamp:
            max_timestamp = file[2]
            latest_file = file[0]

    return latest_file


# Parse the filename of FCST file, and return the date of fcst.  Ex: FCST_11July2021 returns 2021-07-11
def get_fcst_date_from_filename(fcst_filename):
    filename_format = 'FCST_%d%B%Y'
    parsed_file = fcst_filename[:-5]

    try:
        file_date = datetime.datetime.strptime(parsed_file, filename_format).date()

    except ValueError as v:
        if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
            parsed_file = parsed_file[:-(len(v.args[0]) - 26)]
            file_date = datetime.datetime.strptime(parsed_file, filename_format).date()

        else:
            raise

    return file_date


# Read FCST file into Pandas, & create a dataframe with the future gen tab
def get_df_from_excel(fcst_location, tab_name):
    fcst_df = pandas.ExcelFile(fcst_location)
    output_df = pandas.read_excel(fcst_df, tab_name, skiprows=3)

    return output_df


# Go through each row in file and populate a list of dictionaries for each row, with the date ranked from today.
def populate_row_dict(input_df):
    row_list = []

    try:
        for row_num, row in input_df.iterrows():
            row_dict = row.to_dict()
            row_list.append(row_dict)
    except AttributeError:
        pass

    return row_list


# Return a list of unique days in fcst file, ranked from 0-6. Also return the max date
def rank_days(row_list, days):
    date_format = '%m/%d/%Y'
    min_date = datetime.datetime(3000, 1, 1).date()
    max_date = datetime.datetime(1990, 1, 1).date()
    ranked_days = []
    unique_ranked_days = []

    # Get min and max dates in fcst file
    for row in row_list:
        if isinstance(row['Date'], str):
            try:
                date = datetime.datetime.strptime(str(row['Date']), date_format).date()

                if date < min_date:
                    min_date = date

                if date > max_date:
                    max_date = date

            except ValueError:
                continue

    # Go through each row in the list of rows, and replace the date with a list containing date and rank [06/23/2021, 1]
    for row in row_list:

        # Make sure value is of type String (the other non-date values in this column read in as NaN)
        if isinstance(row['Date'], str):

            # Save the date that is in current row
            date_string = row['Date']

            # Make sure that the date is in format MM/DD/YYYY
            try:
                date = datetime.datetime.strptime(str(row['Date']), date_format).date()
                day_rank = (date - min_date).days + days

            except ValueError:
                continue

            # Update the list of rows
            row['Date'] = [date_string, day_rank]
            ranked_days.append(([date_string, day_rank]))

            # Populate a list with unique days in FCST file, ranked from 1-6
            for day in ranked_days:
                if day not in unique_ranked_days:
                    unique_ranked_days.append([date_string, day_rank])

    return unique_ranked_days, max_date


# Return a list of rows from current day FCST.
def fetch_previous_day(row_list, second_half_current_day_rows):
    day_zero_rows = []

    for row in row_list:
        try:
            if row['Date'][1] == 0:
                day_zero_rows.append(row)
        except TypeError:
            continue

# Update day zero rows with second half of previous day data
    for row in day_zero_rows:
        for unit in second_half_current_day_rows:
            if row['Unit'] == unit['Resource']:
                for hour in range(13, 25):
                    index = str(hour)
                    row[index] = unit[index]

    return day_zero_rows


# If we don't have 6 days worth of data, copy the last day that we have into the rest of the days, until we have 6.
def ensure_six_days(fcst_rows, ranked_days, max_day):
    additional_rows = []
    additional_days = []
    max_day_string = max_day.strftime('%m/%d/%Y')

    for i in range(7):
        try:
            ranked_days[i]

        # If a day doesn't exist in forecast file, create a list with the remaining days required to complete 6
        except IndexError:
            day = datetime.datetime.strptime(str(ranked_days[i-1][0]), '%m/%d/%Y').date() + datetime.timedelta(days=1)
            new_day = day.strftime('%m/%d/%Y')
            new_day_rank = ranked_days[i-1][1] + 1
            ranked_days.append([new_day, new_day_rank])
            additional_days.append([new_day, new_day_rank])

    # For each additional day required, go thru existing fcst days, and copy the max day for each unit for each day
    for day in additional_days:
        for row in fcst_rows:
            try:
                if row['Date'][0] == max_day_string:
                    row_dict = dict(row)
                    row_dict['Date'] = [day[0], day[1]]
                    additional_rows.append(row_dict)

            except TypeError:
                continue

    # Add the newly copied additional days to the final list
    for row in additional_rows:
        print(row)
        fcst_rows.append(row)

    return fcst_rows


# Ex Output:
# [{'Date':['06/23/2021, 1], 'Unit':'STN-1', '1':'145', '2':'157', '3':'160'...}, {'Date':['06/24/2021, 2], 'Unit'...]
def get_row_dicts(current_day, next_day, second_half_current_day):
    row_list = []
    # fcst_file_num = len(future_gen_tabs)

    current_day_rows = populate_row_dict(current_day)
    current_day_ranks, current_day_max_day = rank_days(current_day_rows, 0)
    second_half_current_day_rows = populate_row_dict(second_half_current_day)
    # for tab in second_half_current_day_rows:
    #     print(tab)

    # If both the next day and current day fcst files exist, populate appropriate lists
    if current_day is not None and next_day is not None:
        # List of dicts for next-day file
        next_day_rows = populate_row_dict(next_day)

        # Unique dates and ranks for next-day file, as well as max date
        next_day_ranks, next_day_max_day = rank_days(next_day_rows, 1)

        # Today's data from yesterday's file (including updating 2nd half of today with today's file)
        day_zero_rows = fetch_previous_day(current_day_rows, second_half_current_day_rows)

        # Update final list with next-day and day-zero values
        for row in next_day_rows:
            row_list.append(row)

        for row in day_zero_rows:
            row_list.append(row)

        # Populate list with dates ranks
        next_day_ranks.append(current_day_ranks[0])

        return row_list, next_day_ranks, next_day_max_day

    # If only today's file exists, and not tomorrow's only use today's data
    elif current_day is not None and next_day is None:
        for row in current_day_rows:
            row_list.append(row)

        return row_list, current_day_ranks, current_day_max_day


# Takes a CSV File and returns a list of dictionaries for each row:
# [{'FirstColumnName': 'FirstRowValue', {'SecondColumnName': 'SecondRowValue'}........]
def csv_to_dict_list(csv_path):
    csv_file = pandas.read_csv(csv_path)
    csv_rows = []

    for row_num, row in csv_file.iterrows():
        row_dict = row.to_dict()
        csv_rows.append(row_dict)

    return csv_rows


# Check if the day (day 0 - day 6) match in the FEM FCST File and the Template File
def check_date_match(fem_row, template_row, ranked_days):
    dates_match = 0
    # print(ranked_days)

    for day in ranked_days:
        try:
            if template_row['Date'] == day[0] and fem_row['Date'][1] == day[1]:
                dates_match = 1
            # if template_row['Date'] == fem_row['Date'][1]:
            #     dates_match = 1

        except TypeError:
            pass

    return dates_match


# Check if the unit in the FCST file and Template file match, per translation table file
def check_unit_match(fem_unit, template_unit, translation_table):
    unit_match = 0
    for translation_row in translation_table:
        if (translation_row['FEM Name'] == fem_unit['Unit'] and translation_row['PSSE Name'] == template_unit['Unit']
                and translation_row['Unit ID'] == template_unit['Unit-ID']):
            unit_match = 1

    return unit_match


# Get the CT and ST multiplier factor for CC units from Translation Table
def get_multiplier(template_row, translation_table):
    multiplier = 1

    for translation_row in translation_table:
        if (translation_row['PSSE Name'] == template_row['Unit'] and
                translation_row['Unit ID'] == template_row['Unit-ID']):
            multiplier = translation_row['Multiplier']

    return multiplier


# When we have a match, transfer gen data from FCST file to output file, via template
def transfer_data(template_row, fcst_row, translation_table):
    multiplier = get_multiplier(template_row, translation_table)
    for hour in range(24):
        index = str(hour+1)
        template_row[index] = round(fcst_row[index] * multiplier, 3)


# Update the date from rank (0-6) to actual date
def update_date(template_row, ranked_days):
    for day in ranked_days:
        if day[1] == template_row['Date']:
            template_row['Date'] = day[0]
