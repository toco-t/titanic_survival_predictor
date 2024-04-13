from keras.src.saving.saving_api import load_model
from pandas import DataFrame

data = {
    "Age_(0, 10]": 1,
    "Age_(10, 20]": 0,
    "SigSp": 2,
    "Parch": 1,
    "Fare": 37.0,
    "Pclass_3": 0,
    "Sex_female": 0,
    "Cabin_0": 0,
    "Embarked_S": 1,
}
data_frame = DataFrame([data])

try:
    model = load_model("ann.keras")
    prediction = model.predict(data_frame, verbose=1)
    print(prediction)
except FileNotFoundError:
    print("Error: Model not found")