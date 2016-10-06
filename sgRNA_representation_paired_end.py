#This is made for paired end less than 70bp Illumina sequences only

import os
from chunkypipes.components import *
import subprocess
import datetime

class Pipeline(BasePipeline):

	def dependencies(self):
		return []
	def description(self):
		return 'Calculates complexity of sgRNA libraries against homemade crispr-genome (paired-end)'

	def configure(self):
		return{
			'cutadapt':{
				'path':'Full path to cutadapt executable'
				},
			'bwa':{
				'path':'Full path to bwa executable'
				},
			'samtools':{
				'path':'Full path to samtools executable'
				},
			'crisprRef':{
				'path':'Full path to crispr-genome in a single fasta file, needs BWA index files in same directory!!!'
				}	
		}

	def add_pipeline_args(self, parser):
		parser.add_argument('-forward_first', required=True, help='string sequnce of pair1 forward adapter, 5 -> 3')
		parser.add_argument('-reverse_first', required=True, help='string sequence of pair1 reverse adapter, 5 -> 3')
		parser.add_argument('-forward_second', required=True, help='reverse compliment of the pair1 reverse_first')
		parser.add_argument('-reverse_second', required=True, help='reverse compliment of the pair1 forward_first')
		parser.add_argument('-fileName', required=True, help='name of output files prefix')
		parser.add_argument('-1', required=True, help='path to first pair fastq file')
		parser.add_argument('-2', required=True, help='path to second pair fastq file')
		parser.add_argument('-output', required=True, help='path to output final results directory')
		#parser.add_argument('--spaceSaveMode', help='if this mode is used, SAM files will be deleted')	


	def run_pipeline(self, pipeline_args, pipeline_config):
		cutadapt=Software('cutadapt', pipeline_config['cutadapt']['path'])
		align=Software('bwa', pipeline_config['bwa']['path'])
		bamIndex=Software('samtools', pipeline_config['samtools']['path'])
		print "trimming adapters..."
		cutadapt.run(
			# removes forward adapter on first file
			Parameter('-g', pipeline_args['forward_first']),
			# removes reverse adapter on second file
			Parameter('-a', pipeline_args['reverse_first']),
			Parameter('-G', pipeline_args['forward_second']),
			Parameter('-A', pipeline_args['reverse_second']),
			Parameter('-n', '2'),
			Parameter('-m', '10'),
			Parameter('-o', pipeline_args['output']+pipeline_args['fileName']+'_trimmed.1.fastq'),
			Parameter('-p', pipeline_args['output']+pipeline_args['fileName']+'_trimmed.2.fastq'),
			Parameter(pipeline_args['1']),
			Parameter(pipeline_args['2'])
			)
		
		print 'aligning first pair...'
		align.run(
			Parameter('aln', pipeline_config['crisprRef']['path']),
			Parameter(pipeline_args['output']+pipeline_args['fileName']+'_trimmed.1.fastq'),
			Redirect(stream=Redirect.STDOUT, dest=pipeline_args['output']+pipeline_args['fileName']+'_1.sai')
			)

		print 'aligning second pair...'
		align.run(
			Parameter('aln', pipeline_config['crisprRef']['path']),
			Parameter(pipeline_args['output']+pipeline_args['fileName']+'_trimmed.2.fastq'),
			Redirect(stream=Redirect.STDOUT, dest=pipeline_args['output']+pipeline_args['fileName']+'_2.sai')
			)

		print 'creating SAM file...'
		align.run(
			Parameter('sampe', pipeline_config['crisprRef']['path']),
			Parameter(pipeline_args['output']+pipeline_args['fileName']+'_1.sai'),
			Parameter(pipeline_args['output']+pipeline_args['fileName']+'_2.sai'),
			Parameter(pipeline_args['output']+pipeline_args['fileName']+'_trimmed.1.fastq'),
			Parameter(pipeline_args['output']+pipeline_args['fileName']+'_trimmed.2.fastq'),
			Redirect(stream=Redirect.STDOUT, dest=pipeline_args['output']+pipeline_args['fileName']+'.sam')
			)

		print 'converting SAM to BAM...'
		convertSam=subprocess.Popen((pipeline_config['samtools']['path'], 'view', '-bS', pipeline_args['output']+pipeline_args['fileName']+'.sam'), stdout=subprocess.PIPE)
		sortBam=subprocess.check_output((pipeline_config['samtools']['path'], 'sort', '-o', pipeline_args['output']+pipeline_args['fileName']+'_sorted.bam'), stdin=convertSam.stdout)
		convertSam.wait()

		bamIndex.run(
			Parameter('index'),
			Parameter(pipeline_args['output']+pipeline_args['fileName']+'_sorted.bam'),
			Redirect(stream=Redirect.STDOUT, dest=pipeline_args['output']+pipeline_args['fileName']+'.bai')
			)

		print 'calculating index statistics...'
		#outputs the index stats of bam file, needed to calculated complexity
		bamIndex.run(
			Parameter('idxstats'),
			Parameter(pipeline_args['output']+pipeline_args['fileName']+'_sorted.bam'),
			Redirect(stream=Redirect.STDOUT, dest=pipeline_args['output']+pipeline_args['fileName']+'_indexStats.txt')
			)

		filename=open(pipeline_args['output']+'sgRNA-library-complexities-'+pipeline_args['fileName']+'.txt', 'w')
		total=0
		with open(pipeline_args['output']+pipeline_args['fileName']+'_indexStats.txt') as sample_stats:
			for line in sample_stats:
				line=line.split('\t')
				if line[2]=='0' and line[3].rstrip('\n')=='0':
					continue;
				else:
					total+=1
		with open(pipeline_args['output']+'sgRNA-library-complexities-'+pipeline_args['fileName']+'.txt', 'a+') as library_stats:
			library_stats.write('The total number of sgRNAs represented in '+ pipeline_args['fileName'] +' are '+str(total)+'\n')