#!/usr/bin/pypy
import math
import heapq
import copy

#trainSet = [list(map(lambda i: float(i), line.split(' '))) for line in open('trainfeat.txt', 'r')]
#trainLabel = [float(line) for line in open('trainlabs.txt', 'r')]
testSet = [list(map(lambda i: float(i), line.split(' '))) for line in open('testfeat.txt', 'r')]
testLabel = [float(line) for line in open('testlabs.txt', 'r')]

def entropy(first, second):
	try:
		total = first + second
		fp = float(first) / total
		sp = float(second) / total
		return -((fp * math.log(fp, 2)) + (sp * math.log(sp, 2)))
	except ValueError as e:
		if (first == 0) or (second == 0):
			return -math.log(1, 2)
		else:
			raise e

class Node(object):
	def __init__(self, data, label, feature = None, featureIndex = None, featureValue = None, flag = None):
		super(Node, self).__init__()
		self.data = data
		self.label = label
		self.feature = feature
		self.featureIndex = featureIndex
		self.featureValue = featureValue
		self.flag = flag
		
		if flag == None:
			self.features = len(data[0])
			self.samples = len(data)
			self.trues = int(sum(label))
			self.entropy = entropy(self.trues, self.samples - self.trues)
			self.childs = []

			#print("Sample: %s, Feature: %s, Trues: %s, FeatureIndex: %s, FeatureValue: %s" % (self.samples, self.features, self.trues, self.featureIndex, self.featureValue))
			if self.samples > 1 and self.features > 1 and self.trues != 0 and self.trues != self.samples:
				self.prepare()
				self.prepareTrue()
				self.grow()

		else:
			print("FeatureIndex: %s, FeatureValue: %s, Flag: %s" % (self.featureIndex, self.featureValue, self.flag))

		del self.data
		del self.label

	def prepare(self):
		table = []

		for f in range(self.features):
			table.append({})
			for r in range(self.samples):
				if table[f].get(self.data[r][f]) == None:
					table[f][self.data[r][f]] = 1
				else:
					table[f][self.data[r][f]] += 1

		self.table = table

	def prepareTrue(self):
		table = []

		for f in range(self.features):
			table.append({})
			for r in range(self.samples):
				if table[f].get(self.data[r][f]) == None:
					table[f][self.data[r][f]] = 0
				if self.label[r] == 1:
					table[f][self.data[r][f]] += 1

		self.trueTable = table

	def indexToEntropy(self, index):
		aggregate = 0
		weightSum = 0

		for key, value in self.table[index].items():
			trueValue = self.trueTable[index][key]
			newEntropy = entropy(value - trueValue, trueValue)
			aggregate += newEntropy * value
			weightSum += value

		return aggregate / weightSum

	def grow(self):
		'''
		key -> globalFeatureIndex
		index -> localFeatureIndex
		'''

		candidates = []
		localFeatureIndex = 0

		for key, value in self.feature.items():
			if value == False:
				continue
			else:
				heapq.heappush(candidates, (self.indexToEntropy(localFeatureIndex), localFeatureIndex, key))
				localFeatureIndex += 1

		choice = heapq.heappop(candidates)
		index = choice[1]

		#print(choice)
		#print(self.table[index])
		#print(self.trueTable[index])
		#print(self.entropy, choice[0])

		childFeature = copy.deepcopy(self.feature)
		childFeature[choice[2]] = False

		if len(self.table[index]) == 1:
			print(choice)
			print(self.table[index])
			print(self.trueTable[index])
			print(self.entropy, choice[0])
			key, value = self.table[index].popitem()
			key, trueValue = self.trueTable[index].popitem()
			if value > (2 * trueValue):
				childNode = Node(None, None, childFeature, choice[2], key, False)
			else:
				childNode = Node(None, None, childFeature, choice[2], key, True)

			self.childs.append(childNode)
			return

		for key in self.table[index]:
			childData = copy.deepcopy(self.data)
			childLabel = copy.deepcopy(self.label)

			i = 0
			while i < len(childData):
				if childData[i][index] != key:
					del childData[i]
					del childLabel[i]
				else:
					del childData[i][index]
					i += 1

			childNode = Node(childData, childLabel, childFeature, choice[2], key)
			self.childs.append(childNode)

allFeature = dict.fromkeys(range(len(testSet[0])), True)
rootNode = Node(testSet, testLabel, allFeature)
