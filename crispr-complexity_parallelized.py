import sys
sys.path.insert(0, '/usr/lib/python2.7/dist-packages')
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from multiprocessing import Pool
import time

#FOR EXACT METHOD
#sys.argv[1]=method, exact or mismatch
#sys.argv[2]=guide RNA library
#sys.argv[3]=only sequences from fastq illumina output

#FOR MISMATCH METHOD
#sys.argv[1]=method, exact or mismatch
#sys.argv[2]=integer for percent mismatch
#sys.argv[3]=guide RNA library
#sys.argv[4]=only sequences from fastq illumina output


def exactMatch(line):

	line=line.rstrip('\n')
	count=0
		
	f=open(sys.argv[3], 'r')
	for seqLine in f.xreadlines():
		if line in seqLine:
			count=count+1	
	f.close()
			
	appendToFile=str(line)+'\t'+str(count)+'\n'		
	return appendToFile

	
def mismatchOption(line):
		
	similarityScore=int(sys.argv[2])
	line=line.rstrip('\n')
	count=0

	f=open(sys.argv[4], 'r')
	for seqLine in f.xreadlines():
		if line in seqLine:
			count=count+1
		#based on Levenshtein distance
		elif int(fuzz.partial_ratio(line, seqLine))>=similarityScore:
			count=count+1
	f.close()
	
	appendToFile=str(line)+'\t'+str(count)+'\n'		
	return appendToFile


#----------------------------------------------------------------------------------------------------
		
if __name__=='__main__':
	#parallelize
	pool=Pool(4)
	#method for exact counts only
	if sys.argv[1]=='exact':
		f2=open('readCounts_per_sgRNA_exact_matches_'+str(time.strftime("%Y%m%d"))+'.txt', 'w')
		with open(sys.argv[2]) as input:
			results=pool.map(exactMatch, input, 4)
		for i in range(0, len(results)):
			f2.write(results[i])	


	elif sys.argv[1]=='mismatch':		
		#integer of what percent similarity the two sequences need to be
		#in order to be counted as a hit
		similarityScore=sys.argv[2]
		f2=open('readCounts_per_sgRNA_simScore_'+str(similarityScore)+'_'+str(time.strftime("%Y%m%d"))+'.txt', 'w')
		#f2=open('readCounts_per_sgRNA_exact_matches.txt', 'w')
		with open(sys.argv[3]) as input:
			results=pool.map(mismatchOption, input, 4)
		for i in range(0, len(results)):
			f2.write(results[i])

	else:
		print "Error: Invalid method, please choose either 'exact' or 'mismatch'"
