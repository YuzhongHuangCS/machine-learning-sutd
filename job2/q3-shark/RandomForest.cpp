#include <shark/Data/Csv.h> //importing the file
#include <shark/Algorithms/Trainers/RFTrainer.h> //the random forest trainer
#include <shark/ObjectiveFunctions/Loss/ZeroOneLoss.h> //zero one loss for evaluation

#include <iostream> 

using namespace std; 
using namespace shark;

ClassificationDataset loadData(const string& dataFile, const string& labelFile){
	//we first load two separate data files for the training inputs and the labels of the data point
	Data<RealVector> inputs;
	Data<unsigned int> labels;
	try {
		importCSV(inputs, dataFile, ' ');
		importCSV(labels, labelFile, ' ');
	} catch (Exception e) {
		cerr << e.what() << endl;
		exit(EXIT_FAILURE);
	}
	//now we create a complete dataset which represents pairs of inputs and labels
	ClassificationDataset data(inputs, labels);

	return data;	
}

int main(int argc, char **argv) {

	// generate dataset
	ClassificationDataset data = loadData("trainfeat.txt", "trainlabs.txt");
	ClassificationDataset dataTest = loadData("testfeat.txt", "testlabs.txt");

	cout << "Training set: number of data points: " << data.numberOfElements()
		<< " number of classes: " << numberOfClasses(data)
		<< " input dimension: " << inputDimension(data) << endl;

	cout << "Test set: number of data points: " << dataTest.numberOfElements()
		<< " number of classes: " << numberOfClasses(dataTest)
		<< " input dimension: " << inputDimension(dataTest) << endl;

	//Generate a random forest
	RFTrainer trainer;
	RFClassifier model;
	trainer.train(model, data);

	// evaluate Random Forest classifier
	ZeroOneLoss<unsigned int, RealVector> loss;
	Data<RealVector> prediction = model(data.inputs());
	cout << "Random Forest on training set error " << loss.eval(data.labels(), prediction) << endl;

	prediction = model(dataTest.inputs());
	cout << "Random Forest on test set error " << loss.eval(dataTest.labels(), prediction) << endl;
}
