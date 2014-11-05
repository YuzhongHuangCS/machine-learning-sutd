from numpy import *
import matplotlib.pyplot as plt
from random import randrange
import heapq

trainFile = array([list(map(lambda i: float(i), line.split(','))) for line in open('train_diabetes.csv', 'r')])
dataSet = trainFile[:, 1:]
labelSet = trainFile[:, 0]

draw = []
# calculate the sigmoid function
def train(**options):
	samples, features = dataSet.shape
	alpha = options['alpha']
	limit = options['limit']
	weights = empty(features)

	for k in range(limit / 100):
		for j in range(100):
			i = randrange(samples)
			grad = labelSet[i] * dataSet[i, :] / (1 + exp(dot(dataSet[i, :], weights) * labelSet[i])) 
			weights += grad * alpha

		draw.append(test(weights))

	return weights

def test(weights):
	samples, features = dataSet.shape
	return -sum([log(1 + exp(-labelSet[i] * dot(dataSet[i, :], weights))) for i in range(samples)]) / samples

result = train(alpha=0.1, limit=10000)

diff = [draw[i+1]-draw[i] for i in range(len(draw)-1)]
diffCopy = [draw[i+1]-draw[i] for i in range(len(draw)-1)]
heapq.heapify(diff)
biggest = heapq.nlargest(5, diff)

print("Most important features...")

for i in biggest:
	print diffCopy.index(i)

plt.plot(range(len(draw)), draw, linewidth = 2, label = 'accuracy')
plt.show()