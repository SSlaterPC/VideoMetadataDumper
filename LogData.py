# Description
'''
Author: Steven Slater
Date: 2025-11-02
Description: Description: Output a CSV of certain data from HandBrake video encoding logs.

'''


# Imports
import numpy as np
import os
import pandas as pd
from pprint import pprint
from re import search
import VideoMetadata as vm
import EncodingSpeed as es

# Constants
MAX_AUDIO_STREAMS = 5   # number of audio bitrate columns in benchmark spreadsheet

# Functions
def get_combined_metadata(logs: list[str]) -> list[pd.DataFrame]:
    ''''''
    df_videos = get_logged_filepaths(logs)
    src = vm.create_metadata_table(videos=df_videos['Source'])
    dest = vm.create_metadata_table(videos=df_videos['Destination'])
    logd = es.get_log_data(logs)

    # rename columns
    audio_count_src = len([col for col in src.columns if col.startswith('Arate')])
    audio_count_dest = len([col for col in dest.columns if col.startswith('Arate')])
    column_names_src = {
        'Name': 'SFilename',
        'Extension': 'SExt',
        'Codec': 'SCodec',
        'EncProfile': 'SProf',
        'EncLevel': 'SLv',
        'FPS': 'SFPS',
        'Len': 'Slen_s',
        'Frames': 'Slen_f',
        'Res': 'SRes',
        'SizeKB': 'SsizeKB',
        'Vrate': 'SV-BR',
    }
    for i in range(1, audio_count_src + 1):
        column_names_src[f'Arate{i}'] = f'SA{i}'
    src = src.rename(columns=column_names_src)

    # Only the columns we need
    dest2 = dest.drop(['DateCreated', 'DateModified'], axis=1)
    logd2 = logd[['RF', 'Preset', 'Speed', 'Encoder']]
    combined = pd.concat([src, logd2, dest2], axis=1)

    # empty columns that reduces number of manual copypaste operations
    # this will change every time I move a spreadsheet column
    dummies = [
        [12]*3,
        [14]*(4 + MAX_AUDIO_STREAMS - audio_count_src),
        [28]*5
    ]
    dummy_cols = []
    for d in dummies:
        dummy_cols += d
    padded = vm.add_dummy_columns(combined, insert_at=dummy_cols)
    return padded

def get_logged_filepaths(logs: list[str]) -> list[pd.DataFrame]:
    ''''''
    r_encode = r'encode_(\d{2})\.(\d{2})\.(\d{4}) (\d{2})-(\d{2})-(\d{2})\.txt'
    r_source = r'"Path": "(.*)",'
    r_dest = r'"File": "(.*)",'
    dfs = []
    for log in logs:
        file_content = ''
        with open(log, 'r') as f:
            file_content = f.read()
        e_grp = search(pattern=r_encode, string=os.path.basename(log)).groups()
        encode = f'{e_grp[2]}-{e_grp[0]}-{e_grp[1]} {e_grp[3]}:{e_grp[4]}:{e_grp[5]}'
        source = search(pattern=r_source, string=file_content).group(1)
        dest = search(pattern=r_dest, string=file_content).group(1)
        meta_d = {
            'Encode': [encode],
            'Source': [source],       # TODO: reuse these paths to get video metadata
            'Destination': [dest],
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
        intro = vm.Text('-------\nWelcome to the Handbrake Log Data Extractor!' \
        '\nThis outputs a CSV of certain data from HandBrake video encoding logs.')
        intro.show()

        # get path to logs from Handbrake installation settings?
        starting_dir = r'C:\Users\Cobalt Storm\AppData\Roaming\HandBrake\logs'
        logs = es.get_logs(starting_dir)
        if not logs:
            print('Cancelled.')
            print('Exited.')
            return

        df = get_combined_metadata(logs)
        pprint(df)
        df.to_csv(f'output.csv')
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
