#!/usr/bin/env python3

from Common import *

ExprimentName = "P1"

ZipMethodName	= "DNSLogZip"
ZipMethodSuffix  = "dlz.gz"

CompressedFilePathFormat = "/media/ramdisk/{exprimentName}.{datasetName}.{resultName}.txt.{suffix}"

Params = ["N1", "N2", "N5", "N10", "N15", "N20", "N25", "N30", "N35", "N40", "N45" "N50", 
"N55", "N60", "N65", "N70", "N75", "N80", "N85", "N90", "N95", "N100"]
		  
ColNames = ["N=1", "N=2", "N=5", "N=10", "N=15", "N=20", "N=25", "N=30", "N=35", "N=40", "N=45", "N=50",
"N=55", "N=60", "N=65", "N=70", "N=75", "N=80", "N=85", "N=90", "N=95", "N=100"]

ZipCMD = "rm -f /media/ramdisk/{exprimentName}.{datasetName}.{resultName}.txt.{suffix} " \
"&& time -p ( DNSLogzip -Z -F -{param} < /media/ramdisk/data/{datasetName}/{logFileName} " \
"-o /media/ramdisk/{exprimentName}.{datasetName}.{resultName}.txt.{suffix})"

UnzipCMD = "time -p ( gunzip -c /media/ramdisk/{exprimentName}.{datasetName}.{resultName}.txt.{suffix} > /media/ramdisk/{exprimentName}.{datasetName}.{resultName}.txt ;" \
" DNSLogzip -D  < /media/ramdisk/{exprimentName}.{datasetName}.{resultName}.txt > /dev/null ) && " \
"rm -rf /media/ramdisk/{exprimentName}.{datasetName}.{resultName}.txt; " \
"rm -rf /media/ramdisk/{exprimentName}.{datasetName}.{resultName}.txt.{suffix}"

class P1Experiment(QExperiment):	

	def __init__(self):
		QExperiment.__init__(self, "{}.csv".format(ExprimentName))
		
	def Run(self):
		for i in range(len(self.Datasets)):
			datasetResult = self.datasetResults[i]
			datasetResult.datasetName = self.Datasets[i]
			datasetResult.results = [Result() for _ in range(len(Params))]
			
			for j in range(len(Params)):
				result = datasetResult.results[j]
				
				originalFilePath = "/media/ramdisk/data/{}/{}".format(datasetResult.datasetName, self.LogFileName)
				result.name = Params[j]
				suffix = ZipMethodSuffix
				compressedFilePath = CompressedFilePathFormat.format(exprimentName=ExprimentName, datasetName=datasetResult.datasetName, resultName=result.name, suffix=suffix)
				
				# Execute the zip command and get its output
				command = ZipCMD.format(exprimentName=ExprimentName, workingDir=self.workingDir, datasetName=datasetResult.datasetName, resultName=result.name, logFileName=self.LogFileName, suffix=suffix, param=Params[j])				
				self.RunZipCMD(command, result, originalFilePath, compressedFilePath)
				
				# Execute the decompression command and get its output
				command = UnzipCMD.format(exprimentName=ExprimentName, workingDir=self.workingDir, datasetName=datasetResult.datasetName, resultName=result.name, logFileName=self.LogFileName, suffix=suffix, param=Params[j])
				self.RunUnzipCMD(command, result, originalFilePath)

	def DumpResult(self):
	
		with open(self.resultFilePath, "w+") as f:
			# the first row
			f.write("DatasetName")		
			for k in range(len(ColNames)):
				f.write(",{0}(CR),{0}(CS),{0}(DS)".format(ColNames[k]))
			f.write("\n")
			
			# A row data.
			for i in range(len(self.datasetResults)):
				datasetResult = self.datasetResults[i]
				f.write(datasetResult.datasetName)
				
				for k in range(len(Params)):
					result = datasetResult.results[k]
					f.write(",{:.2f},{:.2f},{:.2f}".format(result.ratio, result.speed / 1024 / 1024, result.dspeed / 1024 / 1024))
				f.write("\n")

if __name__ == "__main__":

	PrintMsg("Start.")
	ex = P1Experiment()
	
	"""parse paraments"""
	ex.ParseArgs(sys)
	ex.Run()
	ex.DumpResult()

	PrintMsg("Done.")
	