import os
from pandas import *
import datetime


# Find the file that begins with FCST, and return the location
def get_fcst_path(working_directory):
    fcst_location = ''
    for file in os.listdir(working_directory):
        if os.path.isfile(os.path.join(working_directory, file)) and 'FCST' in file:
            fcst_location = working_directory + "\\" + file

    return fcst_location


# Read FCST file into Pandas, & create a dataframe with the future gen tab
def get_future_gen(fcst_location):
    fcst_df = pandas.ExcelFile(fcst_location)
    future_gen_df = pandas.read_excel(fcst_df, "FutureGen", skiprows=3)

    return future_gen_df


# Ex Output:
# [{'Date':['06/23/2021, 1], 'Unit':'STN-1', '1':'145', '2':'157', '3':'160'...}, {'Date':['06/24/2021, 2], 'Unit'...]
def get_row_dicts(future_gen_df):
    # Set the minimum date to 1/1/3000
    min_date = datetime.datetime(3000, 1, 1).date()
    date_format = '%m/%d/%Y'
    ranked_days = []
    unique_ranked_days = []

    row_list = []

    # Go through each row in file and populate a list of dictionaries for each row, with the date ranked from today.
    for row_num, row in future_gen_df.iterrows():
        row_dict = row.to_dict()
        row_list.append(row_dict)

    # Get minimum date in FEM file
    for row in row_list:

        if isinstance(row['Date'], str):
            try:
                date = datetime.datetime.strptime(str(row['Date']), date_format).date()

                if date < min_date:
                    min_date = date

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
                day_rank = (date - min_date).days + 1

            except ValueError:
                continue

            # Update the list of rows
            row['Date'] = [date_string, day_rank]
            ranked_days.append(([date_string, day_rank]))

            # Populate a list with unique days in FCST file, ranked from 1-6
            for day in ranked_days:
                if day not in unique_ranked_days:
                    unique_ranked_days.append([date_string, day_rank])

    return row_list, unique_ranked_days


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
        fcst_index = str(hour+1)
        template_index = str(hour)
        template_row[template_index] = round(fcst_row[fcst_index] * multiplier, 3)


# Update the date from rank (0-6) to actual date
def update_date(template_row, ranked_days):
    for day in ranked_days:
        if day[1] == template_row['Date']:
            template_row['Date'] = day[0]
