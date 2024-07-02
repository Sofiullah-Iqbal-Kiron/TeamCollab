from django.urls import path

from .demo_views import ProjectList


demo_endpoints = [
    path("demo/projects/", ProjectList.as_view(), name="demo-project-list"),
]
