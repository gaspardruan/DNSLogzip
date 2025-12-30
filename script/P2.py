#!/usr/bin/env python3

from Common import *

ExprimentName = "P2"

ZipMethodName	= "DNSLogZip"
ZipMethodSuffix  = "dlz.gz"

CompressedFilePathFormat = "/media/ramdisk/{exprimentName}.{datasetName}.{resultName}*"

Params = ["P1", "P2", "P4", "P6", "P8", "P10", "P12", "P14", "P16", "P18", "P20", "P22", "P24", "P26", "P28", "P30"]
		  
ColNames = ["P=1", "P=2", "P=4", "P=6", "P=8", "P=10", "P=12", "P=14", "P=16", "P=18", "P=20", 
						"P=22", "P=24", "P=26", "P=28", "P=30"]

ZipCMD = "rm -f /media/ramdisk/{exprimentName}.{datasetName}.{resultName}* " \
"&& time -p ( DNSLogzip -Z -F -{param} < /media/ramdisk/data/{datasetName}/{logFileName} " \
"-o /media/ramdisk/{exprimentName}.{datasetName}.{resultName})"

UnzipCMD = "time -p ( gunzip -c /media/ramdisk/{exprimentName}.{datasetName}.{resultName}* > /media/ramdisk/{exprimentName}.{datasetName}.{resultName}.txt ;" \
" DNSLogzip -D  < /media/ramdisk/{exprimentName}.{datasetName}.{resultName}.txt > /dev/null ) && " \
"rm -f /media/ramdisk/{exprimentName}.{datasetName}.{resultName}*; "

class P2Experiment(QExperiment):	

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
	ex = P2Experiment()
	
	"""parse paraments"""
	ex.ParseArgs(sys)
	ex.Run()
	ex.DumpResult()

	PrintMsg("Done.")
	