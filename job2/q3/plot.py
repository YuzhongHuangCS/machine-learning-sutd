#!/usr/bin/python
import json
import matplotlib.pyplot as plt

trainRates = []
validationRates = []
testRates = []

with open("result.json", 'r') as fin:
	rates = json.loads(fin.read())
	for row in rates:
		trainRates.append(row[0])
		validationRates.append(row[1])
		testRates.append(row[2])

plt.plot(range(len(trainRates)), trainRates, linewidth = 2, label = 'Accuracy in train set')
plt.plot(range(len(validationRates)), validationRates, linewidth = 2, label = 'Accuracy in validation set')
plt.plot(range(len(testRates)), testRates, linewidth = 2, label = 'Accuracy in test set')
plt.xlabel('Iteration')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
