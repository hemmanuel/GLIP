import os
from pandas import *
import datetime


def main():
    fcst_path = get_fcst_path(path)

    print(fcst_path)


# Find the file that begins with FCST, and return the location
def get_fcst_path(working_directory):
    fcst_location = ''
    files = []
    file_day = ''
    min_date = datetime.datetime(3000, 1, 1).date()

    for file in os.listdir(working_directory):
        parsed_file = file[:-5]

        if os.path.isfile(os.path.join(working_directory, file)) and 'FCST' in file:
            try:
                file_day = datetime.datetime.strptime(parsed_file, date_format).date()

            except ValueError as v:
                if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
                    parsed_file = parsed_file[:-(len(v.args[0]) - 26)]
                    file_day = datetime.datetime.strptime(parsed_file, date_format).date()

                else:
                    raise
            files.append([file_day, file])

    for file in files:
        day = file[0]
        location = file[1]
        if day < min_date:
            min_date = day
            fcst_location = location

    print(min_date, fcst_location)




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
date_format = 'FCST_%d%B%Y'

main()