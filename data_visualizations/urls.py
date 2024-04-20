from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("task/<int:id>", views.select, name="open"),
    path("plot/<int:id>", views.plot, name="plot"),
    path("upload", views.upload, name="upload")
]
