import pandas

fcst_dicts = [{'Day': 'day1', 'Unit': 'unit1', 'FirstData': 'd1.1.1', 'SecondData': 'd1.1.2'},
              {'Day': 'day2', 'Unit': 'unit1', 'FirstData': 'd2.1.1', 'SecondData': 'd2.1.2'},
              {'Day': 'day3', 'Unit': 'unit1', 'FirstData': 'd3.1.1', 'SecondData': 'd3.1.2'},
              {'Day': 'day4', 'Unit': 'unit1', 'FirstData': 'd4.1.1', 'SecondData': 'd4.1.2'},
              {'Day': 'day5', 'Unit': 'unit1', 'FirstData': 'd5.1.1', 'SecondData': 'd5.1.2'},
              {'Day': 'day6', 'Unit': 'unit1', 'FirstData': 'd6.1.1', 'SecondData': 'd6.1.2'},
              {'Day': 'day1', 'Unit': 'unit2', 'FirstData': 'd1.2.1', 'SecondData': 'd1.2.2'},
              {'Day': 'day2', 'Unit': 'unit2', 'FirstData': 'd2.2.1', 'SecondData': 'd2.2.2'},
              {'Day': 'day3', 'Unit': 'unit2', 'FirstData': 'd3.2.1', 'SecondData': 'd3.2.2'},
              {'Day': 'day4', 'Unit': 'unit2', 'FirstData': 'd4.2.1', 'SecondData': 'd4.2.2'},
              {'Day': 'day5', 'Unit': 'unit2', 'FirstData': 'd5.2.1', 'SecondData': 'd5.2.2'},
              {'Day': 'day6', 'Unit': 'unit2', 'FirstData': 'd6.2.1', 'SecondData': 'd6.2.2'},
              ]

translation_table = [['unit1', 'unidad1'], ['unit2', 'unidad2']]

csv_template = pandas.read_csv(r'C:\Users\MyPC\Documents\GLIP-local\csv-test.csv')
csv_rows = []

# Create a list of dictionaries with each row from FEM file, also has row numbers
for row_num, row in csv_template.iterrows():
    row_dict = row.to_dict()
    row_dict['row'] = row_num
    csv_rows.append(row_dict)


# Function that compares the unit name in 2 files.  Returns 1 if units match
def compare_units(fcst_unit, webtrans_unit):
    units_match = 0
    for unit in translation_table:
        if unit[0] == fcst_unit and unit[1] == webtrans_unit:
            units_match = 1

    return units_match


# For each row in WebTrans file, loop through each row in FEM file.  If the day matches, run the translation for  unit
# If the unit matches, add the data into the hourly boxes
for row in csv_rows:
    for dict in fcst_dicts:
        if dict['Day'] == row['Date']:
            unit = compare_units(dict['Unit'], row['Unit'])

            if unit == 1:
                row['Data1'] = dict['FirstData']
                row['Data2'] = dict['SecondData']
                # print('We got a match!! \nDay:', dict['Day'], '\nFEM Unit: ', dict['Unit'], '\nWebTrans Unit: ', row['Unit'], '\n')

for row in csv_rows:
    print (row)













