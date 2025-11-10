# Imports
import pandas as pd
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
def test_test():
    assert True

