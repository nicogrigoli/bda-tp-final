import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns



# Asumimos que ya tienes los datos en un archivo CSV
dataClima = pd.read_csv('DatosPruebaInventados.csv')


dataClima.head()
dataClima.info()
dataClima.describe()


# Selecciona las características y la variable objetivo
X = dataClima.drop('foco_incendio', axis=1)
#X = dataClima.drop('DIA_TRANSPORTE', axis=1)
y = dataClima['foco_incendio'] # VARIABLE A PREDECIR

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Crea un modelo de random forest
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Entrena el modelo con los datos de entrenamiento
model.fit(X_train, y_train)


# Realiza predicciones sobre los datos de prueba
y_pred = model.predict(X_test)

print("Valores predichos:")
print(y_pred)
print("Nombres de las clases: ", model.classes_)


y_pred_new = model.predict(X)

print("Valores predichos nuevos:")
print(y_pred_new)
print("Nombres de las clases: ", model.classes_)

# Calcula la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print('Precisión: ', accuracy)

# Muestra la matriz de confusión
cm = confusion_matrix(y_test, y_pred)
print('Matriz de confusión: \n', cm)

# Muestra el informe de clasificación
cr = classification_report(y_test, y_pred)
print('Informe de clasificación: \n', cr)

#sns.pairplot(dataClima)

sns.lmplot(x='mes_precipitaciones', y='temperatura', hue="foco_incendio", data=dataClima)
plt.show()

#https://www.youtube.com/watch?v=OJ6hF5ZUSuo&t=768s