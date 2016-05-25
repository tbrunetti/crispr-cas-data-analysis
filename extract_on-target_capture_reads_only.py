import sys
from multiprocessing import Pool
from multiprocessing import Process
import time

#sys.argv[1]=bed file of capture regions
#sys.argv[2]=bed file of reads
#sys.argv[3]=string with name of capture region for title in output file
#sys.argv[4]=string with name of read file for title in output file

def makeCapture():
	#key=chromosome in bed file
	#value=list of tuples (start nt, end nt) of capture region in bed from bed file
	captureSites={}
	f=open(sys.argv[1], 'r')
	for captureRegion in f.xreadlines():
		captureRegion=captureRegion.rstrip()
		captureRegion=captureRegion.split('\t')
		#checks if chromosome key has already been made and adds tuple
		if captureRegion[0] in captureSites:
			captureSites[captureRegion[0]]=captureSites[captureRegion[0]]+[(captureRegion[1], captureRegion[2])] 
		#if chromosome key had not been made
		else:
			captureSites[captureRegion[0]]=[(captureRegion[1], captureRegion[2])]

	return captureSites


def selectReads(captureSites, line):
	for tuples in range(len(captureSites[line[0]])):
		readStatus=checkRange(int(captureSites[line[0]][tuples][0]), int(captureSites[line[0]][tuples][1]), int(line[1]), int(line[2]));
		if readStatus==True:
			return line


#if return True, add read to list, else skip read
def checkRange(capStart, capEnd, readStart, readEnd):	
	return max(capStart, readStart)<=min(capEnd, readEnd)



if __name__=='__main__':
	pool=Pool(processes=5)
	onTargetReads=open(str(sys.argv[4])+'-reads-overlapping-'+str(sys.argv[3])+'capture-region-'+str(time.strftime("%Y%m%d"))+'.bed', 'w')
	captureSites=makeCapture();
	with open(sys.argv[2]) as input:
		for line in input:
			line=line.rstrip()
			line=line.split('\t')
			#line=selectReads(captureSites, line)
			results=pool.apply_async(selectReads, kwds={"captureSites":captureSites, "line":line})
			if str(results.get())!='None':
				onTargetReads.write(str(results.get()[0])+'\t'+results.get()[1]+'\t'+results.get()[2]+'\n')
			#results=pool.apply(selectReads, (captureSites, line))
			#print retrieveResults[0]
			#for i in range(0, len(retrieveResults)):
			#if str(results.get())!='None':
			#	onTargetReads.write(str(results.get[0])+'\t'+results[1]+'\t'+results[2]+'\n')
