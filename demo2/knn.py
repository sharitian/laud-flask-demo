import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

knn_df = pd.read_csv("laud/dim_df.csv")

data = knn_df.iloc[:,-(len(knn_df.columns) - 2):].values
data = StandardScaler().fit_transform(data)
target = knn_df["cure_status"].values
train_data, test_data, train_target, test_target = train_test_split(data, target, test_size=0.3, random_state=216)

params_to_try = {"n_neighbors": range(1, 30)}
knn_search = GridSearchCV(estimator = KNeighborsClassifier(), param_grid = params_to_try, cv = 10)
knn_search.fit(train_data, train_target)
print(knn_search.best_params_)
print("Accuracy on training data:", knn_search.score(train_data, train_target))
print("Accuracy on testing data:", knn_search.score(test_data, test_target))