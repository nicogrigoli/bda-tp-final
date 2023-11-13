import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error
import csv


x = []
y = []

with open('datos_finales.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        else:
            x.append([float(row[6]), float(row[7]), float(row[8]), float(row[9]), float(row[10])])
            y.append(float(row[12]))

            line_count += 1




X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.3, random_state=None)


model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=10000)
model.fit(X_train, Y_train)


Y_pred = model.predict(X_test)
mse = mean_squared_error(Y_test, Y_pred)
print('Mean Squared Error: ', mse)