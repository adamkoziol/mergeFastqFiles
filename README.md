# mergeFastqFiles README

This script merges .fastq.gz files from separate Illumina MiSeq runs as long as the files are in the same order. 
For instance, 498_S1_L001_R1_001.fastq and 498_S1_L001_R1_001.fastq are the same, but 498_S1_L001_R1_001.fastq and 498_S5_L001_R1_001.fastq are different

Here is an example of how to run the script:

`python mergeFastqFiles.py -p /media/nas/backup/MiSeq/MiSeqOutput -d /media/nas/akoziol/fastqmergetest -f1 140814_M02466_0023_000000000-AAF1M -f2 140818_M02466_0024_000000000-A78YN`

-p is the path of the folder, which contains the folders with the sequence data from the runs e.g. /media/HDD01/MiSeqData

-d is the path of the destination folder that will contain your merged .fastq.gz files

-f1 and -f2 are the folders containing the sequence data