#! /usr/env/python

import os, re, errno
from multiprocessing import Pool
from glob import glob

# Argument parser for user-inputted values, and a nifty help menu
from argparse import ArgumentParser

#Parser for arguments
parser = ArgumentParser(description='Combine fastq files from separate Illumina MiSeq runs')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.01')
parser.add_argument('-p', '--path', required=True, help='Specify your HDD01/MiSeqData path. '
                    'Should be something like /mnt/HDD01/MiSeqData or /media/HDD01/MiSeqData')
parser.add_argument('-d', '--destinationPath', required=True, help='Specify the destination for your merged fastq files')
parser.add_argument('-f1', '--folderOne', required=True, help='The name of the first run e.g. 150324_M02516_0002_000000000-AEHCF')
parser.add_argument('-f2', '--folderTwo', required=True, help='The name of the first run e.g. 150327_M02516_0003_000000000-AEGLL')

# Get the arguments into a list
args = vars(parser.parse_args())

# Define variables from the arguments - there may be a more streamlined way to do this
path = args['path']
destination = args['destinationPath']
folderOne = args['folderOne']
folderTwo = args['folderTwo']

# As there is a set folder hierarchy, combine everything here to keep the rest of the script looking pretty
directoryOne = "%s/%s/Data/Intensities/BaseCalls" % (path, folderOne)
directoryTwo = "%s/%s/Data/Intensities/BaseCalls" % (path, folderTwo)
# Get the directories into a list for ease of use
directoryList = [directoryOne, directoryTwo]


def make_path(inPath):
    """from: http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary \
    does what is indicated by the URL"""
    try:
        os.makedirs(inPath)
        os.chmod(inPath, 0775)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Make the destination folder if required
make_path(destination)


def fastqList():
    """Combines two fastq files with matching names in different MiSeq runs into a single fastq file"""
    # A set only contains unique entries, so any duplicate names are automatically screened out
    fastqTrimmed = set()
    # Get the paths and folders into two handy variable
    os.chdir(directoryOne)
    fastqNames = glob("*.fastq.gz")
    for fastq in fastqNames:
        # Undetermined .fastq files are useless to us now, so they are ignored
        if not 'Undetermined' in fastq:
            # The name preceeds the "_R1_001.fastq" portion of the file name
            # Add the name to the set
            fastqTrimmed.add(fastq.split("_R")[0])
    return sorted(fastqTrimmed)


def mergeFastqPrepProcesses(sampleName, directoryList, readNumber):
    """A helper function to make a pool of processes to allow for a multi-processed approach to error correction"""
    fastqPrepArgs = []
    if __name__ == '__main__':
        createFastqPool = Pool()
        # Prepare a tuple of the arguments (strainName and path)
        for name in sampleName:
            fastqPrepArgs.append((name, directoryList, readNumber))
        # This map function allows for multi-processing
        createFastqPool.map(mergeFastq, fastqPrepArgs)


def mergeFastq((name, directoryList, readNumber)):
    """Renames the strains, and combines .fastq.gz files"""
    # Perform the same steps for both the forward and reverse reads (1 and 2, respectively)
    for number in readNumber:
        # The pipeline currently has an issue with sample names that are integers (e.g. 920)
        # This adds an "a" to the end of the name
        stringName = name.split("_S")[0] + "a_S" + name.split("_S")[1]
        # Ensures that the files exist before attempting to manipulate them
        if os.path.isfile("%s/%s_R%s_001.fastq.gz" % (directoryList[0], name, number)) \
                and os.path.isfile("%s/%s_R%s_001.fastq.gz" % (directoryList[1], name, number)):
            # Read the two fastq files in the separate directories using cat and output the data into a single file
            # with the corrected stringName in your destination folder.
            systemCommand = "cat %s/%s_R%s_001.fastq.gz %s/%s_R%s_001.fastq.gz > %s/%s_R%s_001.fastq.gz" \
                            % (directoryList[0], name, number, directoryList[1], name, number, destination, stringName, number)
            print systemCommand
            os.system(systemCommand)

# Paired-end reads are numbered 1 and 2 - when combining fastq.gz files, these must be treated separately
readNumber = [1, 2]

# Get the list of the names of the files
fastqTrimmed = fastqList()
# Merge the files into the destination folder
mergeFastqPrepProcesses(fastqTrimmed, directoryList, readNumber)


