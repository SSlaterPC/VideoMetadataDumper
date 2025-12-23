Video Metadata Dumper

Reads handbrake encoding logs, gets the input/output files, then dumps a the following bits of metadata into a .csv file.
For both input and output files:
- Filename
- Extension
- Codec
- Encoding Profile
- Encoding Level
- FPS
- Length in seconds
- Length in frames
- Resolution
- Size in KB
- Video bitrate in bytes
- Audio bitrates of five audio tracks
- Total audio bitrate in bytes

For input files only:
- Date Created
- Date Modified

For output files only:
- RF
- Encoder Preset
- Encoding Speed
- Encoder


It also outputs empty dummy columns to make it easier for me to copypaste into an existing spreadsheet.
