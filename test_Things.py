# Imports
import numpy as np
import pandas as pd
from pprint import pprint
import pytest
import VideoMetadata as vm
import EncodingSpeed as es


# Fixtures
@pytest.fixture
def example_videos():
    videos = [
        r'A:\Primary\Other\Code\Software_Projects\VideoMetadataDumper\vids\00001.MTS'
        r'A:\Primary\Other\Code\Software_Projects\VideoMetadataDumper\vids\1m L.mp4'
        r'A:\Primary\Other\Code\Software_Projects\VideoMetadataDumper\vids\A480_001.AVI'
        r'A:\Primary\Other\Code\Software_Projects\VideoMetadataDumper\vids\A480_merged.mp4'
        r'A:\Primary\Other\Code\Software_Projects\VideoMetadataDumper\vids\Dashcam_seg.MOV'
        r'A:\Primary\Other\Code\Software_Projects\VideoMetadataDumper\vids\DCR m.mp4'
        r'A:\Primary\Other\Code\Software_Projects\VideoMetadataDumper\vids\Note-9_.mp4'
        r'A:\Primary\Other\Code\Software_Projects\VideoMetadataDumper\vids\R600_00005.mp4'
        r'A:\Primary\Other\Code\Software_Projects\VideoMetadataDumper\vids\Rec 0002.ts'
        r'A:\Primary\Other\Code\Software_Projects\VideoMetadataDumper\vids\SX44.MPG'
    ]
    return videos

# Tests
def test_add_dummy_columns():
    data = {
        'Col1': ['data', 'data'],
        'Col2': ['data', 'data'],
        'Col3': ['data', 'data'],
    }
    data_dummy2 = {
        'D1': [np.nan, np.nan], 
        'Col1': ['data', 'data'],
        'D2': [np.nan, np.nan], 
        'D3': [np.nan, np.nan], 
        'Col2': ['data', 'data'],
        'D4': [np.nan, np.nan], 
        'Col3': ['data', 'data'],
    }
    expected_dummy = pd.DataFrame(data=data_dummy2)
    
    df = pd.DataFrame(data)
    df_dummy = vm.add_dummy_columns(df, insert_at=(0, 1, 1, -1))
    #pprint(df_dummy)
    #pprint(expected_dummy)
    assert all(df_dummy == expected_dummy)

