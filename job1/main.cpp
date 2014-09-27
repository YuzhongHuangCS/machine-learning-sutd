#include <iostream>
#include <fstream>
#include <memory>
#include <boost/algorithm/string.hpp>

using namespace std;

// type deinfe
typedef array<double, 3> Row;
typedef shared_ptr< list<Row> > RowList;
typedef array<double, 3> Para;
typedef shared_ptr< list<Para> > ParaList;
typedef pair<int, Para> Score;

// function defines
RowList readFile(const string& fileName);
int sign(const Row& row, const Para& para);
int errors(const Para& para);
int predictErrors(const Para& para);
Para patch(const Para& para, const Row& row);
ParaList analysys(const Para& para);
Score deepin(const int i, const Para& para, const int depth);

// preset data defines
Para initPara = {0, 0, 0};
auto trainFileContent = readFile("train_1_5.csv");
auto testFileContent = readFile("test_1_5.csv");

// main
int main(void) {
	Score finalResult = deepin(0, initPara, 1);
	
	int bestError = finalResult.first;
	Para bestPara = finalResult.second;
	
	int predictionError = predictErrors(bestPara);

	cout << bestError << endl;
	cout << bestPara[0] << ", " << bestPara[1] << ", " << bestPara[2] << endl;
	cout << predictionError << endl;
}

// function implementation
RowList readFile(const string& fileName) {
	ifstream inFile(fileName);
	string line;
	vector<string> words;
	Row nums;
	RowList fileContent = static_cast<RowList>(new list<Row>);

	while(getline(inFile, line)){
		boost::split(words, line, boost::is_any_of(","));
		nums = {
			stod(words[0]),
			stod(words[1]),
			stod(words[2])
		};
		fileContent->push_back(nums);
	}

	return fileContent;
}

int sign(const Row& row, const Para& para) {
	double result = para[0] * row[0] + para[1] * row[1] + para[2];
	if(result >= 0){
		return 1;
	} else{
		return -1;
	}
}

int errors(const Para& para) {
	int sum = 0;

	for(auto it = trainFileContent->begin(); it != trainFileContent->end(); it++){
		Row& row = *it;
		if(sign(row, para) != row[2]){
			sum++;
		}
	}

	return sum;
}

int predictErrors(const Para& para) {
	int sum = 0;

	for(auto it = testFileContent->begin(); it != testFileContent->end(); it++){
		Row& row = *it;
		if(sign(row, para) != row[2]){
			sum++;
		}
	}

	return sum;
}

Para patch(const Para& para, const Row& row) {
	Para tryPara = {
		para[0] + row[2] * row[0],
		para[1] + row[2] * row[1],
		para[2] + row[2]
	};

	return tryPara;
}

ParaList analysys(const Para& para) {
	ParaList candidatePara = static_cast<ParaList>(new list<Para>);

	for(auto it = trainFileContent->begin(); it != trainFileContent->end(); it++){
		Row& row = *it;
		if(sign(row, para) != row[2]){
			candidatePara->push_back(patch(para, row));
		}
	}

	return candidatePara;
}

Score deepin(const int i, const Para& para, const int depth) {
	list<Score> thisResult;
	thisResult.push_back(Score(errors(para), para));

	if(i < depth){
		auto tryParas = analysys(para);

		for(auto it = tryParas->begin(); it != tryParas->end(); it++){
			Para& childPara = *it;
			thisResult.push_back(deepin(i+1, childPara, depth));
		}
	} else{
		auto tryParas = analysys(para);

		for(auto it = tryParas->begin(); it != tryParas->end(); it++){
			Para& subPara = *it;
			thisResult.push_back(Score(errors(subPara), subPara));
		}
	}

	int bestError = thisResult.begin()->first;
	Para bestPara = thisResult.begin()->second;

	for(auto it = thisResult.begin(); it != thisResult.end(); it++){
		if(it->first < bestError){
			bestError = it->first;
			bestPara = it->second;
		}
	}

	return(Score(bestError, bestPara));
}