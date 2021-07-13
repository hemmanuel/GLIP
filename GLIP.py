import GLIP_Functions
import pandas


# Main function calling all other functions in program
def main():
    fcst_file_count = 0
    current_day_fcst_path = ''
    nextday_fcst_path = ''
    next_day_future_gen_tab = None
    current_day_future_gen_tab = None
    second_half_of_current_day = None

    # Find Path & Filename for FCST File in Working Directory
    fcst_files = GLIP_Functions.get_fcst_path(path)

    # If two FCST files were returned, then we have today and tomorrow.  Set variables and flag
    if len(fcst_files) == 2:
        nextday_fcst_path = fcst_files[0]
        current_day_fcst_path = fcst_files[1]
        fcst_file_count = 2

    # If only one FCST file was returned, then we only have today (or some other day).  Set variables and flag
    elif len(fcst_files) == 1:
        current_day_fcst_path = fcst_files[0]
        fcst_file_count = 1

    # Return a Pandas Dataframe containing the FutureGen Tab of FCST File for current day
    current_day_future_gen_tab = GLIP_Functions.get_df_from_excel(current_day_fcst_path, "FutureGen")

    # If next day FCST exists, return a Pandas Dataframe containing the FutureGen Tab of FCST File
    if fcst_file_count == 2:
        next_day_future_gen_tab = GLIP_Functions.get_df_from_excel(nextday_fcst_path, "FutureGen")
        # Return a Pandas Dataframe containing the "Second half of day prior" tab.
        second_half_of_current_day = GLIP_Functions.get_df_from_excel(nextday_fcst_path, "Second half of day prior")

    # Return a List of Dictionaries For Each Row in FCST FutureGen in Following Format:
    # [{'Date':['06/23/2021, 1], 'Unit':'STN-1', '1':'145', '2':'157', '3':'160'...}, {'Date':['06/24/2021, 2], 'Unit':]
    fcst_rows, ranked_days = GLIP_Functions.get_row_dicts(current_day_future_gen_tab, next_day_future_gen_tab,
                                                          second_half_of_current_day)

    # Return a List of Dictionaries Containing Each Row in Translation Table in Following Format:
    # [{'FEM Name': 'CANE-2_CC', 'PSSE Name': 'CI#2 CT     13.800', 'Unit ID': 1, 'Multiplier': 0.643312102}, {FEM Na..]
    translation_table = GLIP_Functions.csv_to_dict_list(translation_path)

    # Return a List of Dictionaries Containing Each Row in Output Template File in Following Format: (nan = null)
    # [{'Date': 0, 'Unit': 'CI#2 CT 13.800', 'Unit-ID': 1, '0': nan, '1': nan, '2': nan, '3': nan,...]
    output_template = GLIP_Functions.csv_to_dict_list(output_template_path)

# For each row in Template file, loop through each row in FCST file.  If day and unit matches update output file
    for template_row in output_template:
        GLIP_Functions.update_date(template_row, ranked_days)

        # Check if dates and units match between the 2 files
        for fcst_row in fcst_rows:
            dates_match = GLIP_Functions.check_date_match(fcst_row, template_row, ranked_days)
            units_match = GLIP_Functions.check_unit_match(fcst_row, template_row, translation_table)

            # If dates and units match, transfer data on current row from FCST file to output file
            if dates_match == 1 and units_match == 1:
                GLIP_Functions.transfer_data(template_row, fcst_row, translation_table)

        output_list.append(template_row)

    # Convert Final List of Dicts to Pandas Dataframe, then write to CSV file
    output_dataframe = pandas.DataFrame(output_list)
    output_dataframe.to_csv(output_file, index=False)


# Initialize global variables and call main function
if __name__ == "__main__":

    path = r'C:\GLIP'
    output_template_path = r'C:\GLIP\FMPP-GenData-TEMPLATE.csv'
    translation_path = r'C:\GLIP\translation-table.csv'
    output_file = r'C:\GLIP\FMPP-Gen-Forecast.csv'
    output_list = []
    # Call main function to begin program
    main()
