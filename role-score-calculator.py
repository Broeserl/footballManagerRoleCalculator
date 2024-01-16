#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import glob
import os
import sys
import os
import datetime

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

def generate_html(data_frame: pd.DataFrame):
    # get the table HTML from the dataframe
    table_html = data_frame.to_html(table_id="table", index=False)
    # construct the complete HTML with jQuery Data tables
    # You can disable paging or enable y scrolling on lines 20 and 21 respectively
    html = f"""
    <html>
    <header>
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
    </header>
    <body>
    {table_html}
    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready( function () {{
            $('#table').DataTable({{
                paging: false,
                order: [[12, 'desc']],
                // scrollY: 400,
            }});
        }});
    </script>
    </body>
    </html>
    """
    # return the html
    return html

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

        squad_filtered['Defending GK'] = calculate_position_value(squad_filtered, {'Agi', 'Ref'}, {'Aer', 'Cmd', 'Han', 'Kic', 'Cnt', 'Pos'}, {'1v1', 'Thr', 'Ant', 'Dec'})
        squad_filtered['Sweeper Keeper'] = calculate_position_value(squad_filtered, {'Agi', 'Ref'}, {'Cmd', 'Kic', '1v1', 'Ant', 'Cnt', 'Pos'}, {'Aer', 'Fir', 'Han', 'Pas', 'TRO', 'Dec', 'Vis', 'Acc'})

        squad_filtered['BP Defender - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Mar', 'Pas', 'Tck', 'Pos', 'Str'}, {'Fir', 'Tec', 'Agg', 'Ant', 'Bra', 'Cnt', 'Dec', 'Vis'})
        squad_filtered['BP Defender - Stopper'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Pas', 'Tck', 'Pos', 'Str', 'Agg', 'Bra', 'Dec'}, {'Fir', 'Tec', 'Ant', 'Cnt', 'Vis', 'Mar'})
        squad_filtered['BP Defender - Cover'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Mar', 'Pas', 'Tck', 'Pos', 'Ant', 'Cnt', 'Dec'}, {'Fir', 'Tec', 'Bra', 'Vis', 'Str', 'Hea'})
        squad_filtered['Cntl Defender - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Mar', 'Tck', 'Pos', 'Str'}, {'Agg', 'Ant', 'Bra', 'Cnt', 'Dec'})
        squad_filtered['Cntl Defender - Stopper'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Tck', 'Agg', 'Bra', 'Dec', 'Pos', 'Str'}, {'Mar', 'Ant', 'Cnt'})
        squad_filtered['Cntl Defender - Cover'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Mar', 'Tck', 'Ant', 'Cnt', 'Dec', 'Pos'}, {'Hea', 'Bra', 'Str'})

        squad_filtered['Comp Wing Back - Support'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Tec', 'OtB', 'Tea'}, {'Fir', 'Mar', 'Pas', 'Tck', 'Ant', 'Dec', 'Fla', 'Pos', 'Agi', 'Bal'})
        squad_filtered['Comp Wing Back - Attack'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Tec', 'Fla', 'OtB', 'Tea'}, {'Fir', 'Mar', 'Pas', 'Tck', 'Ant', 'Dec', 'Pos', 'Agi', 'Bal'})
        squad_filtered['Full Back - Defend'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Mar', 'Tck', 'Ant', 'Cnt', 'Pos', 'Pos'}, {'Cro', 'Pas', 'Dec', 'Tea'})
        squad_filtered['Full Back - Support'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Mar', 'Tck', 'Ant', 'Cnt', 'Pos', 'Tea'}, {'Cro', 'Dri', 'Pas', 'Tec', 'Dec'})
        squad_filtered['Full Back - Attack'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Mar', 'Tck', 'Ant', 'Pos', 'Tea'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Cnt', 'Dec', 'OtB', 'Agi'})
        squad_filtered['Inv Full Back - Defend'] =calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Hea', 'Mar', 'Tck', 'Pos', 'Str'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Agg', 'Ant', 'Bra', 'Cmp', 'Cnt', 'Dec', 'Agi', 'Jum'})
        squad_filtered['Inv Wing Back - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Pas', 'Tck', 'Ant', 'Dec', 'Pos', 'Tea'}, {'Fir', 'Mar', 'Tec', 'Cmp', 'Cnt', 'OtB', 'Agi'})
        squad_filtered['Inv Wing Back - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tck', 'Cmp', 'Dec', 'Tea'}, {'Mar', 'Tec', 'Ant', 'Cnt', 'OtB', 'Pos', 'Vis', 'Agi'})
        squad_filtered['Inv Wing Back - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tck', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea', 'Vis'}, {'Cro', 'Dri', 'Lon', 'Mar', 'Ant', 'Cnt', 'Fla', 'Pos', 'Agi'})
        squad_filtered['Libero - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Fir', 'Hea', 'Mar', 'Pas', 'Tck', 'Tec', 'Dec', 'Pos', 'Tea', 'Str'}, {'Ant', 'Bra', 'Cnt', 'Sta'})
        squad_filtered['Libero - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Fir', 'Hea', 'Mar', 'Pas', 'Tck', 'Tec', 'Dec', 'Pos', 'Tea', 'Str'}, {'Dri', 'Ant', 'Bra', 'Cnt', 'Vis', 'Sta'})
        squad_filtered['Non CB - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Mar', 'Tck', 'Pos', 'Str'}, {'Agg', 'Ant', 'Bra', 'Cnt'})
        squad_filtered['Non CB - Stopper'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Tck', 'Agg', 'Bra', 'Pos', 'Str'}, {'Mar', 'Ant', 'Cnt'})
        squad_filtered['Non CB - Cover'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Mar', 'Tck', 'Ant', 'Cnt', 'Pos'}, {'Hea', 'Bra', 'Str'})
        squad_filtered['Non FB - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Mar', 'Tck', 'Ant', 'Pos', 'Str'}, {'Hea', 'Agg', 'Bra', 'Cnt', 'Tea'})
        squad_filtered['Wide CB - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Hea', 'Mar', 'Tck', 'Pos', 'Str'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Agg', 'Ant', 'Bra', 'Cnt', 'Dec', 'Wor', 'Agi'})
        squad_filtered['Wide CB - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Dri', 'Hea', 'Mar', 'Tck', 'Pos', 'Str'}, {'Cro', 'Fir', 'Pas', 'Tec', 'Agg', 'Ant', 'Bra', 'Cnt', 'Dec', 'OtB', 'Wor', 'Agi', 'Sta'})
        squad_filtered['Wide CB - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Jum', 'Cmp'}, {'Cro', 'Dri', 'Hea', 'Mar', 'Tck', 'OtB', 'Sta', 'Str'}, {'Fir', 'Pas', 'Tec', 'Agg', 'Ant', 'Bra', 'Cnt', 'Dec', 'Pos', 'Wor', 'Agi'})
        squad_filtered['Wing Back - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Mar', 'Tck', 'Ant', 'Pos', 'Tea'}, {'Cro', 'Dri', 'Fir', 'Pas', 'Tec', 'Cnt', 'Dec', 'OtB', 'Agi', 'Bal'})
        squad_filtered['Wing Back - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Mar', 'Tck', 'OtB', 'Tea'}, {'Fir', 'Pas', 'Tec', 'Ant', 'Cnt', 'Dec', 'Pos', 'Agi', 'Bal'})
        squad_filtered['Wing Back - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Tck', 'Tec', 'OtB', 'Tea'}, {'Fir', 'Mar', 'Pas', 'Ant', 'Cnt', 'Dec', 'Fla', 'Pos', 'Agi', 'Bal'})
        squad_filtered['Adv Playmaker - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea', 'Vis'}, {'Dri', 'Ant', 'Fla', 'Agi'})
        squad_filtered['Adv Playmaker - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea', 'Vis'}, {'Dri', 'Ant', 'Fla', 'Agi'})
        squad_filtered['Anchor - Defend'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Mar', 'Tck', 'Ant', 'Cnt', 'Dec', 'Pos'}, {'Cmp', 'Tea', 'Str'})
        squad_filtered['Attck Midf - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Lon', 'Pas', 'Tec', 'Ant', 'Dec', 'Fla', 'OtB'}, {'Dri', 'Cmp', 'Vis', 'Agi'})
        squad_filtered['Attck Midf - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Fir', 'Lon', 'Pas', 'Tec', 'Ant', 'Dec', 'Fla', 'OtB'}, {'Fin', 'Cmp', 'Vis', 'Agi'})
        squad_filtered['Ball Win Midf - Defend'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Tck', 'Agg', 'Ant', 'Tea'}, {'Mar', 'Bra', 'Cnt', 'Pos', 'Agi', 'Str'})
        squad_filtered['Ball Win Midf - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Tck', 'Agg', 'Ant', 'Tea'}, {'Mar', 'Pas', 'Bra', 'Cnt', 'Agi', 'Str'})
        squad_filtered['Box2Box Midf - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Pas', 'Tck', 'OtB', 'Tea'}, {'Dri', 'Fin', 'Fir', 'Lon', 'Tec', 'Agg', 'Ant', 'Cmp', 'Dec', 'Pos', 'Bal', 'Str'})
        squad_filtered['Carrilero - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Fir', 'Pas', 'Tck', 'Dec', 'Pos', 'Tea'}, {'Tec', 'Ant', 'Cmp', 'Cnt', 'OtB', 'Vis'})
        squad_filtered['Ctrl Midf - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Tck', 'Cnt', 'Dec', 'Pos', 'Tea'}, {'Fir', 'Mar', 'Pas', 'Tec', 'Agg', 'Ant', 'Cmp'})
        squad_filtered['Ctrl Midfl - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tck', 'Dec', 'Tea'}, {'Tec', 'Ant', 'Cmp', 'Cnt', 'OtB', 'Vis'})
        squad_filtered['Ctrl Midfl - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Dec', 'OtB'}, {'Lon', 'Tck', 'Tec', 'Ant', 'Cmp', 'Tea', 'Vis'})
        squad_filtered['Deep Playmaker - Defend'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Tea', 'Vis'}, {'Tck', 'Ant', 'Pos', 'Bal'})
        squad_filtered['Deep Playmaker - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Tea', 'Vis'}, {'Ant', 'OtB', 'Pos', 'Bal'})
        squad_filtered['Def Midfl - Defend'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Tck', 'Ant', 'Cnt', 'Pos', 'Tea'}, {'Mar', 'Pas', 'Agg', 'Cmp', 'Str', 'Dec'})
        squad_filtered['Def Midfl - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Tck', 'Ant', 'Cnt', 'Pos', 'Tea'}, {'Fir', 'Mar', 'Pas', 'Agg', 'Cmp', 'Dec', 'Str'})
        squad_filtered['Def Winger - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Tec', 'Ant', 'OtB', 'Pos', 'Tea'}, {'Cro', 'Dri', 'Fir', 'Mar', 'Tck', 'Agg', 'Cnt', 'Dec'})
        squad_filtered['Def Winger - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Pas', 'Tec', 'OtB', 'Tea'}, {'Dri', 'Fir', 'Mar', 'Pas', 'Tck', 'Agg', 'Ant', 'Cmp', 'Cnt', 'Dec', 'Pos'})
        squad_filtered['Enganche - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Vis'}, {'Dri', 'Ant', 'Fla', 'OtB', 'Tea', 'Agi'})
        squad_filtered['Half Back - Defend'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Mar', 'Tck', 'Ant', 'Cmp', 'Cnt', 'Dec', 'Pos', 'Tea'}, {'Fir', 'Pas', 'Agg', 'Bra', 'Jum', 'Str'})
        squad_filtered['Ins Forward - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Fin', 'Fir', 'Tec', 'OtB', 'Agi'}, {'Lon', 'Pas', 'Ant', 'Cmp', 'Fla', 'Vis', 'Bal'})
        squad_filtered['Ins Forward - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Fin', 'Fir', 'Tec', 'Ant', 'OtB', 'Agi'}, {'Lon', 'Pas', 'Cmp', 'Fla', 'Bal'})
        squad_filtered['Inv Winger - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Pas', 'Tec', 'Agi'}, {'Fir', 'Lon', 'Cmp', 'Dec', 'OtB', 'Vis', 'Bal'})
        squad_filtered['Inv Winger - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Pas', 'Tec', 'Agi'}, {'Fir', 'Lon', 'Ant', 'Cmp', 'Dec', 'Fla', 'OtB', 'Vis', 'Bal'})
        squad_filtered['Mezzala - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Pas', 'Tec', 'Dec', 'OtB'}, {'Dri', 'Fir', 'Lon', 'Tck', 'Ant', 'Cmp', 'Vis', 'Bal'})
        squad_filtered['Mezzala - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Pas', 'Tec', 'Dec', 'OtB', 'Vis'}, {'Fin', 'Fir', 'Lon', 'Ant', 'Cmp', 'Fla', 'Bal'})
        squad_filtered['Raumdeuter - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fin', 'Ant', 'Cmp', 'Cnt', 'Dec', 'OtB', 'Bal'}, {'Fir', 'Tec'})
        squad_filtered['Regista - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Fla', 'OtB', 'Tea', 'Vis'}, {'Dri', 'Lon', 'Ant', 'Bal'})
        squad_filtered['Roam Playmaker - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tec', 'Ant', 'Cmp', 'Dec', 'OtB', 'Tea', 'Vis'}, {'Dri', 'Lon', 'Cnt', 'Pos', 'Agi', 'Bal'})
        squad_filtered['Segundo Volante - Support'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Mar', 'Pas', 'Tck', 'OtB', 'Pos'}, {'Fin', 'Fir', 'Lon', 'Ant', 'Cmp', 'Cnt', 'Dec', 'Bal', 'Str'})
        squad_filtered['Segundo Volante - Attack'] = calculate_position_value(squad_filtered, {'Wor', 'Sta', 'Acc', 'Pac'}, {'Fin', 'Lon', 'Pas', 'Tck', 'Ant', 'OtB', 'Pos'}, {'Fir', 'Mar', 'Cmp', 'Cnt', 'Dec', 'Bal'})
        squad_filtered['Shadow Striker - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Fin', 'Fir', 'Ant', 'Cmp', 'OtB'}, {'Pas', 'Tec', 'Cnt', 'Dec', 'Agi', 'Bal'})
        squad_filtered['Wide Midf - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Pas', 'Tck', 'Cnt', 'Dec', 'Pos', 'Tea'}, {'Cro', 'Fir', 'Mar', 'Tec', 'Ant', 'Cmp'})
        squad_filtered['Wide Midf - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Pas', 'Tck', 'Dec', 'Tea'}, {'Cro', 'Fir', 'Tec', 'Ant', 'Cmp', 'Cnt', 'OtB', 'Pos', 'Vis'})
        squad_filtered['Wide Midf - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Fir', 'Pas', 'Dec', 'Tea'}, {'Tck', 'Tec', 'Ant', 'Cmp', 'OtB', 'Vis'})
        squad_filtered['Wide Playmaker - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Tea', 'Vis'}, {'Dri', 'OtB', 'Agi'})
        squad_filtered['Wide Playmaker - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea', 'Vis'}, {'Ant', 'Fla', 'Agi'})
        squad_filtered['Wide Tgt Forw - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Hea', 'Bra', 'Tea', 'Jum', 'Str'}, {'Cro', 'Fir', 'Ant', 'OtB', 'Bal'})
        squad_filtered['Wide Tgt Forw - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Hea', 'Bra', 'OtB', 'Jum', 'Str'}, {'Cro', 'Fin', 'Fir', 'Ant', 'Tea', 'Bal'})
        squad_filtered['Winger - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Tec', 'Agi'}, {'Fir', 'Pas', 'OtB', 'Bal'})
        squad_filtered['Winger - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Sta', 'Wor'}, {'Cro', 'Dri', 'Tec', 'Agi'}, {'Fir', 'Pas', 'Ant', 'Fla', 'OtB', 'Bal'})
        squad_filtered['Adv Forward - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Dri', 'Fir', 'Tec', 'Cmp', 'OtB'}, {'Pas', 'Ant', 'Dec', 'Wor', 'Agi', 'Bal', 'Sta'})
        squad_filtered['Compl Forward - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Dri', 'Fir', 'Hea', 'Lon', 'Pas', 'Tec', 'Ant', 'Cmp', 'Dec', 'OtB', 'Vis', 'Agi', 'Str'}, {'Tea', 'Wor', 'Bal', 'Jum', 'Sta'})
        squad_filtered['Compl Forward - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Dri', 'Fir', 'Hea', 'Tec', 'Ant', 'Cmp', 'OtB', 'Agi', 'Str'}, {'Lon', 'Pas', 'Dec', 'Tea', 'Vis', 'Wor', 'Bal', 'Jum', 'Sta'})
        squad_filtered['Deep Lying Forw - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea'}, {'Ant', 'Fla', 'Vis', 'Bal', 'Str'})
        squad_filtered['Deep Lying Forw - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Tea'}, {'Dri', 'Ant', 'Fla', 'Vis', 'Bal', 'Str'})
        squad_filtered['False 9 - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'OtB', 'Vis', 'Agi'}, {'Ant', 'Fla', 'Tea', 'Bal'})
        squad_filtered['Poacher - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Ant', 'Cmp', 'OtB'}, {'Fir', 'Hea', 'Tec', 'Dec'})
        squad_filtered['Pressing Forw - Defend'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Agg', 'Ant', 'Bra', 'Dec', 'Tea', 'Wor', 'Sta'}, {'Fir', 'Cmp', 'Cnt', 'Agi', 'Bal', 'Str'})
        squad_filtered['Pressing Forw - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Agg', 'Ant', 'Bra', 'Dec', 'Tea', 'Wor', 'Sta'}, {'Fir', 'Pas', 'Cmp', 'Cnt', 'OtB', 'Agi', 'Bal', 'Str'})
        squad_filtered['Pressing Forw - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Agg', 'Ant', 'Bra', 'OtB', 'Tea', 'Wor', 'Sta'}, {'Fir', 'Cmp', 'Cnt', 'Dec', 'Agi', 'Bal', 'Str'})
        squad_filtered['Tgt Forw - Support'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Hea', 'Bra', 'Tea', 'Bal', 'Jum', 'Str'}, {'Fir', 'Agg', 'Ant', 'Cmp', 'Dec', 'OtB'})
        squad_filtered['Tgt Forw - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Hea', 'Bra', 'Cmp', 'OtB', 'Bal', 'Jum', 'Str'}, {'Fir', 'Agg', 'Ant', 'Dec', 'Tea'})
        squad_filtered['Trequarista - Attack'] = calculate_position_value(squad_filtered, {'Acc', 'Pac', 'Fin'}, {'Dri', 'Fir', 'Pas', 'Tec', 'Cmp', 'Dec', 'Fla', 'OtB', 'Vis'}, {'Ant', 'Agi', 'Bal'})

        content = generate_html(squad_filtered)
        write_output_file(append_date_time_to_filename(file_path), content)

    except ValueError as e:
        print(e)
