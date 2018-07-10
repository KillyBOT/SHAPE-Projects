# -*- coding: utf-8 -*-

def SelectionSort(inList):
    sortedArray = []
    unsortedArray = inList
    
    while len(unsortedArray) != 0:
        smallestNum = unsortedArray[0]
        for num in unsortedArray:
            if num < smallestNum:          
                smallestNum = num
        sortedArray.append(smallestNum)
        unsortedArray.remove(smallestNum)
        
    return sortedArray
    
def InsertionSort(inList):
    returnList = inList
    for x in range(len(returnList)):
        for num in range(len(returnList)-1):
            if returnList[num] > returnList[num+1]:
                returnList[num], returnList[num+1] = returnList[num+1], returnList[num]
                
    return returnList

def SplitList(inList):

    list1 = inList[:int(len(inList)/2)]
    list2 = inList[int(len(inList)/2):]
            
    return list1, list2
    
def CompareLists(list1, list2):
    returnList = []
    list1Place = 0
    list2Place = 0
    while list1Place < len(list1) and list2Place < len(list2):
        if list1[list1Place] < list2[list2Place]:
            returnList.append(list1[list1Place])
            list1Place += 1
        elif list1[list1Place] > list2[list2Place]:
            returnList.append(list2[list2Place])
            list2Place += 1
    
    if list1Place < len(list1): 
        returnList.extend(list1[list1Place:])
    elif list2Place < len(list2):
        returnList.extend(list2[list2Place:])
    
    return returnList

def MergeSort(listToSort):
    
    if len(listToSort) == 1:
        return listToSort
    list1, list2 = SplitList(listToSort)
    list1Sorted = MergeSort(list1)
    list2Sorted = MergeSort(list2)
    
    return CompareLists(list1Sorted,list2Sorted)
    
def findSplit(listToArrange):
    finalList = listToArrange
    startPoint = 1
    endPoint = len(finalList)-1
    while endPoint > startPoint:
        if finalList[startPoint] < finalList[0]:
            startPoint += 1
        elif finalList[endPoint] > finalList[0]:
            endPoint -= 1
        else:
            finalList[startPoint], finalList[endPoint] = finalList[endPoint], finalList[startPoint]
            startPoint += 1
            endPoint -= 1
    if finalList[0] > finalList[endPoint]:
        finalList[0], finalList[endPoint] = finalList[endPoint], finalList[0]
            
    return finalList[:startPoint], finalList[startPoint:]
    
def findSplit2(listToArrange):
    finalList = listToArrange
    startPoint = 0
    endPoint = len(finalList)-1
    pivotPoint = len(finalList)//2
    while endPoint > startPoint:
        if finalList[startPoint] < finalList[pivotPoint]:
            startPoint += 1
        elif finalList[endPoint] > finalList[pivotPoint]:
            endPoint -= 1
        else:
            finalList[startPoint], finalList[endPoint] = finalList[endPoint], finalList[startPoint]
            startPoint += 1
            endPoint -= 1
          
    return finalList[:startPoint], finalList[startPoint:]
    
def QuickSort(listToSort):
    if len(listToSort) == 1:
        return listToSort
    list1, list2 = findSplit2(listToSort)
    list1Arranged = QuickSort(list1)
    list2Arranged = QuickSort(list2)
    return list1Arranged+list2Arranged

    
            
#print(SelectionSort([1,3,5,7,9,2,4,6,8,0]))
#print(InsertionSort([1,3,5,7,9,2,4,6,8,0]))
#print(MergeSort([1,3,5,7,9,2,4,6,8,0]))
print(QuickSort([1,3,5,7,9,2,4,6,8,0]))