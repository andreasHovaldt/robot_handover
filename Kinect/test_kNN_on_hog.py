import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA 

import matplotlib.pyplot as plt

import time 

hog_pose_data = np.loadtxt("hog_pose_data.txt")

training_data, testing_data = train_test_split(hog_pose_data, test_size=0.2, random_state=13)

print(f"No. of training examples: {training_data.shape[0]}")
print(f"No. of testing examples: {testing_data.shape[0]}")

x_train = training_data[:,0:training_data.shape[1]-1]
y_train = training_data[:,training_data.shape[1]-1]

x_test = testing_data[:,0:testing_data.shape[1]-1]
y_test = testing_data[:,testing_data.shape[1]-1]


#scaler = preprocessing.StandardScaler().fit(x_train)
#the traning data is scaled 
#sx_train = scaler.transform(x_train)
#print(sx_train[:,1])
#the test data is scaled 
#sx_test = scaler.transform(x_test)
#cov_matrix = np.cov(sx_train.T)
#eigen_vals, eigen_vectors = np.linalg.eig(cov_matrix)
#print(f" eig vals = {eigen_vals} \n eig_vec = \n {eigen_vectors}")

#plt.plot(eigen_vals)
#plt.show()


#classifing the data 
classifier = KNeighborsClassifier(n_neighbors=2, metric="euclidean", algorithm="ball_tree")
classifier.fit(x_train,y_train)

start_time = time.time()
y_pred = classifier.predict(x_test)
end_time = time.time()
correct = 0
for pred, real in zip(y_pred, y_test):
    print(f"pred = {pred} \t real = {real}")
    if pred == real:
        correct += 1
print(f"correct = {(correct / len(y_test))*100}%")

print(f"pred time {end_time-start_time}")