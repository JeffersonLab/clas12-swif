#!/usr/bin/env python

##########################################################################################################################
#
# 2017/02/7 Vardan Gyurjyan
# Based on work by Paul Mattione (HallD)
#
# SWIF DOCUMENTATION:
# https://scicomp.jlab.org/docs/swif
# https://scicomp.jlab.org/docs/swif-cli
#
##########################################################################################################################

from optparse import OptionParser
import os.path
import sys
import re
import subprocess
import glob

#################################################### GLOBAL VARIABLES ####################################################

# DEBUG
VERBOSE = False

# PROJECT INFO
PROJECT = "clas12"  # http://scicomp.jlab.org/scicomp/projects
TRACK = "reconstruction"  # https://scicomp.jlab.org/docs/batch_job_tracks

# RESOURCES
NCORES = "1"  # Number of CPU cores
DISK = "6GB"  # Max Disk usage
RAM = "6GB"  # Max RAM usage
TIMELIMIT = "300minutes"  # Max walltime
OS = "centos7"  # Specify CentOS65 machines

# SOURCE DATA INFORMATION
RUN_PERIOD = "2018-01"
VERSION = "5a.019"
DATA_SOURCE_TYPE = "mss"  # "mss tape" or "file disk"
DATA_SOURCE_BASE_DIR = "/mss/clas12/er-a/data/"

# OUTPUT DATA LOCATION
DATA_OUTPUT_BASE_DIR = "/volatile/clas12/data/pass0/decoded/"

# JOB EXECUTION
SCRIPTFILE = "$CLARA_HOME/bin/clas12-decoder.sh"

####################################################### FIND FILES #######################################################

def find_files(DATA_SOURCE_DIR, RUN):
    # CHANGE TO THE DIRECTORY CONTAINING THE INPUT FILES
    current_dir = os.getcwd()
    os.chdir(DATA_SOURCE_DIR)

    # SEARCH FOR THE FILES
    file_signature = "clas_*.evio.*"
    file_list = glob.glob(file_signature)
    if (VERBOSE == True):
        print "size of file_list is " + str(len(file_list))

    # CHANGE BACK TO THE PREVIOUS DIRECTORY
    os.chdir(current_dir)
    return file_list


######################################################## ADD JOB #########################################################

def add_job(WORKFLOW, DATA_SOURCE_DIR, INFILENAME, OUTFILENAME, RUNNO, FILENO):
    # PREPARE NAMES
    STUBNAME = RUNNO + "_" + FILENO
    JOBNAME = WORKFLOW + "_" + STUBNAME

    # CREATE ADD-JOB COMMAND
    # job
    add_command = "swif add-job -workflow " + WORKFLOW + " -name " + JOBNAME
    # project/track
    add_command += " -project " + PROJECT + " -track " + TRACK
    # resources
    add_command += " -cores " + NCORES + " -disk " + DISK + " -ram " + RAM + " -time " + TIMELIMIT + " -os " + OS
    # inputs
    add_command += " -input " + INFILENAME + " " + DATA_SOURCE_TYPE + ":" + DATA_SOURCE_DIR + "/" + INFILENAME
    # tags
    add_command += " -tag run_number " + RUNNO
    # tags
    add_command += " -tag file_number " + FILENO
    # command
    add_command += " " + SCRIPTFILE + " " + DATA_SOURCE_DIR+INFILENAME + " " + DATA_OUTPUT_BASE_DIR+OUTFILENAME

    if (VERBOSE == True):
        print "job add command is \n" + str(add_command)

    # ADD JOB
    status = subprocess.call(add_command.split(" "))


########################################################## MAIN ##########################################################

def main(argv):
    parser_usage = "swif_clas12-decoder.py workflow minrun maxrun"
    parser = OptionParser(usage=parser_usage)
    (options, args) = parser.parse_args(argv)

    if (len(args) != 3):
        parser.print_help()
        return

    # GET ARGUMENTS
    WORKFLOW = args[0]
    MINRUN = int(args[1])
    MAXRUN = int(args[2])

    # CREATE WORKFLOW
    status = subprocess.call(["swif", "create", "-workflow", WORKFLOW])


    # FIND/ADD JOBS
    for RUN in range(MINRUN, MAXRUN + 1):

        # Format run and file numbers
        FORMATTED_RUN = "%06d" % RUN

        # Find files for run number
        file_list = ""
        if (os.path.exists(DATA_SOURCE_BASE_DIR)):
            file_list = find_files(DATA_SOURCE_BASE_DIR, FORMATTED_RUN)
        else:
            continue

        if (len(file_list) == 0):
            continue

        # Add jobs to workflow
        for FILENAME in file_list:
            FILENO = FILENAME.split(".")[2]  # e.g. clas_002999.evio.11
            OFILENAME = FILENAME.split(".")[0]+".hipo"

            add_job(WORKFLOW, DATA_SOURCE_BASE_DIR, FILENAME, OFILENAME, FORMATTED_RUN, FILENO)


if __name__ == "__main__":
    main(sys.argv[1:])
