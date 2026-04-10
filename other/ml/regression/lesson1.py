import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model, model_selection

#step1: Load the diabetes dataset and target extraction
# https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset
X,y= datasets.load_diabetes(return_X_y=True)
print(X.shape)
print(X[0])

#step2: feature extraction and reshape
# | Step           | Shape     | Meaning                                 |
# | -------------- | --------- | --------------------------------------- |
# | Original       | (442, 10) | 442 samples, 10 features                |
# | After `X[:,2]` | (442,)    | 1 feature, but flattened                |
# | After reshape  | (442, 1)  | 442 samples, 1 feature (correct format) |
# tall all row and one column -- reshape will change it into 2d array
X=X[:,2].reshape(-1,1)
print(X.shape)

#step2.1: data split
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.33)

#step3: model tarining
# for prediction linera regression is used
model=linear_model.LinearRegression() # select model
model.fit(X_train,y_train) # train the model

#step4: model evaluation


#step5: model prediction
predict=model.predict(X_test)

# step6: model visualization -- plot the table
#  use matplotlib -- title, show, xlabel, ylabel
# Same X → two Y values:
#        → actual (dot) ---scatter
#        → predicted (line) ---- line
plt.scatter(X_test,y_test,color='black')
plt.plot(X_test,predict,color='blue')
plt.title('A Graph Plot Showing Diabetes Progression Against BMI')
plt.xlabel('BMI')
plt.ylabel('desease progression')
plt.show()


# Think a bit about what's going on here. A straight line is running through many small dots of data, but what is it doing exactly? Can you see how you should be able to use this line to predict where a new, unseen data point should fit in relationship to the plot's y axis? Try to put into words the practical use of this model.

# What the line is actually doing

# The blue line represents a function:

# y = mX + b
# m → slope (how much y changes when X changes)
# b → intercept (starting point)

# This line is chosen to minimize the overall error between:

# actual values (y_test, black dots)
# predicted values (y_pred, blue line)

# Formally, it minimizes something like:

# total squared distance between dots and the line

# This model allows you to: --practical use
# 1. Predict unknown outcomes
# 2. Predict the relationship between two variables

