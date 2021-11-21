## Import Modules ## 
import pandas as pd
import sys, glob, os

import settings as s
from utility import optdict, audio_ext, sepdict



## Define Classes ##

class ListFile:
    def __init__(self, name, ext):
        self.name = name
        self.ext = ext


## Define Functions ##


def initial():
    arg_length = len(sys.argv)

    # Print Help
    if arg_length == 2 and sys.argv[1] == '-h':
        optdict['-h']()

    # Normal Usage
    elif arg_length >= 3:

        if arg_length > 3:
            optargs = sys.argv[3:arg_length]
            
            for arg in optargs:
                optdict[arg]()
    

        dtf_arg = str(sys.argv[1])
        dir_arg = str(sys.argv[2])

        try:
            split_dtf =  dtf_arg.split(".")
            dtf = ListFile(split_dtf[0], split_dtf[1])
        except IndexError:
            error_msg = "Invalid file name \"{0}\"".format(dtf_arg)
            raise SystemExit(error_msg)

        try:
            dtf_df = pd.read_csv(dtf_arg, header=None, sep=sepdict[dtf.ext], skiprows=s.skip)
        except FileNotFoundError:
            error_msg = "File \"{0}\" does not exist!".format(dtf_arg)
            raise SystemExit(error_msg)
        
        try: 
            os.chdir(dir_arg)
            audio_files = []
            for files in audio_ext:
                audio_files.extend(glob.glob(files))
            
            if bool(audio_files):
                pass
            else:
                error_msg = "No suitable audio files found in directory."
                raise SystemExit(error_msg)
        except FileNotFoundError:
            error_msg = "Directory \"{0}\" does not exist!".format(dir_arg)
            raise SystemExit(error_msg)

    else:
        print("\nAt least two arguments required!")
        print("Required:\n- Delimeted-Text File: \"PATH\\file.ext\"")
        print("- Audio Directory: \"PATH\\dir\"\n")
        raise SystemExit

# Process
initial()