### This project is no longer being updated as of 07/03/2022

# MP3-List
Compare a delimited-text file containing song details with a directory of audio files using metadata obtained using eyeD3 module. Optionally, output missing entries and/or unmatched audio files in DTF files.

# Supported list types
<ul>
<li>CSV</li>
<li>TSV</li>
<li>PSV</li>
</ul>

# Supported audio types
<ul>
<li>mp3</li>
<li>wav</li>
</ul>

# Usage

Ensure your current path is within the directory containing mp3_list.py

## Parameters
arg 1: Delimited Text File DTF (file containing your list of audio)<br>
arg 2: Directory (directory containing your audio)<br>
Optional flags:<br>
<ul>
<li>-h: help for optional flags. (can use without arg1 and arg2)</li>
<li>-sk: skip first row in your DTF.</li> 
</ul>

e.g. 
>".\mp3_list.py songs.csv G:\Music\Pop"

## Output
### Missing Entries
Entries in your DTF file that do not find matching audio files in your provided directory can be output as a separate DTF file (same extension type as input). 

Output as: 

>[PROVIDED_AUDIO_DIRECTORY]/missing.[ORIGINAL_EXTENSION]

e.g. 

>my_audio/missing.csv


### Unmatched Audio
Audio files in your provided directory that aren't matched with your any entries in your provided DTF file can be output as a separate DTF file (same extension type as input).

Output as: 

>[PROVIDED_AUDIO_DIRECTORY]/extra.[ORIGINAL_EXTENSION]

e.g. 

>my_audio/extra.csv
