import os
from pandas import *
import datetime


def main():
    fcst_path = get_fcst_path(path)

    print(fcst_path)


# Find the file that begins with FCST, and return the location
def get_fcst_path(working_directory):
    fcst_location = ''

    for file in os.listdir(working_directory):
        if os.path.isfile(os.path.join(working_directory, file)) and 'FCST' in file:
            try:
                file_day = datetime.datetime.strptime(file, date_format).date()
                print(file_day, file)

            except ValueError:
                continue


    # for row in row_list:
    #
    #     if isinstance(row['Date'], str):
    #         try:
    #             date = datetime.datetime.strptime(str(row['Date']), date_format).date()
    #
    #             if date < min_date:
    #                 min_date = date
    #
    #         except ValueError:
    #             continue

    return fcst_location


path = r'C:\Users\MyPC\Documents\GLIP-local\STRPTEST'
date_format = 'FCST_%d%B%Y.xlsx'

main()