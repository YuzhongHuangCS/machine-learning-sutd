using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using ParaList = System.Collections.Generic.List<double[]>;
using Score = System.Tuple<double[], int>;

namespace ML {
    class Program {
        static public double[][] trainSet;
        static public double[][] testSet;
        static public double[] initPara = new double[3] { 0, 0, 0 };

        static void Main(string[] args) {
            trainSet = (from line in File.ReadAllLines("train_1_5.csv") select (Array.ConvertAll(line.Split(','), double.Parse).ToArray())).ToArray();
            testSet = (from line in File.ReadAllLines("test_1_5.csv") select (Array.ConvertAll(line.Split(','), double.Parse).ToArray())).ToArray();

            Score trainResult = deepin(0, initPara, 2);
            int predictionError = predictErrors(trainResult.Item1);

            Console.WriteLine("Train Result: <{0}, {1}>", string.Join(", ", trainResult.Item1), trainResult.Item2);
            Console.WriteLine("Prediction Error: {0}", string.Join(", ", predictionError));
        }

        static public int sign(double[] row, double[] para) {
            double result = para[0] * row[0] + para[1] * row[1] + para[2];
            if (result >= 0) {
                return 1;
            } else {
                return -1;
            }
        }

        static public int errors(double[] para) {
            int sum = 0;
            foreach (var row in trainSet) {
                if (sign(row, para) != row[2]) {
                    sum++;
                }
            }
            return sum;
        }

        static public int predictErrors(double[] para) {
            int sum = 0;
            foreach (var row in testSet) {
                if (sign(row, para) != row[2]) {
                    sum++;
                }
            }
            return sum;
        }

        static public double[] patch(double[] para, double[] row) {
            double[] tryPara = new double[3] {
                para[0] + row[2] * row[0],
		        para[1] + row[2] * row[1],
		        para[2] + row[2]
            };
            return tryPara;
        }

        static public ParaList analysys(double[] para) {
            ParaList candidatePara = new ParaList();
            foreach (var row in trainSet) {
                if (sign(row, para) != row[2]) {
                    candidatePara.Add(patch(para, row));
                }
            }
            return candidatePara;
        }

        static public Score deepin(int now, double[] para, int limit) {
            List<Score> thisResult = new List<Score>();
            thisResult.Add(new Tuple<double[], int>(para, errors(para)));

            var tryParas = analysys(para);
            int size = tryParas.Count;

            if (now < limit) {
                Parallel.For(0, size, (int i) => {
                    var childPara = tryParas[i];
                    thisResult.Add(deepin(now + 1, childPara, limit));
                    if (now == 0) {
                        Console.WriteLine("No: {0}, Score: <{1}, {2}>", i++, string.Join(",", thisResult.Last().Item1), thisResult.Last().Item2);
                    }
                });
            } else {
                foreach (var subPara in tryParas) {
                    thisResult.Add(new Tuple<double[], int>(subPara, errors(subPara)));
                }
            }

            double[] bestPara = thisResult[0].Item1;
            int bestError = thisResult[0].Item2;

            foreach (var score in thisResult) {
                if (score.Item2 < bestError) {
                    bestPara = score.Item1;
                    bestError = score.Item2;
                }
            }

            return new Tuple<double[], int>(bestPara, bestError);
        }
    }
}
