import sys

#sys.argv[1]=idxstats file created from samtools

#NOTE: this takes into account mapped and unmapped reads
#for mapped reads only use line[2] and ignore line[3]

def sgRNAsRepresented():
	
	with open(sys.argv[1]) as input:
		total=0
		for line in input:
			line=line.split('\t')
			if line[2]=='0' and line[3].rstrip('\n')=='0':
				continue;
			else:
				total+=1
	print 'The total number of sgRNAs represented in the crispr-cas genome library are '+str(total)

if __name__=='__main__':
	sgRNAsRepresented();