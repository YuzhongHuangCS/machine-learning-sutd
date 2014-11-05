#!/bin/bash
echo "Linear Kernel:"
svm-train -t 0 training.txt
svm-predict validation.txt training.txt.model output.txt
echo -e "\n"

echo "Polynomial Kernel:"
svm-train -t 1 training.txt
svm-predict validation.txt training.txt.model output.txt
echo -e "\n"

echo "Radial basis Kernel:"
svm-train -t 2 training.txt
svm-predict validation.txt training.txt.model output.txt
echo -e "\n"

echo "Sigmoid Kernel:"
svm-train -t 3 training.txt
svm-predict validation.txt training.txt.model output.txt
echo -e "\n"
