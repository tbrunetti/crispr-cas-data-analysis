#This is made for single end less than 70bp Illumina sequences only

import os
from chunkypipes.components import *
import subprocess
import datetime

class Pipeline(BasePipeline):

	def dependencies(self):
		return []
	def description(self):
		return 'Calculates complexity of sgRNA libraries against homemade crispr-genome'

	def configure(self):
		return{
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
		parser.add_argument('-input', required=True, help='path to directory of all fastq files to analyze')
		parser.add_argument('-output', required=True, help='path to output final results directory')
		#parser.add_argument('--spaceSaveMode', help='if this mode is used, SAM files will be deleted')	


	def run_pipeline(self, pipeline_args, pipeline_config):
		align=Software('bwa', pipeline_config['bwa']['path'])
		bamIndex=Software('samtools', pipeline_config['samtools']['path'])

		for fastq in os.listdir(pipeline_args['input']):
			print "aligning fastq files...fastq_name="+str(fastq)
			align.run(
				Parameter('aln', pipeline_config['crisprRef']['path']),
				Parameter(pipeline_args['input']+fastq),
				Redirect(stream=Redirect.STDOUT, dest=pipeline_args['output']+str(fastq[:-6])+'.sai')
				)

			align.run(
				Parameter('samse'),
				Parameter(pipeline_config['crisprRef']['path']),
				Parameter(pipeline_args['output']+str(fastq[:-6])+'.sai'),
				Parameter(pipeline_args['input']+fastq),
				Redirect(stream=Redirect.STDOUT, dest=pipeline_args['output']+str(fastq[:-6])+'.sam')
				)

		for sam in os.listdir(pipeline_args['output']):
			#checks to make sure SAM file
			if sam[-4:]=='.sam':
				#converts SAM to BAM and then sorts BAM file
				print "converting SAM to BAM and sorting...sample_name="+str(sam)
				convertSam=subprocess.Popen((pipeline_config['samtools']['path'], 'view', '-bS', pipeline_args['output']+sam), stdout=subprocess.PIPE)
				sortBam=subprocess.check_output((pipeline_config['samtools']['path'], 'sort', '-o', pipeline_args['output']+sam[:-4]+'_sorted.bam' ), stdin=convertSam.stdout)
				convertSam.wait()

				#indexes the converted and sorted BAM file
				bamIndex.run(
					Parameter('index'),
					Parameter(pipeline_args['output']+sam[:-4]+'_sorted.bam')
					)

				print 'calculating index statistics...'
				#outputs the index stats of bam file, needed to calculated complexity
				bamIndex.run(
					Parameter('idxstats'),
					Parameter(pipeline_args['output']+sam[:-4]+'_sorted.bam'),
					Redirect(stream=Redirect.STDOUT, dest=pipeline_args['output']+str(sam[:-4])+'_indexStats.txt')
					)

		#finds indexStats file generated from above and calculates the estimated number of sgRNA represented
		filename=pipeline_args['output']+'sgRNA-library-complexities-'+str(time.strftime("%a-%d-%b-%Y_%H:%M:%S"))+'.txt'
		f=open(filename, 'w')
		for indexStats in os.listdir(pipeline_args['output']):
			if indexStats[-14:]=='indexStats.txt':
				print 'Calculating library complexity...lib_name='+str(indexStats)
				total=0
				with open(pipeline_args['output']+indexStats) as input:
					for line in input:
						line=line.split('\t')
						if line[2]=='0' and line[3].rstrip('\n')=='0':
							continue;
						else:
							total+=1
				with open(filename, 'a+') as file:
					file.write('The total number of sgRNAs represented in '+ str(indexStats)+' are '+str(total)+'\n')
