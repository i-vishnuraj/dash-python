import numpy as np
import pandas as pd

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

X_digits,y_digits = load_digits(return_X_y=True)

X_train,X_test,y_train,y_test = train_test_split(X_digits,y_digits)

from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans

log_reg = LogisticRegression(solver="saga",max_iter=1200)
log_reg.fit(X_train,y_train)

print("Logistic Reg : ",log_reg.score(X_test,y_test))

from sklearn.pipeline import Pipeline

pipeline = Pipeline([("kmeans",KMeans(n_clusters=50)),("log_reg",LogisticRegression(solver="saga",max_iter=4000)),])

pipeline.fit(X_train,y_train)

print("KMeans + LR :",pipeline.score(X_test,y_test))

from sklearn.model_selection import GridSearchCV

param_grid = dict(kmeans__n_clusters = range(2,100))
grid_clf = GridSearchCV(pipeline, param_grid,cv=3, verbose=2)
grid_clf.fit(X_train,y_train)

print(grid_clf.best_params_)
print("Grid Search CV : ",grid_clf.score(X_test,y_test))
