## Import Modules ## 
import pandas as pd
import sys, glob, os

import settings as s
from utility import optdict, audio_ext, sepdict



## Define Classes ##

# DTF Object type
class ListFile:
    def __init__(self, name, ext):
        self.name = name
        self.ext = ext


## Define Functions ##

# Function run when program is called through terminal
def initial():
    arg_length = len(sys.argv)

    # Print Help
    if arg_length == 2 and sys.argv[1] == '-h':
        optdict['-h']()

    # Normal Usage
    elif arg_length >= 3:

        # Parse optional flags
        if arg_length > 3:
            optargs = sys.argv[3:arg_length]
            # Run optional flags
            for arg in optargs:
                try:
                    # Run optional flag if it exists in optdict
                    optdict[arg]()
                except KeyError:
                    # Stop program if flag does not exist
                    error_msg = "Invalid flag \"{0}\"".format(arg)
                    raise SystemExit(error_msg)
    
        # Set DTF and DIR arguments. 
        dtf_arg = str(sys.argv[1])
        dir_arg = str(sys.argv[2])

        try:
            # Try split DTF argument string
            split_dtf =  dtf_arg.split(".")
            dtf = ListFile(split_dtf[0], split_dtf[1])
        except IndexError:
            # Stop program if argument is invalid
            error_msg = "Invalid file name \"{0}\"".format(dtf_arg)
            raise SystemExit(error_msg)

        try:
            # Try load DTF into Pandas Dataframe
            dtf_df = pd.read_csv(dtf_arg, header=None, sep=sepdict[dtf.ext], skiprows=s.skip)
        except FileNotFoundError:
            # Stop program if file does not exist
            error_msg = "File \"{0}\" does not exist!".format(dtf_arg)
            raise SystemExit(error_msg)
        
        try: 
            # Try locate Directory 
            os.chdir(dir_arg)
            audio_files = []
            for files in audio_ext:
                audio_files.extend(glob.glob(files))
            
            if bool(audio_files):
                pass
            else:
                error_msg = "No suitable audio files found in directory."
                raise SystemExit(error_msg)
                # Stop if directory is invalid
        except FileNotFoundError:
            error_msg = "Directory \"{0}\" does not exist!".format(dir_arg)
            raise SystemExit(error_msg)

    else:
        # Stop program if args are not at least 2
        print("\nAt least two arguments required!")
        print("Required:\n- Delimeted-Text File: \"PATH\\file.ext\"")
        print("- Audio Directory: \"PATH\\dir\"\n")
        raise SystemExit

# Process
initial()