from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import TaskListCreate, UserViewSet, UserRegister, ProjectViewSet, TaskViewSet, CommentListCreate, CommentViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')

task_retrieve_update_delete = TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})
comment_retrieve_update_delete = CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

endpoints = [
    # user
    path('users/register/', UserRegister.as_view(), name='user-register'),

    # task
    path('projects/<int:pk>/tasks/', TaskListCreate.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', task_retrieve_update_delete, name='task-retrieve-update-delete'),

    # comment
    path('tasks/<int:pk>/comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', comment_retrieve_update_delete, name='comment-retrieve-update-delete')
] + router.urls
