# This is a module responsible for storing utility functions, dictionaries and other variables
import settings

# Functions 
def help_msg():
    print('Optional Flags:')
    print("\t-sk: skips first row of dtf")
    print("\t-etc.\n")

def skip_row():
    settings.skip = 1

# Dictionary containing dtf extensions for separator arg in pandas.read_csv
sepdict = {
    "csv": ', ',
    "tsv": '\t',
    "psv": '|'
}

# Tuple containing audio extensions supported by mp3_list
audio_ext = ('*.mp3', '*.wav')

# Dictionary containing optional system arguments when mp3-list is called
optdict = {
    '-h': help_msg,
    '-sk': skip_row
}

