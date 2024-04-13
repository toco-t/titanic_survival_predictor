from django.urls import path

from .views import HomePageView, PredictionPageView, ResultsPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("prediction/", PredictionPageView.as_view(), name="prediction"),
    path("results/", ResultsPageView.as_view(), name="results"),
]