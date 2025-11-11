# Description
'''
Author: Steven Slater
Date: 2025-11-02
Description: Output a CSV of metadata from selected video file(s).

'''

# Imports
from copy import deepcopy
import cProfile
import datetime
import ffmpeg
from fractions import Fraction
import numpy as np
import os
import pandas as pd
from pprint import pprint
import pstats
import time
import tkinter as tk
import tkinter.filedialog as fd


# Constants
MAX_AUDIO_STREAMS = 5   # number of audio bitrate columns in benchmark spreadsheet


# Classes
class Text:
    ''''''
    def __init__(self, body_text=''):
        self.body_text = body_text
        return

    def show(self):
        print(self.body_text)
        return

class Menu:
    ''''''
    def __init__(self, options=None):
        self.options = options if options is not None else {}
        return
    
    def activate(self, choice: str):
        print(f'activated {choice}')
        return

class VideosList:
    ''''''
    def __init__(self, videos=None):
        self.videos = videos if videos is not None else []
        self.metadata = MetadataTable()
        return

    def select_videos(self) -> list[str]:
        # open file dialog with multiselect

        # insert basenames of selected files into list
        vids = []
        return vids

    def create_table(self) -> pd.DataFrame:
        # run ffmpeg to get metadata

        # choose metadata


        table = pd.DataFrame()
        return table

class MetadataTable:
    ''''''
    def __init__(self, table=None):
        self.table = pd.DataFrame(table) if table is not None else pd.DataFrame({})
        return
    
    def add(self, records: dict):
        pd.concat(self.table, pd.DataFrame(records))
        return


# Functions
def get_videos(starting_dir: str, show=True):
    ''''''
    root = tk.Tk()
    root.withdraw()
    #videos = fd.askopenfilenames(parent=root, title='Select Video Files', filetypes=[('Video files', '*.mp4')])
    video_exts = '.mp4 .mpg .avi .mov .ts .mts .vob .wmv .webm'
    videos = fd.askopenfilenames(parent=root, title='Select Video Files', initialdir=starting_dir,
                                 filetypes=[('Video files', video_exts)])
    if show:
        pprint([os.path.basename(video) for video in videos])
    return videos

def get_metadata(videos: list[str]) -> list[pd.DataFrame]:
    ''''''
    dfs = []
    audio_count = 0
    for video in videos:
        meta = ffmpeg.probe(video)
        basename_ = os.path.basename(meta['format']['filename'])
        date_created = datetime.datetime.fromtimestamp(os.stat(video).st_birthtime)
        date_modified = datetime.datetime.fromtimestamp(os.stat(video).st_mtime)
        #data_rate = os.stat(video).st_file_attributes
        #pprint(data_rate)
        #pprint(meta)

        metav = None
        for i, stream in enumerate(meta['streams']):
            if stream['codec_type'] == 'audio':
                pass
            elif stream['codec_type'] == 'video':
                metav = meta['streams'][i]
                break
            else:
                print(f"codec_type: {stream['codec_type']}")

        relevant_meta = {
            'DateCreated': date_created,
            'DateModified': date_modified,
            'Name': [basename_],
            'Extension': [os.path.splitext(meta['format']['filename'])[1][1:]],
            'Codec': [metav['codec_name']],
            'EncProfile': [metav['profile']],
            'EncLevel': [int(metav['level'])],
            'FPS': [round(float(Fraction(metav['r_frame_rate'])), 2)],     # was eval(), oof
            'Len': [float(metav['duration'])],
            'Res': [f"{metav['width']}x{metav['height']}"],
            'SizeKB': [float(meta['format']['size']) / 1024],   # Bytes to KB
            }

        try:     # N/A for MPEG-1 and MPEG-TS
            mpg_meta = {'Vrate': [int(metav['bit_rate'])],
                        'Frames': [int(metav['nb_frames'])]}
        except KeyError:
            #print(f'MPEG-1 or MPEG-TS means video bitrate and nb_frames are N/A')
            mpg_meta = {'Vrate': [np.nan],
                        'Frames': [np.nan]}

        # skip tracks that don't exist
        audio_bitrates = {}
        i = 0
        total_audio = 0
        for stream in meta['streams']:
            if stream['codec_type'] == 'audio':
                if i < MAX_AUDIO_STREAMS:
                    i += 1
                    audio_bitrates[f'Arate{i}'] = [int(stream['bit_rate'])]
                # sum all audio bitrates
                total_audio += int(stream['bit_rate'])


        # max audio streams
        if audio_count < i:
            audio_count = i
        
        rm = relevant_meta | mpg_meta | audio_bitrates
        df = pd.DataFrame(rm)   # length is 1, because it is one record

        # For MPEG and MPEG-TS, calc missing values
        df['TotalAudio'] = total_audio
        if len(df['Vrate'].isna()) > 0:
            df['Vrate'] = (df['SizeKB']*1024*8 / df['Len'] - df['TotalAudio']).round(0).astype(int)
        if len(df['Frames'].isna()) > 0:
            df['Frames'] = (df['Len'] * df['FPS']).round(0).astype(int)

        df['SizeKB'] = df['SizeKB'].round(3)
        dfs.append(df)

    return dfs, audio_count

def reorder_columns(columns: list[str], audio_count: int):
    ''''''
    for j in range(1, audio_count + 1):
        columns += [f'Arate{j}']
    columns += ['TotalAudio']
    return columns

def add_dummy_columns_old(df: pd.DataFrame, insert_at: list[str]) -> pd.DataFrame:
    '''Return a dataframe copy with extra empty columns added.
    'insert_at' are the indices of the input dataframe where you want to add a column.
    Repeat the same index for multiple dummy columns in the same spot.'''
    dfd = deepcopy(df)

    # get OG column labels
    colnames = []
    for i in insert_at:
        colnames.append(df.columns[i])

    # insert columns
    dnum = 1
    for name in colnames:
        col_loc = dfd.columns.get_loc(name)
        while f'D{dnum}' in dfd.columns:    # for combining multiple dataframes that already have dummy columns
            dnum += 1
        dfd.insert(loc=col_loc, column=f'D{dnum}', value=None)
        dnum += 1

    return dfd

def add_dummy_columns(df: pd.DataFrame, insert_at_names: dict[str: int]) -> pd.DataFrame:
    '''Return a dataframe copy with extra empty columns added.
    'insert_at_name' are the column names of the input dataframe where you want to add a column.
    It takes the format {'column name': amount of dummy columns to insert}.'''
    dfd = deepcopy(df)
    dnum = 1
    for dname, amount in zip(insert_at_names, insert_at_names.values()):
        dloc = dfd.columns.get_loc(dname)
        for i in range(amount):
            while f'D{dnum}' in dfd.columns:    # avoid duplicate cols
                dnum += 1
            dfd.insert(loc=dloc, column=f'D{dnum}', value=None)
        dnum += 1
    return dfd

def organize_df(metadata_df: pd.DataFrame, audio_count: int, insert_dummy_col_at=[]) -> pd.DataFrame:
    ''''''
    columns = ['DateCreated', 
                'DateModified', 
                'Name', 
                'Extension', 
                'Codec', 
                'EncProfile', 
                'EncLevel',
                'FPS', 
                'Len', 
                'Frames', 
                'Res', 
                'SizeKB', 
                'Vrate']
    cols = reorder_columns(columns=columns, audio_count=audio_count)
    mtable = metadata_df[cols]
    mtable = add_dummy_columns_old(df=mtable, insert_at=insert_dummy_col_at)
    return mtable

def create_metadata_table(videos: list[str], insert_dummy_col_at=[]) -> pd.DataFrame:
    ''''''
    dfs, audio_count = get_metadata(videos=videos)
    df = pd.concat(dfs).reset_index(drop=True)
    df = organize_df(df, audio_count, insert_dummy_col_at)
    return df


# Run
def main():
    basename_ = ''
    try:
        intro = Text('-------\nWelcome to the Video Metadata Dumper!' \
        '\nThis outputs the chosen metadata of selected video files into a CSV.')
        intro.show()

        starting_dir = r'A:\Videos\Editing Exports\Handbrake'
        videos = get_videos(starting_dir=starting_dir)
        if not videos:
            print('Cancelled.')
            print('Exited.')
            return

        mtable = create_metadata_table(videos, insert_dummy_col_at=[12, 12, 12])
        print(mtable.columns)
        pprint(mtable)
        mtable.to_csv(f'output.csv')
        print('Created CSV.')

    except Exception as e:
        print(e)
        print(f'Filename: {basename_}')
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
