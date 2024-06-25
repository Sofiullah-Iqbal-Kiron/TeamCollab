from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, UserRegister, ProjectViewSet, TaskViewSet, CommentViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'comments', CommentViewSet, basename='comment')

# user
user_register = UserRegister.as_view()

endpoints = [
    # user
    path('users/register/', user_register, name='user-register'),
] + router.urls
