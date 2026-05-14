from sklearn.linear_model import LinearRegression
import numpy as np

def predict_rainfall(values):
    x = np.array(range(len(values))).reshape(-1,1)
    y = np.array(values)

    model = LinearRegression()
    model.fit(x,y)

    pred = model.predict([[len(values)]])
    return round(pred[0],2)