import math

class Vertex(object):
	def __init__(self,name,connections):
		self.name = name
		self.connections = connections

	def __str__(self):
		return str("Name: %s\t Connections: %s\n" % (self.name, self.connections))
		#return str(self.name)

	def __repr__(self):
		return str(self)

class Queue(object):

	def __init__(self):
		self.queueData = []

	def enque(self, data):
		self.queueData.append(data)

	def deque(self):
		return self.queueData.pop(0)

	def __str__(self):
		return str(self.queueData)

class Connection(object):
	def __init__(self,connectedTo,length):
		self.connectedTo = connectedTo
		self.length = length

	def __str__(self):
		return self.connectedTo

	def __repr__(self):
		return str(self)

def CreateGraph(connections):
	finalGraph = []
	for l, v in connections.items():
		vertexToAdd = Vertex(l,[])
		if len(v) > 0:
			if type(v[0]) == str:
				vertexToAdd.connections = v
			elif type(v[0]) == list:
				for x in v:
					if len(x) > 0:
						vertexToAdd.connections.append(Connection(x[0],x[1]))
		finalGraph.append(vertexToAdd)

	return finalGraph

def CreateConnectionList(graph):
	returnList = {}
	for x in graph.queueData:
		returnList[x.name] = x.connections

	return returnList

def findConnections(connections):
	verticesDict = {}

	for l in connections:
		verticesDict[l.name] = 0

	for x in connections:
		for y in x.connections:
			verticesDict[str(y)] += 1

	return verticesDict

def TopSort(connections):
	editConnections = connections
	verticesDict = findConnections(editConnections)
	finalGraph = Queue()

	while len(verticesDict) != 0:

		for n, l in enumerate(verticesDict):
			if verticesDict[l] == 0:
	 			finalGraph.enque(connections[n])
	 			editConnections.pop(n)
	 			del verticesDict[l]
	 			break

		verticesDict = findConnections(editConnections)

	return finalGraph

listOfConnections = {
"E":[["D",3],["C",4]],
"D":[["B",2]],
"C":[["B",5],["A",3]],
"B":[["A",7]],
"A":[[]]
}

newListOfConnections = {
"A":[["B",4],["C",3],["D",5]],
"B":[["D",3]],
"C":[["E",4]],
"D":[["F",3]],
"E":[["F",4]],
"F":[["G",5]],
"G":[[]],
}

def FindPath(originName, destinationName, connectionList):
	travelDict = {}
	toBacktrackQueue = Queue()
	toBacktrackQueue.enque(originName)
	currentPoint = toBacktrackQueue.deque()
	while str(currentPoint) != destinationName:
		for x in connectionList[str(currentPoint)]:
			if str(x) not in travelDict:
				toBacktrackQueue.enque(x)
				#print(currentPoint, type(currentPoint))
				travelDict[str(x)] = currentPoint
		currentPoint = toBacktrackQueue.deque()

	goBackPoint = destinationName
	#finalDict = {}
	finalList = [destinationName]

	while str(goBackPoint) != originName:
		#print(finalDict)
		#finalDict[goBackPoint] = travelDict[goBackPoint]
		finalList.insert(0, travelDict[str(goBackPoint)])
		goBackPoint = travelDict[str(goBackPoint)]

	return finalList

testGraph = CreateGraph(newListOfConnections)
testGraph2 = CreateGraph(listOfConnections)
testGraph = TopSort(testGraph)
testGraph2 = TopSort(testGraph2)
print(testGraph)
print(testGraph2)
newListOfConnections = CreateConnectionList(testGraph)
listOfConnections = CreateConnectionList(testGraph2)
print(FindPath("A","G",newListOfConnections))
pathOfConnections2 = FindPath("E","A",listOfConnections)
print(pathOfConnections2)