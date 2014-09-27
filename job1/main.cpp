#include <iostream>
#include <fstream>
#include <boost/algorithm/string.hpp>

using namespace std;

// function defines
typedef array<double, 3> Row;
typedef array<double, 3> Para;

list<Row> readFile(string fileName);
int sign(const Row &row, const Para &para);
int errors(const Para &para);
int predictErrors(const Para &para);
Para patch(const Para &para, const Row &row);
list<Para> analysys(const Para &para);
array<double, 4> deepin(int i, Para para, int depth);

// preset data defines
Para initPara = {0, 0, 0};
auto trainFileContent = readFile("train_1_5.csv");
auto testFileContent = readFile("test_1_5.csv");

int main(void) {
	auto finalResult = deepin(0, initPara, 1);
	int bestErrors = finalResult[0];
	Para bestPara = {
		finalResult[1],
		finalResult[2],
		finalResult[3],
	};
	int predictionError = predictErrors(bestPara);

	cout << bestErrors << endl;
	cout << bestPara[0] << ", " << bestPara[1] << ", " << bestPara[2] << endl;
	cout << predictionError << endl;
}

list<Row> readFile(string fileName) {
	ifstream inFile(fileName);
	string line;
	vector<string> words;
	Row nums;
	list<Row> fileContent;

	while(getline(inFile, line)){
		boost::split(words, line, boost::is_any_of(","));
		nums = {
			stod(words[0]),
			stod(words[1]),
			stod(words[2])
		};
		fileContent.push_back(nums);
	}

	return fileContent;
}

int sign(const Row &row, const Para &para) {
	double result = para[0] * row[0] + para[1] * row[1] + para[2];
	if(result >= 0){
		return 1;
	} else{
		return -1;
	}
}

int errors(const Para &para) {
	int sum = 0;

	for(auto it = trainFileContent.begin(); it != trainFileContent.end(); it++){
		Row &row = *it;
		if(sign({row[0], row[1]}, para) != row[2]){
			sum++;
		}
	}

	return sum;
}

int predictErrors(const Para &para) {
	int sum = 0;

	for(auto it = testFileContent.begin(); it != testFileContent.end(); it++){
		Row &row = *it;
		if(sign(row, para) != row[2]){
			sum++;
		}
	}

	return sum;
}

Para patch(const Para &para, const Row &row) {
	Para newPara = {
		para[0] + row[2] * row[0],
		para[1] + row[2] * row[1],
		para[2] + row[2]
	};

	return newPara;
}

list<Para> analysys(const Para &para) {
	list<Para> candidatePara;

	for(auto it = trainFileContent.begin(); it != trainFileContent.end(); it++){
		Row &row = *it;
		if(sign(row, para) != row[2]){
			candidatePara.push_back(patch(para, row));
		}
	}

	return candidatePara;
}

array<double, 4> deepin(int i, Para para, int depth) {
	list< pair<int, Para> > thisResult;
	
	thisResult.push_back(pair<int, Para>(errors(para), para));

	if(i < depth){
		auto tryParas = analysys(para);

		for(auto it = tryParas.begin(); it != tryParas.end(); it++){
			Para &subPara = *it;
			auto subResult = deepin(i+1, subPara, depth);
			thisResult.push_back( pair<int, Para>(subResult[0], {subResult[1], subResult[2], subResult[3]}));
		}
	} else{
		auto tryParas = analysys(para);

		for(auto it = tryParas.begin(); it != tryParas.end(); it++){
			Para &subPara = *it;
			thisResult.push_back( pair<int, Para>(errors(subPara), subPara));
		}
	}

	double bestError = thisResult.begin()->first;
	Para bestPara = thisResult.begin()->second;

	for(auto it = thisResult.begin(); it != thisResult.end(); it++){
		if(it->first < bestError){
			bestError = it->first;
			bestPara = it->second;
		}
	}

	array<double, 4> returnData = {
		bestError,
		bestPara[0],
		bestPara[1],
		bestPara[2]
	};
	return(returnData);
}