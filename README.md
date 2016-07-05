
# crispr-cas-data-analysis

The scripts and programs listed in this repository are made to be used for projects using genome-wide sgRNA (CRISPR-cas9) screening assays and analysis.

## sgRNA_representation_vers2.py
-----------------------------
A pipeline to analyze the library complexities of sgRNA screens against a list of targeted sgRNAs.  The user has the ability to feed in a directory of fastq files as input into sgRNA_representation_vers2.py.  It will proceed to align all the reads in each of the libraries against a user generated sgRNA genome.  The aligned reads are then used to calculate the overall complexity of each library and the number of reads representing each target in the genome.  **NOTE:This pipeline has only been optimized for single-end 70bp and less reads from Illumina TruSeq libraries**

####Requirements
----------------
* chunkypipes (http://chunky-pipes.readthedocs.io/en/stable/getting_started.html)   
* bwa (http://bio-bwa.sourceforge.net/)  
* samtools (http://samtools.sourceforge.net/)  


####Generate sgRNA "genome"
--------------------------  
Before sgRNA_representation_vers2.py can be run, the user must generate and index a custom sgRNA genome using bwa.

###### Example usage:

```
chunky run sgRNA_representation_vers2.py -input </path/to/fastq/input/directory> -output <path/to/out/directory>
```


