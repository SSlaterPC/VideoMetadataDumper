# Description
'''
Author: Steven Slater
Date: 2025-11-02
Description: Output a CSV of metadata (source, destination, and encoding speed) from Handbrake logs.

'''

# Imports
import cProfile
import numpy as np
import os
import pandas as pd
from pprint import pprint
import pstats
import re
from re import search, findall
import tkinter as tk
import tkinter.filedialog as fd
from VideoMetadata import Text






# Functions
def get_logs(starting_dir: str, show=True):
    ''''''
    root = tk.Tk()
    root.withdraw()
    logs = fd.askopenfilenames(parent=root, title='Select Handbrake Encoding Logs',
                                filetypes=[('Handbrake Encoding Logs', '.txt')],
                                initialdir=starting_dir)
    if show:
        pprint([os.path.basename(log) for log in logs])
    return logs

def get_log_data(logs: list[str]) -> list[pd.DataFrame]:
    ''''''
    r_encode = r'encode_(\d{2})\.(\d{2})\.(\d{4}) (\d{2})-(\d{2})-(\d{2})\.txt'
    r_source = r'"Path": "(.*)",'
    r_dest = r'"File": "(.*)",'
    r_encoder = r'"Video": {\n    "Encoder": "(.*)",'
    r_preset = r'"Preset": "(.*)",'
    r_RF = r'"Quality": (.*),'
    r_speed = r'work: average encoding speed for job is (.*) fps'
    dfs = []
    for log in logs:
        file_content = ''
        with open(log, 'r') as f:
            file_content = f.read()
        e_grp = search(pattern=r_encode, string=os.path.basename(log)).groups()
        encode = f'{e_grp[2]}-{e_grp[0]}-{e_grp[1]} {e_grp[3]}:{e_grp[4]}:{e_grp[5]}'
        source = search(pattern=r_source, string=file_content).group(1)
        dest = search(pattern=r_dest, string=file_content).group(1)
        encoder = search(pattern=r_encoder, string=file_content).group(1)
        preset = search(pattern=r_preset, string=file_content).group(1)
        qualRF = search(pattern=r_RF, string=file_content).group(1)
        speed = search(pattern=r_speed, string=file_content).group(1)
        meta_d = {
            'Encode': [encode],
            'Source': [os.path.basename(source)],       # TODO: reuse these paths to get video metadata
            'Destination': [os.path.basename(dest)],
            'RF': [qualRF],
            'Preset': [preset],
            'Speed': [int(round(float(speed), 0))],
            'Encoder': [encoder],
        }
        df = pd.DataFrame(meta_d)
        dfs.append(df)
    dfm = pd.concat(dfs).reset_index(drop=True)
    # sort by encode timestamp
    dfm = dfm.sort_values('Encode').reset_index(drop=True)
    return dfm

# Run
def main():
    try:
        intro = Text('-------\nWelcome to the Handbrake Metadata Dumper!' \
        '\nThis outputs a CSV of metadata (source, destination, and encoding speed) from Handbrake logs.')
        intro.show()

        # get path to logs from Handbrake installation settings?
        starting_dir = r'C:\Users\Cobalt Storm\AppData\Roaming\HandBrake\logs'
        logs = get_logs(starting_dir)
        if not logs:
            print('Cancelled.')
            print('Exited.')
            return

        metadata_table = get_log_data(logs)
        print(metadata_table)

        metadata_table.to_csv(f'output_encspeed.csv')
        print('Created CSV.')


    except Exception as e:
        print(e)
        raise(e)
        #time.sleep(2)

    # allow user to read message
    print('Exited.')
    #time.sleep(1)
    return


if __name__ == '__main__':
    # profiler = cProfile.Profile()
    # profiler.enable()

    main()

    # profiler.disable()
    # stats = pstats.Stats(profiler)
    # stats.sort_stats(pstats.SortKey.CUMULATIVE)
    # stats.print_stats(3)
