from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from keras.src.saving.saving_api import load_model
from pandas import DataFrame


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class PredictionPageView(TemplateView):
    template_name = "prediction.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["age_groups"] = [
            f"{age_group}-{age_group + 10}" for age_group in range(0, 80, 10)
        ]
        context["ports"] = ["Cherbourg", "Queenstown", "Southampton"]
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class ResultsPageView(TemplateView):
    template_name = "results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prediction"] = kwargs.get("prediction")
        return context

    def post(self, request, *args, **kwargs):
        try:
            age = request.POST.get("age")
            if age == "Select your age group":
                raise ValueError("Please select an age group")

            sex = request.POST.get("sex")
            if not sex:
                raise ValueError("Please select a gender")

            fare = request.POST.get("fare")
            if not fare:
                raise ValueError("Please select a fare")

            pclass = request.POST.get("socio-economic")
            if pclass == "Select your socio-economic status":
                raise ValueError("Please select a socio-economic status")

            sibsp = request.POST.get("siblings-spouses")
            if not sibsp:
                raise ValueError("Please select the number of siblings/spouses aboard")

            parch = request.POST.get("parents-children")
            if not parch:
                raise ValueError("Please select the number of parents/children aboard")

            cabin = request.POST.get("cabin")

            embarked = request.POST.get("port")
            if embarked == "Select your port of embarkation":
                raise ValueError("Please select the port of embarkation")

        except ValueError as e:
            contexts = self.get_context_data()
            contexts["error_message"] = f"Error: {e}"
            return render(request, self.template_name, contexts)

        data = {
            "Age_(0, 10]": 1 if age == "0-10" else 0,
            "Age_(10, 20]": 1 if age == "10-20" else 0,
            "SigSp": int(sibsp),
            "Parch": int(parch),
            "Fare": float(fare),
            "Pclass_3": 1 if pclass == "Low" else 0,
            "Sex_female": 1 if sex == "Female" else 0,
            "Cabin_0": 1 if cabin else 0,
            "Embarked_S": 1 if embarked == "Southampton" else 0,
        }
        data_frame = DataFrame([data])

        try:
            model = load_model("ann.keras")
            prediction = model.predict(data_frame, verbose=1)
        except FileNotFoundError:
            contexts = self.get_context_data()
            contexts["error_message"] = "Error: Model not found"
            return render(request, self.template_name, contexts)
        except ValueError as e:
            contexts = self.get_context_data()
            contexts["error_message"] = f"Error: {e}"
            return render(request, self.template_name, contexts)

        contexts = self.get_context_data()
        contexts["prediction"] = "Survived" if prediction[0][0] > 0.5 else "Died"
        return render(request, self.template_name, contexts)
