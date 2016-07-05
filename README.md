
# crispr-cas-data-analysis
==========================

The scripts and programs listed in this repository are made to be used for projects using genome-wide sgRNA (CRISPR-cas9) screening assays and analysis.

## crispr-complexity_parallelized.py
---------------------------------

## sgRNA_representation_vers2.py
-----------------------------
A pipeline to analyze library complexity of sgRNA screens against a list of targeted sgRNAs.  The user can feed in a directory of fastq files and sgRNA_representation_vers2.py will align all the reads in each of the libraries against a user generated sgRNA genome.  The aligned reads from each library is then used to calculate the overall complexity of each library and the number of reads representing each target which is useful for data normalization.

####Requirements
----------------
* chunkypipes  
* bwa  
* samtools  


####Generate sgRNA "genome"
--------------------------  
sgRNA_representation_vers2.py requires the Python package chunkypipes.

###### Example usage:

```
chunky run sgRNA_representation_vers2.py -input </path/to/fastq/input/directory> -output <path/to/out/directory>
```


