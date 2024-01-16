#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import glob
import os
import sys
import os
import datetime
from flask import Flask, render_template_string

app = Flask(__name__)

column_name_map = {
    'Info': {'en': 'Info', 'de': 'Info'},
    'Name': {'en': 'Name', 'de': 'Name'},
    'Position': {'en': 'Position', 'de': 'Position'},
    'Nation': {'en': 'Nat', 'de': 'Nation'},
    'Age': {'en': 'Age', 'de': 'Alter'},
    'Club': {'en': 'Club', 'de': 'Verein'},
    'Transfer Value': {'en': 'Transfer Value', 'de': 'Transferwert'},
    'Wage': {'en': 'Wage', 'de': 'Gehalt'},
    'Min AP': {'en': 'Min AP', 'de': 'Min Abl'},
    'Min Fee Rls': {'en': 'Min Fee Rls', 'de': 'Ausstiegskl.'},
    'Min Fee Rls to Foreign Clubs': {'en': 'Min Fee Rls to Foreign Clubs', 'de': 'Ausstiegskl. ausländ. Vereine'},
    'Personality': {'en': 'Personality', 'de': 'Persönlichkeit'},
    'Media Handling': {'en': 'Media Handling', 'de': 'Medienumgang'},
    'Left Foot': {'en': 'Left Foot', 'de': 'Linker Fuß'},
    'Right Foot': {'en': 'Right Foot', 'de': 'Rechter Fuß'},
    '1v1': {'en': '1v1', 'de': '1v1'},
    'Acc': {'en': 'Acc', 'de': 'Ant'},
    'Aer': {'en': 'Aer', 'de': 'HB'},
    'Agg': {'en': 'Agg', 'de': 'Agg'},
    'Agi': {'en': 'Agi', 'de': 'Bew'},
    'Ant': {'en': 'Ant', 'de': 'Azp'},
    'Bal': {'en': 'Bal', 'de': 'Bal'},
    'Bra': {'en': 'Bra', 'de': 'Mut'},
    'Cmd': {'en': 'Cmd', 'de': 'StK'},
    'Cnt': {'en': 'Cnt', 'de': 'Kon'},
    'Cmp': {'en': 'Cmp', 'de': 'Ner'},
    'Cro': {'en': 'Cro', 'de': 'Fla'},
    'Dec': {'en': 'Dec', 'de': 'Ent'},
    'Det': {'en': 'Det', 'de': 'Zie'},
    'Dri': {'en': 'Dri', 'de': 'Dri'},
    'Fin': {'en': 'Fin', 'de': 'Abs'},
    'Fir': {'en': 'Fir', 'de': 'Ann'},
    'Fla': {'en': 'Fla', 'de': 'Flr'},
    'Han': {'en': 'Han', 'de': 'Hal'},
    'Hea': {'en': 'Hea', 'de': 'Kpf'},
    'Jum': {'en': 'Jum', 'de': 'Spr'},
    'Kic': {'en': 'Kic', 'de': 'Abs'},
    'Ldr': {'en': 'Ldr', 'de': 'Füh'},
    'Lon': {'en': 'Lon', 'de': 'WS'},
    'Mar': {'en': 'Mar', 'de': 'Dck'},
    'OtB': {'en': 'OtB', 'de': 'Ohn'},
    'Pac': {'en': 'Pac', 'de': 'Sch'},
    'Pas': {'en': 'Pas', 'de': 'Pas'},
    'Pos': {'en': 'Pos', 'de': 'Ste'},
    'Ref': {'en': 'Ref', 'de': 'Ref'},
    'Sta': {'en': 'Sta', 'de': 'Aus'},
    'Str': {'en': 'Str', 'de': 'Kra'},
    'Tck': {'en': 'Tck', 'de': 'Tck'},
    'Tea': {'en': 'Tea', 'de': 'Tea'},
    'Tec': {'en': 'Tec', 'de': 'Tec'},
    'Thr': {'en': 'Thr', 'de': 'Abw'},
    'TRO': {'en': 'TRO', 'de': 'TzH'},
    'Vis': {'en': 'Vis', 'de': 'Übs'},
    'Wor': {'en': 'Wor', 'de': 'Esf'},
    'Cor': {'en': 'Cor', 'de': 'Eck'},
    'Height': {'en': 'Height', 'de': 'Größe'},
}

def is_valid_file(file_path):
    return os.path.isfile(file_path)

def read_html_file(file_path):
    if not file_path.lower().endswith('.html'):
        raise ValueError(f"The file {file_path} is not a valid HTML file.")
    return pd.read_html(file_path, header=0, encoding="utf-8", keep_default_na=False)[0]

def get_language_of_html_file(data_frame):
    if 'Height' in data_frame.columns:
        return 'en'
    elif 'Größe' in data_frame.columns:
        return 'de'
    else:
        print("Language couldn't be detected!")
        exit()

def is_valid_number(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def remove_columns_from_data_frame(data_frame_input, column_names):
    data_frame = data_frame_input.copy()
    for column_name in column_names:
        data_frame.drop(column_name_map[column_name].get(language), axis=1, inplace=True)
    return data_frame

def filter_data_frame_content_validity(data_frame_input):
    data_frame = data_frame_input.copy()
    columns_to_check = data_frame.loc[:, '1v1':data_frame.columns[-2]].columns
    data_frame['entry_valid'] = data_frame[columns_to_check].apply(lambda row: all(is_valid_number(str(val)) for val in row), axis=1)
    data_frame = data_frame[data_frame['entry_valid']]
    data_frame.drop('entry_valid', axis=1, inplace=True)
    return data_frame

def generate_html_table(data_frame):
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Visualization</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.24/css/jquery.dataTables.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/fixedcolumns/3.3.2/css/fixedColumns.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/fixedcolumns/3.3.2/js/dataTables.fixedColumns.min.js"></script>
    <style>
        /* Add styles to make filter input fields visible */
        input.filter {
            width: 80px; /* Adjust the width as needed */
        }
        .range-filter {
            display: inline-block;
            margin-right: 10px;
        }
    </style>
    <script>
        $(document).ready(function() {
            var table = $('#dataTable').DataTable({
                scrollX: true,
                scrollY: true,
            });
            new $.fn.dataTable.FixedColumns(table, {
                leftColumns: 1,
                rightColumns: 0
            });
        });
    </script>
</head>
<body>
    {{ table_data | safe }}
</body>
</html>
    """
    table_html = data_frame.to_html(classes="display", table_id="dataTable", escape=False, index=False)
    with app.app_context():
        return render_template_string(html_template, table_data=table_html)


def append_date_time_to_filename(filename, format="%Y%m%d_%H%M%S"):
    current_datetime = datetime.datetime.now().strftime(format)
    filename_parts = filename.rsplit('.', 1)

    if len(filename_parts) == 1:
        # If there is no file extension
        return f"{filename}_{current_datetime}"
    else:
        # If there is a file extension
        base_name, extension = filename_parts
        return f"{base_name}_{current_datetime}.{extension}"

def write_output_file(filename, content):
    open(filename, 'w', encoding='utf-8').write(content)

def convert_column_to_int64(data_frame, column_name):
    df = data_frame.copy()
    df[column_name] = df[column_name].astype('int64')
    return df

def calculate_position_value(data_frame, key, green, blue):
    value = 0.0
    df = data_frame.copy()
    for i in key:
        df = convert_column_to_int64(df, column_name_map[i].get(language))
        value = value + 5 * df[column_name_map[i].get(language)]
    for j in green:
        df = convert_column_to_int64(df, column_name_map[j].get(language))
        value = value + 3 * df[column_name_map[j].get(language)]
    for k in blue:
        df = convert_column_to_int64(df, column_name_map[k].get(language))
        value = value + df[column_name_map[k].get(language)]
    return (value/(len(key)*5 + len(green)*3 + len(blue))).round(1)

def handle_keeper_roles(data_frame_input, filename):
    df = data_frame_input.copy()
    df['Defending GK'] = calculate_position_value(squad_filtered, {'Agi', 'Ref'}, {'Aer', 'Cmd', 'Han', 'Kic', 'Cnt', 'Pos'}, {'1v1', 'Thr', 'Ant', 'Dec'})
    df['Sweeper Keeper'] = calculate_position_value(squad_filtered, {'Agi', 'Ref'}, {'Cmd', 'Kic', '1v1', 'Ant', 'Cnt', 'Pos'}, {'Aer', 'Fir', 'Han', 'Pas', 'TRO', 'Dec', 'Vis', 'Acc'})
    content = generate_html_table(df)
    write_output_file(append_date_time_to_filename("keeper_roles_" + filename), content)

def handle_central_defender_roles(data_frame_input, filename):
    df = data_frame_input.copy()
    df['BP Defender - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Mar', 'Pas', 'Tck', 'Pos', 'Str'}, {'Fir', 'Tec', 'Agg', 'Ant', 'Bra', 'Cnt', 'Dec', 'Vis'})
    df['BP Defender - Stopper'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Pas', 'Tck', 'Pos', 'Str', 'Agg', 'Bra', 'Dec'}, {'Fir', 'Tec', 'Ant', 'Cnt', 'Vis', 'Mar'})
    df['BP Defender - Cover'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Mar', 'Pas', 'Tck', 'Pos', 'Ant', 'Cnt', 'Dec'}, {'Fir', 'Tec', 'Bra', 'Vis', 'Str', 'Hea'})
    df['Cntl Defender - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Mar', 'Tck', 'Pos', 'Str'}, {'Agg', 'Ant', 'Bra', 'Cnt', 'Dec'})
    df['Cntl Defender - Stopper'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Tck', 'Agg', 'Bra', 'Dec', 'Pos', 'Str'}, {'Mar', 'Ant', 'Cnt'})
    df['Cntl Defender - Cover'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Mar', 'Tck', 'Ant', 'Cnt', 'Dec', 'Pos'}, {'Hea', 'Bra', 'Str'})
    df['Libero - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Fir', 'Hea', 'Mar', 'Pas', 'Tck', 'Tec', 'Dec', 'Pos', 'Tea', 'Str'}, {'Ant', 'Bra', 'Cnt', 'Sta'})
    df['Libero - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Fir', 'Hea', 'Mar', 'Pas', 'Tck', 'Tec', 'Dec', 'Pos', 'Tea', 'Str'}, {'Dri', 'Ant', 'Bra', 'Cnt', 'Vis', 'Sta'})
    df['Non CB - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Mar', 'Tck', 'Pos', 'Str'}, {'Agg', 'Ant', 'Bra', 'Cnt'})
    df['Non CB - Stopper'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Tck', 'Agg', 'Bra', 'Pos', 'Str'}, {'Mar', 'Ant', 'Cnt'})
    df['Non CB - Cover'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Mar', 'Tck', 'Ant', 'Cnt', 'Pos'}, {'Hea', 'Bra', 'Str'})
    df['Wide CB - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Mar', 'Tck', 'Pos', 'Str'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Agg', 'Ant', 'Bra', 'Cnt', 'Dec', 'Wor', 'Agi'})
    df['Wide CB - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Dri', 'Hea', 'Mar', 'Tck', 'Pos', 'Str'}, {'Cro', 'Fir', 'Pas', 'Tec', 'Agg', 'Ant', 'Bra', 'Cnt', 'Dec', 'OtB', 'Wor', 'Agi', 'Sta'})
    df['Wide CB - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Cro', 'Dri', 'Hea', 'Mar', 'Tck', 'OtB', 'Sta', 'Str'}, {'Fir', 'Pas', 'Tec', 'Agg', 'Ant', 'Bra', 'Cnt', 'Dec', 'Pos', 'Wor', 'Agi'})
    content = generate_html_table(df) 
    write_output_file(append_date_time_to_filename("central_defender_roles_" + filename), content)

def handle_outside_defender_roles(data_frame_input, filename):
    df = data_frame_input.copy()
    df['Comp Wing Back - Support'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Tec', 'OtB', 'Tea'}, {'Fir', 'Mar', 'Pas', 'Tck', 'Ant', 'Dec', 'Fla', 'Pos', 'Agi', 'Bal'})
    df['Comp Wing Back - Attack'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Tec', 'Fla', 'OtB', 'Tea'}, {'Fir', 'Mar', 'Pas', 'Tck', 'Ant', 'Dec', 'Pos', 'Agi', 'Bal'})
    df['Full Back - Defend'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Mar', 'Tck', 'Ant', 'Cnt', 'Pos', 'Pos'}, {'Cro', 'Pas', 'Dec', 'Tea'})
    df['Full Back - Support'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Mar', 'Tck', 'Ant', 'Cnt', 'Pos', 'Tea'}, {'Cro', 'Dri', 'Pas', 'Tec', 'Dec'})
    df['Full Back - Attack'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Mar', 'Tck', 'Ant', 'Pos', 'Tea'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Cnt', 'Dec', 'OtB', 'Agi'})
    df['Inv Full Back - Defend'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Hea', 'Mar', 'Tck', 'Pos', 'Str'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Agg', 'Ant', 'Bra', 'Cmp', 'Cnt', 'Dec', 'Agi', 'Jum'})
    df['Inv Wing Back - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Pas', 'Tck', 'Ant', 'Dec', 'Pos', 'Tea'}, {'Fir', 'Mar', 'Tec', 'Cmp', 'Cnt', 'OtB', 'Agi'})
    df['Inv Wing Back - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tck', 'Cmp', 'Dec', 'Tea'}, {'Mar', 'Tec', 'Ant', 'Cnt', 'OtB', 'Pos', 'Vis', 'Agi'})
    df['Inv Wing Back - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tck', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea', 'Vis'}, {'Cro', 'Dri', 'Lon', 'Mar', 'Ant', 'Cnt', 'Fla', 'Pos', 'Agi'})
    df['Wing Back - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Mar', 'Tck', 'Ant', 'Pos', 'Tea'}, {'Cro', 'Dri', 'Fir', 'Pas', 'Tec', 'Cnt', 'Dec', 'OtB', 'Agi', 'Bal'})
    df['Wing Back - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Mar', 'Tck', 'OtB', 'Tea'}, {'Fir', 'Pas', 'Tec', 'Ant', 'Cnt', 'Dec', 'Pos', 'Agi', 'Bal'})
    df['Wing Back - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Tck', 'Tec', 'OtB', 'Tea'}, {'Fir', 'Mar', 'Pas', 'Ant', 'Cnt', 'Dec', 'Fla', 'Pos', 'Agi', 'Bal'})
    df['Non FB - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Mar', 'Tck', 'Ant', 'Pos', 'Str'}, {'Hea', 'Agg', 'Bra', 'Cnt', 'Tea'})
    content = generate_html_table(df)
    write_output_file(append_date_time_to_filename("outside_defender_roles_" + filename), content)

def handle_midfielder_roles(data_frame_input, filename):
    df = data_frame_input.copy()
    df['Adv Playmaker - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea', 'Vis'}, {'Dri', 'Ant', 'Fla', 'Agi'})
    df['Adv Playmaker - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea', 'Vis'}, {'Dri', 'Ant', 'Fla', 'Agi'})
    df['Anchor - Defend'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Mar', 'Tck', 'Ant', 'Cnt', 'Dec', 'Pos'}, {'Cmp', 'Tea', 'Str'})
    df['Attck Midf - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Lon', 'Pas', 'Tec', 'Ant', 'Dec', 'Fla', 'OtB'}, {'Dri', 'Cmp', 'Vis', 'Agi'})
    df['Attck Midf - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Fir', 'Lon', 'Pas', 'Tec', 'Ant', 'Dec', 'Fla', 'OtB'}, {'Fin', 'Cmp', 'Vis', 'Agi'})
    df['Ball Win Midf - Defend'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Tck', 'Agg', 'Ant', 'Tea'}, {'Mar', 'Bra', 'Cnt', 'Pos', 'Agi', 'Str'})
    df['Ball Win Midf - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Tck', 'Agg', 'Ant', 'Tea'}, {'Mar', 'Pas', 'Bra', 'Cnt', 'Agi', 'Str'})
    df['Box2Box Midf - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Pas', 'Tck', 'OtB', 'Tea'}, {'Dri', 'Fin', 'Fir', 'Lon', 'Tec', 'Agg', 'Ant', 'Cmp', 'Dec', 'Pos', 'Bal', 'Str'})
    df['Carrilero - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Fir', 'Pas', 'Tck', 'Dec', 'Pos', 'Tea'}, {'Tec', 'Ant', 'Cmp', 'Cnt', 'OtB', 'Vis'})
    df['Ctrl Midf - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Tck', 'Cnt', 'Dec', 'Pos', 'Tea'}, {'Fir', 'Mar', 'Pas', 'Tec', 'Agg', 'Ant', 'Cmp'})
    df['Ctrl Midfl - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tck', 'Dec', 'Tea'}, {'Tec', 'Ant', 'Cmp', 'Cnt', 'OtB', 'Vis'})
    df['Ctrl Midfl - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Dec', 'OtB'}, {'Lon', 'Tck', 'Tec', 'Ant', 'Cmp', 'Tea', 'Vis'})
    df['Deep Playmaker - Defend'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Tea', 'Vis'}, {'Tck', 'Ant', 'Pos', 'Bal'})
    df['Deep Playmaker - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Tea', 'Vis'}, {'Ant', 'OtB', 'Pos', 'Bal'})
    df['Def Midfl - Defend'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Tck', 'Ant', 'Cnt', 'Pos', 'Tea'}, {'Mar', 'Pas', 'Agg', 'Cmp', 'Str', 'Dec'})
    df['Def Midfl - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Tck', 'Ant', 'Cnt', 'Pos', 'Tea'}, {'Fir', 'Mar', 'Pas', 'Agg', 'Cmp', 'Dec', 'Str'})
    df['Half Back - Defend'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Mar', 'Tck', 'Ant', 'Cmp', 'Cnt', 'Dec', 'Pos', 'Tea'}, {'Fir', 'Pas', 'Agg', 'Bra', 'Jum', 'Str'})
    df['Segundo Volante - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Mar', 'Pas', 'Tck', 'OtB', 'Pos'}, {'Fin', 'Fir', 'Lon', 'Ant', 'Cmp', 'Cnt', 'Dec', 'Bal', 'Str'})
    df['Segundo Volante - Attack'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Fin', 'Lon', 'Pas', 'Tck', 'Ant', 'OtB', 'Pos'}, {'Fir', 'Mar', 'Cmp', 'Cnt', 'Dec', 'Bal'})
    df['Roam Playmaker - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tec', 'Ant', 'Cmp', 'Dec', 'OtB', 'Tea', 'Vis'}, {'Dri', 'Lon', 'Cnt', 'Pos', 'Agi', 'Bal'})
    df['Mezzala - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Pas', 'Tec', 'Dec', 'OtB'}, {'Dri', 'Fir', 'Lon', 'Tck', 'Ant', 'Cmp', 'Vis', 'Bal'})
    df['Mezzala - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Pas', 'Tec', 'Dec', 'OtB', 'Vis'}, {'Fin', 'Fir', 'Lon', 'Ant', 'Cmp', 'Fla', 'Bal'})
    df['Regista - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Fla', 'OtB', 'Tea', 'Vis'}, {'Dri', 'Lon', 'Ant', 'Bal'})
    df['Def Winger - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Tec', 'Ant', 'OtB', 'Pos', 'Tea'}, {'Cro', 'Dri', 'Fir', 'Mar', 'Tck', 'Agg', 'Cnt', 'Dec'})
    df['Def Winger - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Pas', 'Tec', 'OtB', 'Tea'}, {'Dri', 'Fir', 'Mar', 'Pas', 'Tck', 'Agg', 'Ant', 'Cmp', 'Cnt', 'Dec', 'Pos'})
    df['Wide Midf - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Pas', 'Tck', 'Cnt', 'Dec', 'Pos', 'Tea'}, {'Cro', 'Fir', 'Mar', 'Tec', 'Ant', 'Cmp'})
    df['Wide Midf - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Pas', 'Tck', 'Dec', 'Tea'}, {'Cro', 'Fir', 'Tec', 'Ant', 'Cmp', 'Cnt', 'OtB', 'Pos', 'Vis'})
    df['Wide Midf - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Fir', 'Pas', 'Dec', 'Tea'}, {'Tck', 'Tec', 'Ant', 'Cmp', 'OtB', 'Vis'})
    df['Wide Playmaker - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Tea', 'Vis'}, {'Dri', 'OtB', 'Agi'})
    df['Wide Playmaker - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea', 'Vis'}, {'Ant', 'Fla', 'Agi'})
    df['Enganche - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Vis'}, {'Dri', 'Ant', 'Fla', 'OtB', 'Tea', 'Agi'})
    df['Raumdeuter - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fin', 'Ant', 'Cmp', 'Cnt', 'Dec', 'OtB', 'Bal'}, {'Fir', 'Tec'})
    content = generate_html_table(df)
    write_output_file(append_date_time_to_filename("midfielder_roles_" + filename), content)

def handle_attacker_roles(data_frame_input, filename):
    df = data_frame_input.copy()
    df['Adv Forward - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Dri', 'Fir', 'Tec', 'Cmp', 'OtB'}, {'Pas', 'Ant', 'Dec', 'Wor', 'Agi', 'Bal', 'Sta'})
    df['Compl Forward - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Dri', 'Fir', 'Hea', 'Lon', 'Pas', 'Tec', 'Ant', 'Cmp', 'Dec', 'OtB', 'Vis', 'Agi', 'Str'}, {'Tea', 'Wor', 'Bal', 'Jum', 'Sta'})
    df['Compl Forward - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Dri', 'Fir', 'Hea', 'Tec', 'Ant', 'Cmp', 'OtB', 'Agi', 'Str'}, {'Lon', 'Pas', 'Dec', 'Tea', 'Vis', 'Wor', 'Bal', 'Jum', 'Sta'})
    df['Deep Lying Forw - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea'}, {'Ant', 'Fla', 'Vis', 'Bal', 'Str'})
    df['Deep Lying Forw - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea'}, {'Dri', 'Ant', 'Fla', 'Vis', 'Bal', 'Str'})
    df['False 9 - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Vis', 'Agi'}, {'Ant', 'Fla', 'Tea', 'Bal'})
    df['Poacher - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Ant', 'Cmp', 'OtB'}, {'Fir', 'Hea', 'Tec', 'Dec'})
    df['Pressing Forw - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Agg', 'Ant', 'Bra', 'Dec', 'Tea', 'Wor', 'Sta'}, {'Fir', 'Cmp', 'Cnt', 'Agi', 'Bal', 'Str'})
    df['Pressing Forw - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Agg', 'Ant', 'Bra', 'Dec', 'Tea', 'Wor', 'Sta'}, {'Fir', 'Pas', 'Cmp', 'Cnt', 'OtB', 'Agi', 'Bal', 'Str'})
    df['Pressing Forw - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Agg', 'Ant', 'Bra', 'OtB', 'Tea', 'Wor', 'Sta'}, {'Fir', 'Cmp', 'Cnt', 'Dec', 'Agi', 'Bal', 'Str'})
    df['Tgt Forw - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Hea', 'Bra', 'Tea', 'Bal', 'Jum', 'Str'}, {'Fir', 'Agg', 'Ant', 'Cmp', 'Dec', 'OtB'})
    df['Tgt Forw - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Hea', 'Bra', 'Cmp', 'OtB', 'Bal', 'Jum', 'Str'}, {'Fir', 'Agg', 'Ant', 'Dec', 'Tea'})
    df['Trequarista - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Fla', 'OtB', 'Vis'}, {'Ant', 'Agi', 'Bal'})
    df['Wide Tgt Forw - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Hea', 'Bra', 'Tea', 'Jum', 'Str'}, {'Cro', 'Fir', 'Ant', 'OtB', 'Bal'})
    df['Wide Tgt Forw - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Hea', 'Bra', 'OtB', 'Jum', 'Str'}, {'Cro', 'Fin', 'Fir', 'Ant', 'Tea', 'Bal'})
    df['Winger - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Tec', 'Agi'}, {'Fir', 'Pas', 'OtB', 'Bal'})
    df['Winger - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Tec', 'Agi'}, {'Fir', 'Pas', 'Ant', 'Fla', 'OtB', 'Bal'})
    df['Ins Forward - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Fin', 'Fir', 'Tec', 'OtB', 'Agi'}, {'Lon', 'Pas', 'Ant', 'Cmp', 'Fla', 'Vis', 'Bal'})
    df['Ins Forward - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Fin', 'Fir', 'Tec', 'Ant', 'OtB', 'Agi'}, {'Lon', 'Pas', 'Cmp', 'Fla', 'Bal'})
    df['Inv Winger - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Pas', 'Tec', 'Agi'}, {'Fir', 'Lon', 'Cmp', 'Dec', 'OtB', 'Vis', 'Bal'})
    df['Inv Winger - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Pas', 'Tec', 'Agi'}, {'Fir', 'Lon', 'Ant', 'Cmp', 'Dec', 'Fla', 'OtB', 'Vis', 'Bal'})
    df['Shadow Striker - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Fin', 'Fir', 'Ant', 'Cmp', 'OtB'}, {'Pas', 'Tec', 'Cnt', 'Dec', 'Agi', 'Bal'})
    content = generate_html_table(df)
    write_output_file(append_date_time_to_filename("attacker_roles_" + filename), content)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    # Get the file path from the command-line argument
    file_path = sys.argv[1]

    # Check if the input is a valid file
    if not is_valid_file(file_path):
        print(f"{file_path} is not a valid file or does not exist.")
        exit()

    try:
        squad_rawdata = read_html_file(file_path)
        language = get_language_of_html_file(squad_rawdata)

        squad_stripped = remove_columns_from_data_frame(squad_rawdata, {'Info', 'Media Handling', 'Min Fee Rls', 'Min Fee Rls to Foreign Clubs', 'Personality', 'Min AP'})

        squad_filtered = filter_data_frame_content_validity(squad_stripped)
        if squad_filtered.empty:
            print('Given data input has no valid entry - Not all attributes are set')
            exit()

        handle_keeper_roles(squad_filtered, file_path)
        handle_central_defender_roles(squad_filtered, file_path)
        handle_outside_defender_roles(squad_filtered, file_path)
        handle_midfielder_roles(squad_filtered, file_path)
        handle_attacker_roles(squad_filtered, file_path)

    except ValueError as e:
        print(e)
