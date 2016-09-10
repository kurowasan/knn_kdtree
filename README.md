# knn_kdtree
Following my data structure course, I wanted to try implementing a machine learning algorithm from scratch.
Quickly, I realized that the simple kNN algorithm have a complexity of O(nm) if implemented naively (where m = points in the training set, n = points in the testing set).
To optimize it, you can create a k-d tree: a binary tree that recursively separate the space. 
In the worst case, you'll still have a complexity of O(nm), but in most cases you'll have O(n log(m)).
To keep track of the nearest neighbor, I also had to implement a bounded priority queue.

To test my algorithm, I used the letter recognition dataset from UCI (https://archive.ics.uci.edu/ml/datasets/Letter+Recognition).
There is 20000 instances of letters. The features were pre-engineered: for example, a feature is the mean edge count left to right.
I used 90% of the data for the training and the rest for validation with a k=3.
I got an accuracy of 0.9565.

