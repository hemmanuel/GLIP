import os
from pandas import *
import datetime


# Find the file that begins with FCST, and return the location
def get_fcst_path(working_directory):
    fcst_location = ''
    for file in os.listdir(working_directory):
        if os.path.isfile(os.path.join(working_directory, file)) and 'FCST' in file:
            fcst_location = working_directory + "\\" + file
            fcst_time = os.path.getmtime(fcst_location)
            fcst_time = datetime.datetime.fromtimestamp(fcst_time).strftime('%Y-%m-%d %H:%M:%S')
            print(fcst_location, '\n', fcst_time)

    return fcst_location


# # Read FCST file into Pandas, & create a dataframe with the future gen tab
# def get_future_gen(fcst_location):
#     fcst_df = pandas.ExcelFile(fcst_location)
#     future_gen_df = pandas.read_excel(fcst_df, "FutureGen", skiprows=3)
#
#     return future_gen_df
#
#
# # Ex Output:
# # [{'Date':['06/23/2021, 1], 'Unit':'STN-1', '1':'145', '2':'157', '3':'160'...}, {'Date':['06/24/2021, 2], 'Unit'...]
# def get_row_dicts(future_gen_df):
#     # Acquire current date from computer time
#     min_date = datetime.datetime(3000, 1, 1).date()
#     date_format = '%m/%d/%Y'
#
#     row_list = []
#
#     # Go through each row in file and populate a list of dictionaries for each row, with the date ranked from today.
#     for row_num, row in future_gen_df.iterrows():
#         row_dict = row.to_dict()
#         row_list.append(row_dict)
#
#     # Get minimum date in FEM file
#     for row in row_list:
#
#         if isinstance(row['Date'], str):
#             try:
#                 date = datetime.datetime.strptime(str(row['Date']), date_format).date()
#
#                 if date < min_date:
#                     min_date = date
#
#             except ValueError:
#                 continue
#
#     # Go through each row in the list of rows, and replace the date with a list containing date and rank [06/23/2021, 1]
#     for row in row_list:
#
#         # Make sure value is of type String (the other non-date values in this column read in as NaN)
#         if isinstance(row['Date'], str):
#
#             # Save the date that is in current row
#             date_string = row['Date']
#
#             # Make sure that the date is in format MM/DD/YYYY
#             try:
#                 date = datetime.datetime.strptime(str(row['Date']), date_format).date()
#                 day_rank = (date - min_date).days + 1
#
#             except ValueError:
#                 continue
#
#             # Update the list of rows
#             row['Date'] = [date_string, day_rank]
#
#     return row_list


# Main function calling all other functions in program
def main():
    fcst_path = get_fcst_path(path)
    # future_gen_tab = get_future_gen(fcst_path)
    # fcst_rows = get_row_dicts(future_gen_tab)
    # for row in fcst_rows:
    #     print(row)


# Initialize global variables and call main function
if __name__ == "__main__":

    # Location where all files are located
    path = r'C:\GLIP'
    output_template_path = r'C:\GLIP\FEM1522 - Generation Data-TEMPLATE.csv'

    # Call main function to begin program
    main()
