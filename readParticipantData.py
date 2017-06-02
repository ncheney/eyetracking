#!/usr/bin/python

import os
import numpy as np

agreeScale = ["zeroHolder","stronglyDisagree","disagree","neutral","agree","stronglyAgree"]
treatmentNames = ["MouesClicks","Eyetracking"]
measurementNames = [
"avgSuccesss",
"interestingShapes",
"goalsReached",
"novelSuggestions",
"aidedCreativity",
"enjoyable",
"trialCount",
"genCount",
"totalTime",
"directedTime"
]

numEntries = 10

data = np.zeros((2,numEntries,100))
# 0: avgSuccesss
# 1: interestingShapes
# 2: goalsReached
# 3: novelSuggestions
# 4: aidedCreativity
# 5: enjoyable
# 6: trialCount
# 7: genCount
# 8: totalTime
# 9: part1time

reactions = [[],[]]

directedGenCountData = np.zeros((2,100))

successData = np.zeros((2,100))
successCounter = np.zeros((2))-1

treatmentCounter = np.zeros((2))-1
print treatmentCounter

for userDir, dnames, fnames in os.walk("/home/nick/projects/endlessforms/hyperneat/eyetrack/python/participants"):
	if not userDir.endswith("/participants"):
		print
		print "-------------------------------------------------------------------------------------------"
		print "dirpath:", userDir
		userName = userDir.split("/")[-1]
		print "userName:",userName
		print
		trialCount = 0
		genCount = 0
		treatmentType = 99
		shapeGenCounter = np.zeros((3))

		userInputFile = open(userDir+"/"+userName+"_UserInput")
		for line in userInputFile:
			# print line

			if line.split()[0] == "000000.00":
				print line.split()[-1]
				if "MouseClicks" in line.split()[-1]:
					treatmentType = 0
				elif "Eyetracking" in line.split()[-1]: 
					treatmentType = 1

				treatmentCounter[treatmentType] += 1

			if "success?" in line:
				print "success?",line.split()[-1],":",agreeScale.index(line.split()[-1])
				successCounter[treatmentType] += 1
				successData[treatmentType,successCounter[treatmentType]] = agreeScale.index(line.split()[-1])

			if "interestingShapes?" in line:
				print "interestingShapes?",line.split()[-1],":",agreeScale.index(line.split()[-1])
				data[treatmentType,1,treatmentCounter[treatmentType]] = agreeScale.index(line.split()[-1])
			
			if "goalsReached?" in line:
				print "goalsReached?",line.split()[-1],":",agreeScale.index(line.split()[-1])
				data[treatmentType,2,treatmentCounter[treatmentType]] = agreeScale.index(line.split()[-1])

			if "novelSuggestions?" in line:
				print "novelSuggestions?",line.split()[-1],":",agreeScale.index(line.split()[-1])
				data[treatmentType,3,treatmentCounter[treatmentType]] = agreeScale.index(line.split()[-1])

			if "aidedCreativity?" in line:
				print "aidedCreativity?",line.split()[-1],":",agreeScale.index(line.split()[-1])
				data[treatmentType,4,treatmentCounter[treatmentType]] = agreeScale.index(line.split()[-1])

			if "enjoyable?" in line:
				print "enjoyable?",line.split()[-1],":",agreeScale.index(line.split()[-1])
				data[treatmentType,5,treatmentCounter[treatmentType]] = agreeScale.index(line.split()[-1])

			if "reason?" in line:
				trialCount += 1

			if "DIRECTED-EVOLUTION:" in line:
				startTime = float(line.split()[0])

			if "###" in line:
				endTime = float(line.split()[0])

			if "***" in line:
				data[treatmentType,9,treatmentCounter[treatmentType]] = float(line.split()[0])/60

			if "overallReactions?" in line:
				reactions[treatmentType].append(line.split("overallReactions?")[-1])

		totalTime = endTime - startTime

		print "trialCount:",trialCount
		data[treatmentType,6,treatmentCounter[treatmentType]] = trialCount

		for fname in fnames:
			# print "fnames:"
			if fname.endswith(".xml"):
				genCount += 1

			for shapeNum in range(3):
				if userName+str(shapeNum) in fname:
					shapeGenCounter[shapeNum] += 1

		print "genCount:",genCount
		data[treatmentType,7,treatmentCounter[treatmentType]] = genCount

		data[treatmentType,8,treatmentCounter[treatmentType]] = float(totalTime)/60

		directedGenCountData[treatmentType,treatmentCounter[treatmentType]*3:(treatmentCounter[treatmentType]+1)*3] = shapeGenCounter

		print "DIRECTED-EVOLUTION genCounts:",shapeGenCounter

		print "gens/trial:",float(genCount)/float(trialCount)

		print "totalTime (mins):",totalTime/60
		print "seconds per gen:",totalTime/genCount
		print "seconds per trial:",totalTime/trialCount

# for i in range(2):
# 	print directedGenCountData[i,np.nonzero(directedGenCountData[i])]


print
print "==========================================================================================="
print "----- END DATA ----------------------------------------------------------------------------"

print "DIRECTED-EVOLUTION:"
for i in range(2):
	print "successData"+treatmentNames[i]+":"
	print successData[i,np.nonzero(successData[i])]
	print "mean:",np.mean(successData[i,np.nonzero(successData[i])]) 
	print "std:",np.std(successData[i,np.nonzero(successData[i])]) 
	print

for i in range(2):
	print "successGens"+treatmentNames[i]+":"
	print directedGenCountData[i,np.nonzero(directedGenCountData[i])]
	print "mean:",np.mean(directedGenCountData[i,np.nonzero(directedGenCountData[i])]) 
	print "std:",np.std(directedGenCountData[i,np.nonzero(directedGenCountData[i])]) 
	print

print "OVERALL DATA:"
for i in range(2):
	print "overallData"+treatmentNames[i]+":::::::::::::::::::::::::::::"
	print
	for j in range(1,numEntries):
		print measurementNames[j]+":"
		# print data[i,j]
		print data[i,j,np.nonzero(data[i,j])]
		print "mean:",np.mean(data[i,j,np.nonzero(data[i,j])])
		print "std:", np.std(data[i,j,np.nonzero(data[i,j])])
		print

for i in range(2):
	print
	print "OverallReactions "+treatmentNames[i]+"------"
	print
	for line in reactions[i]:
		print line

print treatmentCounter
