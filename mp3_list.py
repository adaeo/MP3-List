#!/usr/bin/env python

## Import Modules ## 
import pandas as pd 
import eyed3
import sys, glob, os

import settings
from utility import optdict, audio_ext, sepdict

## Define Classes ##

# DTF Object type
class ListFile:
    def __init__(self, name, ext):
        self.name = name
        self.ext = ext


## Define Functions ##

# Extract audio metadata and return it in a pandas dataframe
def get_audio_data(audio_files):

    try:
        audio_df = pd.DataFrame(columns=['title', 'artist', 'file'])

        total = len(audio_files)
        iteration = 0
        sys.stdout.write("Audio files parsed: 0/{}".format(total))

        for file in audio_files:
            # Load audio file using absolute path and eyeD3
            a_file = eyed3.load("{path}/{file}".format(
                path = settings.dir_PATH, file = file))
            audio_df = audio_df.append(
                {'title':a_file.tag.title, 'artist':a_file.tag.artist, 'file':file}, ignore_index=True)
            # Update progress
            iteration += 1
            sys.stdout.write('\r')
            sys.stdout.write("Audio files parsed: {}/{}".format(iteration, total))
        
        print('\nComplete!')
        return audio_df

    except:
         print("Something went wrong: get_audio_data()")

# Evaluate dataframes and produce outputs
def evaluate_df(dtf_df, a_df, ext):
    try: 
        # Find intersection on both title and artist fields
        int_df = pd.merge(dtf_df, a_df, how='inner', on=['title','artist'])
        # Find difference between initial dtf_df and new int_df
        dif_dtf_df = pd.concat([dtf_df, int_df]).drop_duplicates(subset=['title', 'artist'], keep=False)
        
        # Compare DTF file and locate missing audio files
        if dif_dtf_df.shape[0] == 0: # If no missing entries
            print("All audio files in DTF were found.")
        else: # If missing entries exist
            print("{}/{} audio files were missing from DTF.".format(dif_dtf_df.shape[0], dtf_df.shape[0]))
            dtf_ans = input("Print missing audio files to DTF file? y/n\n")
            if dtf_ans.lower() == 'y':
                # Output missing entries to DTF file of original file type
                dif_dtf_df.to_csv('missing.{}'.format(ext), sep=sepdict[ext])
                print("missing.{} was saved to {}".format(ext, settings.dir_PATH))   

        # Find difference between initial a_df and new int_df
        dif_a_df = pd.concat([a_df, int_df]).drop_duplicates(subset=['title', 'artist'], keep=False)
        # Identify audio files not present in DTF file
        if dif_a_df.shape[0] == 0: # If no non-matching audio files
            print("No audio files were found that did not match an entry in DTF.")
        else:
            print("{} audio files were found that did not match any entry in DTF".format(dif_a_df.shape[0]))
            a_ans = input("Print unmatched audio files to DTF file? y/n\n")
            if a_ans.lower() == 'y':
                # Output extra audio files to DTF file of original file type
                dif_a_df.to_csv('extra.{}'.format(ext), sep=sepdict[ext])
                print("extra.{} was saved to {}".format(ext, settings.dir_PATH)) 
    except:
        print("Something went wrong: evaluate_df()")

    # ! Last edit here ! #

# Initial function run when program is called through terminal
def initial():

    # Clean up warnings
    eyed3.log.setLevel("ERROR")

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
            dtf_df = pd.read_csv(dtf_arg, header=None, sep=sepdict[dtf.ext], skiprows=settings.skip)
            dtf_df = dtf_df.rename(columns={0:"title", 1:"artist"})
        except FileNotFoundError:
            # Stop program if file does not exist
            error_msg = "File \"{0}\" does not exist!".format(dtf_arg)
            raise SystemExit(error_msg)
        
        try: 
            # Try locate Directory 
            settings.dir_PATH = os.path.abspath(dir_arg) # Set global absolute PATH for directory
            os.chdir(dir_arg) # Change directory
            audio_files = []
            for files in audio_ext:
                # Appends all files to audio_files array that match *.ext_type from utility.audio_ext
                audio_files.extend(glob.glob(files)) 

            # If any audio files are appended, run get_audio_data function
            if bool(audio_files):
                audio_df = get_audio_data(audio_files)
            else:
                error_msg = "No suitable audio files found in directory."
                raise SystemExit(error_msg)
                # Stop if directory is invalid
            
            # Run evaluation function on both dataframes
            evaluate_df(dtf_df, audio_df, dtf.ext)

        except FileNotFoundError:
            error_msg = "Directory \"{0}\" does not exist!".format(dir_arg)
            raise SystemExit(error_msg)

    else:
        # Stop program if args are not at least 2
        print("\nAt least two arguments required!")
        print("Required:\n- Delimeted-Text File: \"PATH\\file.ext\"")
        print("- Audio Directory: \"PATH\\dir\"\n")
        print(" Use -h for help with optional flags. \n")
        raise SystemExit

# Process
initial()