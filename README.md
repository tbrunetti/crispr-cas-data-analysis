
# crispr-cas-data-analysis

The scripts and programs listed in this repository are made to be used for projects using genome-wide sgRNA (CRISPR-cas9) screening assays and analysis.

## sgRNA_representation_vers2.py
-----------------------------
A pipeline to analyze the library complexities of sgRNA screens against a list of targeted sgRNAs.  The user has the ability to feed in a directory of fastq files as input into sgRNA_representation_vers2.py.  It will proceed to align all the reads in each of the libraries against a user generated sgRNA genome.  The aligned reads are then used to calculate the overall complexity of each library and the number of reads representing each target in the genome.  **NOTE:  This pipeline has only been optimized for single-end 70bp and less reads from Illumina TruSeq libraries**

####Requirements
----------------
* chunkypipes (http://chunky-pipes.readthedocs.io/en/stable/getting_started.html)   
* bwa (http://bio-bwa.sourceforge.net/)  
* samtools (http://samtools.sourceforge.net/)  


####Generate sgRNA "genome"
--------------------------  
Before sgRNA_representation_vers2.py can be run, the user must generate and index a custom sgRNA genome using bwa.  All target sgRNAs should be concatenated into a single FASTA file.  This FASTA file will represent your sgRNA-targeted genome.  The generation of a genome only needs to be performed once per genome.  Once the FASTA file has been generated, use BWA to index the genome:

```
./bwa index sgRNA-targeted-genome.fa
```
The index files and the FASTA file should all be located in the same directory.


####Using the Pipeline
----------------------
ChunkyPipes requires that every pipeline be installed and configured before it can be run.  Install and configure sgRNA_representation_vers2.py into ChunkyPipes:

```
chunky install sgRNA_representation_vers2.py
chunky configure sgRNA_representation_vers2.py
``` 
This should prompt the user for some information in regards to the full path to the executable file for BWA and samtools as well as the full path to sgRNA-targeted-genome.fa

```
Full path to bwa executable [/path/to/bwa_executable]:
Full path to samtools executable [/path/to/samtools_executable]:
Full path to crispr-genome in a single fasta file [/path/to/sgRNA-targeted-genome.fa]:
Configuration file successfully written.
```
The path in the brackets will be empty if pipeline has never been configured or it should have a path in the bracket of the most recent configuration of the pipeline.  Configuration only needs to be performed once unless any of these paths have been updated or changed, in which, the pipeline needs to be re-configured.

###### Example usage:

```
chunky run sgRNA_representation_vers2.py -input </path/to/fastq/input/directory/> -output </path/to/out/directory/>
```

#### Output Files
-----------------
For each FASTQ library analyzed sgRNA_representation_vers2.py outputs the following files:
* SAM with SAI
* sorted BAM with BAI
* indexstats file from samtools

It also outputs an additional file called sgRNA_library_complexities.txt that has a time stamp in the name.  This file is created each time the program is run and contains the name of all the libraries that were procressed and the number of different sgRNAs that were represented from the sgRNA genome.
