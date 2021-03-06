import GLIP_Functions
import pandas


# Main function calling all other functions in program
def main():
    # Find Path & Filename for FCST File in Working Directory
    fcst_path = GLIP_Functions.get_fcst_path(path)

    # Return a Pandas Dataframe containing the FutureGen Tab of FCST File
    future_gen_tab = GLIP_Functions.get_future_gen(fcst_path)

    # Return a List of Dictionaries For Each Row in FCST FutureGen in Following Format:
    # [{'Date':['06/23/2021, 1], 'Unit':'STN-1', '1':'145', '2':'157', '3':'160'...}, {'Date':['06/24/2021, 2], 'Unit':]
    fcst_rows, ranked_days = GLIP_Functions.get_row_dicts(future_gen_tab)

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
