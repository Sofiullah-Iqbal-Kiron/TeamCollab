from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, UserRegister, ProjectViewSet, TaskViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'comments', CommentViewSet, basename='comment')

endpoints = [
    # user
    path('users/register/', UserRegister.as_view(), name='user-register'),
] + router.urls
