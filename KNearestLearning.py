def classifyLearn( element , dataset , labels ,k):
#size in number of rows
dataSetSize = dataSet.shape[0]

#tile will propogate the elemnt n times ... here n= dataSetSize
diffMat = tile(element , (dataSetSize , 1)) - datset

sqDiffMat = diffMat ** 2
# root
sqDistance = sqDiffMat ** 0.5 
sortedDistIndices = distance.argsort()
classCount ={}

for i n range(k):
  voteIlabel = labels(sortedDistIndices[i])
  classCount[voteIlabel] = classCount.get(voteIlabel , 0) +1
  
sortedClassCount = sorted(classCount.iteritems() ,
 key = operator.itemgetter[1] , reverse = True)
 return sortedClassCount[0][0]
 
